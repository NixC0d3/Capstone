from flask import Blueprint, request, jsonify
from sqlalchemy import text
from app.extensions import db

import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler


recommendation_bp = Blueprint("recommendation_bp", __name__)


def get_ml_scores(user_id):
    """
    Builds a user-organisation matrix from engagement_logs and ratings_reviews,
    then uses TruncatedSVD matrix factorization to predict organisations
    the user may like.
    """

    interaction_sql = text("""
        SELECT
            user_id,
            organisation_id,
            CASE
                WHEN engagement_type = 'profile_view' THEN 1
                WHEN engagement_type = 'save' THEN 3
                WHEN engagement_type = 'message' THEN 4
                WHEN engagement_type = 'rating' THEN 5
                WHEN engagement_type = 'review' THEN 6
                WHEN engagement_type = 'volunteer_signup' THEN 5
                ELSE 0
            END AS score
        FROM engagement_logs
        WHERE user_id IS NOT NULL

        UNION ALL

        SELECT
            user_id,
            organisation_id,
            rating * 2 AS score
        FROM ratings_reviews
        WHERE user_id IS NOT NULL;
    """)

    with db.engine.connect() as connection:
        interactions = pd.read_sql(interaction_sql, connection)

    if interactions.empty:
        return {}

    matrix = interactions.pivot_table(
        index="user_id",
        columns="organisation_id",
        values="score",
        aggfunc="sum",
        fill_value=0
    )

    if user_id not in matrix.index:
        return {}

    if matrix.shape[0] < 2 or matrix.shape[1] < 2:
        return {}

    n_components = min(5, matrix.shape[0] - 1, matrix.shape[1] - 1)

    if n_components < 1:
        return {}

    model = TruncatedSVD(
        n_components=n_components,
        random_state=42
    )

    user_features = model.fit_transform(matrix)
    organisation_features = model.components_

    predicted_values = user_features @ organisation_features

    predicted_matrix = pd.DataFrame(
        predicted_values,
        index=matrix.index,
        columns=matrix.columns
    )

    user_predictions = predicted_matrix.loc[user_id]

    already_interacted = matrix.loc[user_id]
    already_interacted = already_interacted[already_interacted > 0].index

    user_predictions = user_predictions.drop(
        already_interacted,
        errors="ignore"
    )

    if user_predictions.empty:
        return {}

    scores = user_predictions.values.reshape(-1, 1)

    scaler = MinMaxScaler(feature_range=(0, 100))
    scaled_scores = scaler.fit_transform(scores).flatten()

    ml_scores = {}

    for organisation_id, score in zip(user_predictions.index, scaled_scores):
        ml_scores[int(organisation_id)] = float(score)

    return ml_scores


