from flask import Blueprint, request, jsonify
from app.models import User, UserModeration, Organisation, RatingReview, Message, SavedOrganisation, Role
from app.extensions import db

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
    status = request.args.get("status")

    query = (User.query.join(Role).filter(Role.role_name == "general_user"))

    if status == "active":
        query = query.filter(
            (User.account_status == "active") |
            (User.account_status.is_(None))
        )
    elif status and status != "all":
        query = query.filter(
            User.account_status == status
        )
        
    users = query.all()

    return jsonify([
        {
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role_id": user.role_id,
            "role": user.role.role_name if user.role else None,
            "status": user.account_status
        }
        for user in users
    ])

@admin_bp.route("/users/<int:user_id>/review", methods=["POST"])
def review_user(user_id):

    data = request.get_json()
    user = User.query.get_or_404(user_id)
    reason = data.get("reason")
    
    allowed = ["inappropriate", "spam", "suspicious"]
    if reason not in allowed:
        return jsonify(
            error="Invalid moderation reason"
        ),400
    user.account_status = reason

    moderation = UserModeration(
        user_id=user_id,
        reason=data.get("reason"),
        notes=data.get("notes")
    )

    db.session.add(moderation)
    db.session.commit()

    return jsonify(message="User reviewed", status=reason)

@admin_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_details(user_id):
    user = User.query.get_or_404(user_id)

    organisation_count = Organisation.query.filter_by(owner_user_id=user_id).count()
    review_count = RatingReview.query.filter_by(user_id=user_id).count()
    message_count = Message.query.filter_by(sender_user_id=user_id).count()
    saved_count = SavedOrganisation.query.filter_by(user_id=user_id).count()

    return jsonify({
        "user": {
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role.role_name if user.role else None,
            "status": user.account_status,
            "created_at": user.created_at
        },

        "activity": {
            "organisations": organisation_count,
            "reviews": review_count,
            "messages": message_count,
            "saved": saved_count
        },
        "moderation_history": [
            {
                "reason": m.reason,
                "notes": m.notes,
                "date": m.created_at
            }
            for m in user.moderation_records
        ]
    })

@admin_bp.route("/organisations", methods=["GET"])
def getAdminOrganisations():
    organisations = Organisation.query.all()

    return jsonify([
        {
            "organisation_id": org.organisation_id,
            "organisation_name": org.organisation_name,
            "owner": f"{org.owner.first_name} {org.owner.last_name}",
            "organisation_type": org.organisation_type,
            "created_by": org.owner.role.role_name
        }
        for org in organisations
    ])