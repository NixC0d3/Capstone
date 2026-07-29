from flask import Blueprint, request, jsonify
from sqlalchemy import text
from app.extensions import db

import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler


recommendation_bp = Blueprint("recommendation_bp", __name__)


def get_action_score_sql():
    """
    Central scoring rule for user actions.
    Stronger actions receive more points than simple views.
    """
    return """
        CASE
            WHEN engagement_type = 'profile_view' THEN 1
            WHEN engagement_type = 'save' THEN 3
            WHEN engagement_type = 'message' THEN 4
            WHEN engagement_type = 'rating' THEN 5
            WHEN engagement_type = 'review' THEN 6
            WHEN engagement_type = 'volunteer_signup' THEN 5
            ELSE 0
        END
    """


def get_user_engagement_count(user_id):
    """
    Counts whether the user has any behaviour history.
    This is used to decide whether to use cold-start recommendation logic.
    """

    row = db.session.execute(
        text("""
            SELECT
                (
                    SELECT COUNT(*)
                    FROM engagement_logs
                    WHERE user_id = :user_id
                )
                +
                (
                    SELECT COUNT(*)
                    FROM ratings_reviews
                    WHERE user_id = :user_id
                ) AS total;
        """),
        {"user_id": user_id}
    ).fetchone()

    return int(row.total or 0)


def get_user_preference_count(user_id):
    """
    Counts signup interests saved in user_preferences.
    """

    row = db.session.execute(
        text("""
            SELECT COUNT(*) AS total
            FROM user_preferences
            WHERE user_id = :user_id;
        """),
        {"user_id": user_id}
    ).fetchone()

    return int(row.total or 0)


def get_ml_scores(user_id):
    """
    Builds a user-organisation matrix from engagement_logs and ratings_reviews,
    then uses TruncatedSVD matrix factorization to predict organisations
    the user may like.

    This only works well after there is enough user activity.
    For a new user, this returns an empty dictionary and the system falls back
    to signup-interest recommendations.
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

    user_engagement_count = get_user_engagement_count(user_id)
    user_preference_count = get_user_preference_count(user_id)

    is_new_user = user_engagement_count == 0

    ml_scores = get_ml_scores(user_id)

    org_sql = text("""
        WITH org_category_matches AS (
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

        user_preferences_scored AS (
            SELECT
                category_id,
                COALESCE(preference_weight, 1) AS preference_weight
            FROM user_preferences
            WHERE user_id = :user_id
        ),

        preferences AS (
            SELECT
                ocm.organisation_id,
                SUM(ups.preference_weight * 25) AS preference_score,
                COUNT(*) AS preference_matches
            FROM org_category_matches ocm
            JOIN user_preferences_scored ups
                ON ups.category_id = ocm.category_id
            GROUP BY ocm.organisation_id
        ),

        user_category_activity AS (
            SELECT
                ocm.category_id,
                SUM(
                    CASE
                        WHEN e.engagement_type = 'profile_view' THEN 1
                        WHEN e.engagement_type = 'save' THEN 3
                        WHEN e.engagement_type = 'message' THEN 4
                        WHEN e.engagement_type = 'rating' THEN 5
                        WHEN e.engagement_type = 'review' THEN 6
                        WHEN e.engagement_type = 'volunteer_signup' THEN 5
                        ELSE 0
                    END
                ) AS behavior_score
            FROM engagement_logs e
            JOIN org_category_matches ocm
                ON ocm.organisation_id = e.organisation_id
            WHERE e.user_id = :user_id
            GROUP BY ocm.category_id
        ),

        personal_behavior AS (
            SELECT
                ocm.organisation_id,
                SUM(uca.behavior_score) AS behavior_score
            FROM org_category_matches ocm
            JOIN user_category_activity uca
                ON uca.category_id = ocm.category_id
            GROUP BY ocm.organisation_id
        ),

        engagement_popularity AS (
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
        ),

        average_reviews AS (
            SELECT
                organisation_id,
                AVG(rating) AS average_rating,
                COUNT(*) AS review_count
            FROM ratings_reviews
            WHERE COALESCE(is_hidden, FALSE) = FALSE
            GROUP BY organisation_id
        ),

        display_categories AS (
            SELECT DISTINCT ON (ocm.organisation_id)
                ocm.organisation_id,
                c.category_name
            FROM org_category_matches ocm
            JOIN categories c
                ON c.category_id = ocm.category_id
            ORDER BY ocm.organisation_id, c.category_name
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

            COALESCE(primary_category.category_name, display_categories.category_name) AS category_name,

            COALESCE(average_reviews.average_rating, 0) AS average_rating,
            COALESCE(average_reviews.review_count, 0) AS review_count,
            COALESCE(engagement_popularity.engagement_score, 0) AS engagement_score,
            COALESCE(preferences.preference_score, 0) AS preference_score,
            COALESCE(preferences.preference_matches, 0) AS preference_matches,
            COALESCE(personal_behavior.behavior_score, 0) AS behavior_score

        FROM organisations o

        LEFT JOIN locations l
            ON l.location_id = o.location_id

        LEFT JOIN categories primary_category
            ON primary_category.category_id = o.category_id

        LEFT JOIN display_categories
            ON display_categories.organisation_id = o.organisation_id

        LEFT JOIN average_reviews
            ON average_reviews.organisation_id = o.organisation_id

        LEFT JOIN engagement_popularity
            ON engagement_popularity.organisation_id = o.organisation_id

        LEFT JOIN preferences
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
        preference_matches = int(row.preference_matches or 0)
        behavior_score = float(row.behavior_score or 0)
        average_rating = float(row.average_rating or 0)

        if is_new_user and user_preference_count > 0:
            # Cold-start logic:
            # A new user has no behaviour yet, so signup interests must dominate.
            final_score = (
                (preference_score * 0.80)
                + (engagement_score * 0.05)
                + (average_rating * 3)
            )

            recommendation_mode = "signup_interests"

        elif user_engagement_count > 0:
            # Returning-user logic:
            # Once the user starts interacting, behaviour becomes more important.
            final_score = (
                (preference_score * 0.35)
                + (behavior_score * 0.40)
                + (ml_score * 0.15)
                + (engagement_score * 0.05)
                + (average_rating * 3)
            )

            recommendation_mode = "behaviour_and_interests"

        else:
            # Fallback:
            # If the user has no preferences and no engagement, show popular/high-rated organisations.
            final_score = (
                (engagement_score * 0.40)
                + (average_rating * 10)
            )

            recommendation_mode = "popular_fallback"

        if preference_matches > 0:
            recommendation_reason = "Matches your selected interests"
        elif behavior_score > 0:
            recommendation_reason = "Similar to organisations you interacted with"
        elif average_rating > 0:
            recommendation_reason = "Recommended based on ratings and activity"
        else:
            recommendation_reason = "Suggested organisation"

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
            "preference_matches": preference_matches,
            "average_rating": round(average_rating, 2),
            "recommendation_score": round(final_score, 2),

            "recommendation_mode": recommendation_mode,
            "recommendation_reason": recommendation_reason,
            "is_new_user": is_new_user
        })

    recommendations.sort(
        key=lambda item: item["recommendation_score"],
        reverse=True
    )

    return jsonify(recommendations[:limit]), 200
