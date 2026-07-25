from flask import Blueprint, request, jsonify
import psycopg2


engagement_bp = Blueprint("engagement", __name__)


DB_NAME = "capstone"
DB_USER = "postgres"
DB_PASSWORD = "your_password_here"
DB_HOST = "localhost"
DB_PORT = "5432"


ALLOWED_ENGAGEMENT_TYPES = {
    "profile_view",
    "save",
    "message",
    "rating",
    "volunteer_signup"
}


def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


@engagement_bp.route("/engagement/log", methods=["POST"])
def log_engagement():
    data = request.get_json()

    organisation_id = data.get("organisation_id")
    user_id = data.get("user_id")
    engagement_type = data.get("engagement_type")

    if engagement_type not in ALLOWED_ENGAGEMENT_TYPES:
        return jsonify({"error": "Invalid engagement type"}), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO engagement_logs
        (
            organisation_id,
            user_id,
            engagement_type,
            created_at
        )
        VALUES
        (
            %s, %s, %s, CURRENT_TIMESTAMP
        );
        """,
        (organisation_id, user_id, engagement_type)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Engagement logged successfully"}), 201
