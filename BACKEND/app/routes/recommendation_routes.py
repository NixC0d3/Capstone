from flask import Blueprint, request, jsonify
from sqlalchemy import text
from app.extensions import db

import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler


recommendation_bp = Blueprint("recommendation_bp", __name__)


STRONG_ENGAGEMENT_TYPES = (
    "save",
    "message",
    "rating",
    "review",
    "volunteer_signup",
)


def get_user_strong_engagement_count(user_id):
    """
    Counts meaningful engagement only.

    Profile views are intentionally excluded because they happen while browsing.
    A new user should not stop receiving signup-interest recommendations just
    because they clicked a few cards.
    """

    row = db.session.execute(
        text("""
            SELECT
                (
                    SELECT COUNT(*)
                    FROM engagement_logs
                    WHERE user_id = :user_id
                      AND engagement_type IN (
                          'save',
                          'message',
                          'rating',
                          'review',
                          'volunteer_signup'
                      )
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
    then uses TruncatedSVD matrix factorization to predict organisations the
    user may like.

    This is useful only after there is enough user activity. For new users,
    this returns an empty dictionary and the route uses signup interests.
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

    strong_engagement_count = get_user_strong_engagement_count(user_id)
    user_preference_count = get_user_preference_count(user_id)

    # Cold start means the user has signup interests but has not done strong
    # actions like saving, messaging, rating, or reviewing yet.
    cold_start = user_preference_count > 0 and strong_engagement_count == 0

    # ML recommendations can be noisy for a brand-new user, so use them only
    # after the user has enough meaningful interaction history.
    ml_scores = get_ml_scores(user_id) if strong_engagement_count >= 3 else {}

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
                up.category_id,
                COALESCE(up.preference_weight, 1) AS preference_weight,
                c.category_name
            FROM user_preferences up
            JOIN categories c
                ON c.category_id = up.category_id
            WHERE up.user_id = :user_id
        ),

        preferences AS (
            SELECT
                ocm.organisation_id,
                SUM(ups.preference_weight * 100) AS preference_score,
                COUNT(*) AS preference_matches,
                STRING_AGG(DISTINCT ups.category_name, ', ' ORDER BY ups.category_name) AS matched_categories
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
                        WHEN e.engagement_type = 'profile_view' THEN 0.5
                        WHEN e.engagement_type = 'save' THEN 4
                        WHEN e.engagement_type = 'message' THEN 5
                        WHEN e.engagement_type = 'rating' THEN 6
                        WHEN e.engagement_type = 'review' THEN 7
                        WHEN e.engagement_type = 'volunteer_signup' THEN 6
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

            COALESCE(
                preferences.matched_categories,
                primary_category.category_name,
                display_categories.category_name
            ) AS category_name,

            COALESCE(preferences.matched_categories, '') AS matched_categories,
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

    # Behaviour influence grows gradually as the user performs strong actions.
    # 0 strong actions = signup interests dominate.
    # 10+ strong actions = behaviour has much more influence.
    behavior_factor = min(strong_engagement_count / 10, 1)
    preference_weight = 0.75 - (0.30 * behavior_factor)
    behavior_weight = 0.10 + (0.35 * behavior_factor)
    ml_weight = 0.00 if strong_engagement_count < 3 else 0.10

    for row in result:
        ml_score = ml_scores.get(row.organisation_id, 0)

        engagement_score = float(row.engagement_score or 0)
        preference_score = float(row.preference_score or 0)
        preference_matches = int(row.preference_matches or 0)
        behavior_score = float(row.behavior_score or 0)
        average_rating = float(row.average_rating or 0)
        
        review_count = int(row.review_count or 0)

        if review_count > 0:
          rating_text = f"{round(average_rating, 1)}/5 ({review_count})"
        else:
          rating_text = None

        if cold_start:
            # Strong guarantee for new users:
            # matching signup interests must appear above unrelated organisations.
            if preference_matches > 0:
                final_score = (
                    10000
                    + preference_score
                    + (average_rating * 2)
                    + (engagement_score * 0.01)
                )
            else:
                final_score = (
                    (average_rating * 2)
                    + (engagement_score * 0.01)
                )

            recommendation_mode = "signup_interests"

        elif user_preference_count > 0:
            # Returning-user logic:
            # Signup interests still matter, but behaviour gradually becomes stronger.
            final_score = (
                (preference_score * preference_weight)
                + (behavior_score * behavior_weight)
                + (ml_score * ml_weight)
                + (engagement_score * 0.03)
                + (average_rating * 2)
            )

            recommendation_mode = "behaviour_and_interests"

        else:
            # Fallback for users with no preferences and no useful behaviour.
            final_score = (
                (behavior_score * 0.45)
                + (ml_score * 0.10)
                + (engagement_score * 0.20)
                + (average_rating * 5)
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
            "matched_categories": row.matched_categories,

            "ml_score": round(ml_score, 2),
            "behavior_score": round(behavior_score, 2),
            "engagement_score": round(engagement_score, 2),
            "preference_score": round(preference_score, 2),
            "preference_matches": preference_matches,
            "recommendation_score": round(final_score, 2),
            
            "average_rating": round(average_rating, 1),
            "review_count": review_count,
            "rating": rating_text,

            "recommendation_mode": recommendation_mode,
            "recommendation_reason": recommendation_reason,
            "is_new_user": cold_start,
            "strong_engagement_count": strong_engagement_count
        })

    recommendations.sort(
        key=lambda item: (
            item["preference_matches"],
            item["recommendation_score"]
        ),
        reverse=True
    )

    return jsonify(recommendations[:limit]), 200
