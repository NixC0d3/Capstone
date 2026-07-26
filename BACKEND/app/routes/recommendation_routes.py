from flask import Blueprint, request, jsonify
from sqlalchemy import text
from app.extensions import db


recommendation_bp = Blueprint("recommendation_bp", __name__)


@recommendation_bp.route("/user/<int:user_id>", methods=["GET"])
def recommend_for_user(user_id):
    """
    Recommends organisations for a user.

    Uses:
    - engagement_logs: views, saves, messages, ratings, volunteer signups
    - user_preferences: categories selected during signup
    - ratings_reviews: average rating
    """

    organisation_type = request.args.get("type", "").strip().lower()
    limit = request.args.get("limit", 6, type=int)

    sql = text("""
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

            COALESCE((
                SELECT SUM(
                    CASE
                        WHEN e.engagement_type = 'profile_view' THEN 1
                        WHEN e.engagement_type = 'save' THEN 3
                        WHEN e.engagement_type = 'message' THEN 4
                        WHEN e.engagement_type = 'rating' THEN 5
                        WHEN e.engagement_type = 'volunteer_signup' THEN 5
                        ELSE 0
                    END
                )
                FROM engagement_logs e
                WHERE e.organisation_id = o.organisation_id
            ), 0) AS engagement_score,

            COALESCE((
                SELECT SUM(COALESCE(up.preference_weight, 1) * 10)
                FROM user_preferences up
                LEFT JOIN organisation_categories oc
                    ON oc.category_id = up.category_id
                WHERE up.user_id = :user_id
                  AND (
                        up.category_id = o.category_id
                        OR oc.organisation_id = o.organisation_id
                  )
            ), 0) AS preference_score,

            COALESCE((
                SELECT AVG(rr.rating)
                FROM ratings_reviews rr
                WHERE rr.organisation_id = o.organisation_id
            ), 0) AS average_rating,

            (
                COALESCE((
                    SELECT SUM(
                        CASE
                            WHEN e.engagement_type = 'profile_view' THEN 1
                            WHEN e.engagement_type = 'save' THEN 3
                            WHEN e.engagement_type = 'message' THEN 4
                            WHEN e.engagement_type = 'rating' THEN 5
                            WHEN e.engagement_type = 'volunteer_signup' THEN 5
                            ELSE 0
                        END
                    )
                    FROM engagement_logs e
                    WHERE e.organisation_id = o.organisation_id
                ), 0)

                +

                COALESCE((
                    SELECT SUM(COALESCE(up.preference_weight, 1) * 10)
                    FROM user_preferences up
                    LEFT JOIN organisation_categories oc
                        ON oc.category_id = up.category_id
                    WHERE up.user_id = :user_id
                      AND (
                            up.category_id = o.category_id
                            OR oc.organisation_id = o.organisation_id
                      )
                ), 0)

                +

                COALESCE((
                    SELECT AVG(rr.rating) * 2
                    FROM ratings_reviews rr
                    WHERE rr.organisation_id = o.organisation_id
                ), 0)
            ) AS recommendation_score

        FROM organisations o
        LEFT JOIN locations l
            ON l.location_id = o.location_id
        LEFT JOIN categories c
            ON c.category_id = o.category_id

        WHERE
            (:organisation_type = '' OR LOWER(o.organisation_type) = :organisation_type)

        ORDER BY
            recommendation_score DESC,
            engagement_score DESC,
            average_rating DESC,
            o.organisation_name ASC

        LIMIT :limit;
    """)

    result = db.session.execute(
        sql,
        {
            "user_id": user_id,
            "organisation_type": organisation_type,
            "limit": limit
        }
    )

    recommendations = []

    for row in result:
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
            "engagement_score": float(row.engagement_score or 0),
            "preference_score": float(row.preference_score or 0),
            "average_rating": float(row.average_rating or 0),
            "recommendation_score": float(row.recommendation_score or 0)
        })

    return jsonify(recommendations), 200