@recommendation_bp.route("/user/<int:user_id>", methods=["GET"])
def recommend_for_user(user_id):
    organisation_type = request.args.get("type", "").strip().lower()
    limit = request.args.get("limit", 6, type=int)

    ml_scores = get_ml_scores(user_id)

    org_sql = text("""
    WITH user_category_activity AS (
        SELECT
            category_id,
            SUM(action_score) AS behavior_score
        FROM (
            SELECT
                o.category_id,
                CASE
                    WHEN e.engagement_type = 'profile_view' THEN 1
                    WHEN e.engagement_type = 'save' THEN 3
                    WHEN e.engagement_type = 'message' THEN 4
                    WHEN e.engagement_type = 'rating' THEN 5
                    WHEN e.engagement_type = 'review' THEN 6
                    WHEN e.engagement_type = 'volunteer_signup' THEN 5
                    ELSE 0
                END AS action_score
            FROM engagement_logs e
            JOIN organisations o
                ON o.organisation_id = e.organisation_id
            WHERE e.user_id = :user_id
              AND o.category_id IS NOT NULL

            UNION ALL

            SELECT
                oc.category_id,
                CASE
                    WHEN e.engagement_type = 'profile_view' THEN 1
                    WHEN e.engagement_type = 'save' THEN 3
                    WHEN e.engagement_type = 'message' THEN 4
                    WHEN e.engagement_type = 'rating' THEN 5
                    WHEN e.engagement_type = 'review' THEN 6
                    WHEN e.engagement_type = 'volunteer_signup' THEN 5
                    ELSE 0
                END AS action_score
            FROM engagement_logs e
            JOIN organisation_categories oc
                ON oc.organisation_id = e.organisation_id
            WHERE e.user_id = :user_id
        ) category_actions
        GROUP BY category_id
    ),

    org_category_matches AS (
        SELECT
            organisation_id,
            category_id
        FROM organisations
        WHERE category_id IS NOT NULL

        UNION

        SELECT
            organisation_id,
            category_id
        FROM organisation_categories
    ),

    personal_behavior AS (
        SELECT
            ocm.organisation_id,
            SUM(uca.behavior_score) AS behavior_score
        FROM org_category_matches ocm
        JOIN user_category_activity uca
            ON uca.category_id = ocm.category_id
        GROUP BY ocm.organisation_id
    )

    SELECT
        o.organisation_id,
        o.organisation_name,
        o.organisation_type,
        o.description,
        o.phone,
        o.email,
        o.website_url,

        l.parish,
        l.town,
        l.address,

        c.category_name,

        COALESCE(avg_reviews.average_rating, 0) AS average_rating,
        COALESCE(engagements.engagement_score, 0) AS engagement_score,
        COALESCE(preferences.preference_score, 0) AS preference_score,
        COALESCE(personal_behavior.behavior_score, 0) AS behavior_score

    FROM organisations o

    LEFT JOIN locations l
        ON l.location_id = o.location_id

    LEFT JOIN categories c
        ON c.category_id = o.category_id

    LEFT JOIN (
        SELECT
            organisation_id,
            AVG(rating) AS average_rating
        FROM ratings_reviews
        WHERE is_hidden = FALSE
        GROUP BY organisation_id
    ) avg_reviews
        ON avg_reviews.organisation_id = o.organisation_id

    LEFT JOIN (
        SELECT
            organisation_id,
            SUM(
                CASE
                    WHEN engagement_type = 'profile_view' THEN 1
                    WHEN engagement_type = 'save' THEN 3
                    WHEN engagement_type = 'message' THEN 4
                    WHEN engagement_type = 'rating' THEN 5
                    WHEN engagement_type = 'review' THEN 6
                    WHEN engagement_type = 'volunteer_signup' THEN 5
                    ELSE 0
                END
            ) AS engagement_score
        FROM engagement_logs
        GROUP BY organisation_id
    ) engagements
        ON engagements.organisation_id = o.organisation_id

    LEFT JOIN (
        SELECT
            o2.organisation_id,
            SUM(COALESCE(up.preference_weight, 1) * 10) AS preference_score
        FROM organisations o2
        LEFT JOIN organisation_categories oc
            ON oc.organisation_id = o2.organisation_id
        JOIN user_preferences up
            ON up.category_id = o2.category_id
            OR up.category_id = oc.category_id
        WHERE up.user_id = :user_id
        GROUP BY o2.organisation_id
    ) preferences
        ON preferences.organisation_id = o.organisation_id

    LEFT JOIN personal_behavior
        ON personal_behavior.organisation_id = o.organisation_id

    WHERE
        (:organisation_type = '' OR LOWER(o.organisation_type) = :organisation_type);
""")

    result = db.session.execute(
        org_sql,
        {
            "user_id": user_id,
            "organisation_type": organisation_type
        }
    )

    recommendations = []

    for row in result:
        ml_score = ml_scores.get(row.organisation_id, 0)

        engagement_score = float(row.engagement_score or 0)
        preference_score = float(row.preference_score or 0)
        behavior_score = float(row.behavior_score or 0)
        average_rating = float(row.average_rating or 0)

        final_score = (
            (ml_score * 0.35)
            + (preference_score * 0.20)
            + (behavior_score * 0.35)
            + (engagement_score * 0.05)
            + (average_rating * 2)
        )

        recommendations.append({
            "organisation_id": row.organisation_id,
            "organisation_name": row.organisation_name,
            "organisation_type": row.organisation_type,
            "description": row.description,
            "phone": row.phone,
            "email": row.email,
            "website_url": row.website_url,
            "parish": row.parish,
            "town": row.town,
            "address": row.address,
            "category_name": row.category_name,

            "ml_score": round(ml_score, 2),
            "behavior_score": round(behavior_score, 2),
            "engagement_score": round(engagement_score, 2),
            "preference_score": round(preference_score, 2),
            "average_rating": round(average_rating, 2),
            "recommendation_score": round(final_score, 2)
            
        })

    recommendations.sort(
        key=lambda item: item["recommendation_score"],
        reverse=True
    )

    return jsonify(recommendations[:limit]), 200
