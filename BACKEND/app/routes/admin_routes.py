from flask import Blueprint, request, jsonify
from app.models import User

admin_bp = Blueprint("admin_bp", __name__)

# Starter in-memory settings.
# Later, store these in a database table so admins can update them permanently.
ENGAGEMENT_WEIGHT_SETTINGS = {
    "view_weight": 1,
    "save_weight": 3,
    "message_weight": 4,
    "rating_action_weight": 5,
    "volunteer_signup_weight": 5,
    "improving_threshold": 5,
    "declining_threshold": -5,
}

@admin_bp.route("/engagement-weights", methods=["GET"])
def get_engagement_weights():
    return jsonify(ENGAGEMENT_WEIGHT_SETTINGS)

@admin_bp.route("/engagement-weights", methods=["PUT"])
def update_engagement_weights():
    data = request.get_json() or {}
    ENGAGEMENT_WEIGHT_SETTINGS.update(data)
    return jsonify(message="Engagement weights updated", settings=ENGAGEMENT_WEIGHT_SETTINGS)

@admin_bp.route("/users", methods=["GET"])
def get_users():

    users = User.query.all()

    return jsonify([
        {
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role.role_name if user.role else None
        }
        for user in users
    ])