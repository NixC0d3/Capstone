from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import EngagementLog


engagement_bp = Blueprint("engagement_bp", __name__)


ALLOWED_ENGAGEMENT_TYPES = {
    "profile_view",
    "save",
    "message",
    "rating",
    "volunteer_signup"
}


@engagement_bp.route("/log", methods=["POST"])
def log_engagement():
    data = request.get_json() or {}

    organisation_id = data.get("organisation_id")
    user_id = data.get("user_id")
    engagement_type = data.get("engagement_type")

    if not organisation_id:
        return jsonify(error="organisation_id is required"), 400

    if not user_id:
        return jsonify(error="user_id is required"), 400

    if engagement_type not in ALLOWED_ENGAGEMENT_TYPES:
        return jsonify(error="Invalid engagement type"), 400

    engagement = EngagementLog(
        organisation_id=organisation_id,
        user_id=user_id,
        engagement_type=engagement_type
    )

    db.session.add(engagement)
    db.session.commit()

    return jsonify(
        message="Engagement logged successfully",
        engagement={
            "organisation_id": organisation_id,
            "user_id": user_id,
            "engagement_type": engagement_type
        }
    ), 201
