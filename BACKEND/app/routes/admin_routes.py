from flask import Blueprint, request, jsonify

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
