from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import (
    User,
    UserSkill,
    UserPreference,
    Category
)

user_bp = Blueprint("user", __name__)


# -----------------------------
# Get user profile
# -----------------------------
@user_bp.route("/<int:user_id>/profile", methods=["GET"])
def get_user_profile(user_id):

    user = User.query.get_or_404(user_id)

    preferences = (
        db.session.query(
            Category.category_id,
            Category.category_name
        )
        .join(
            UserPreference,
            Category.category_id == UserPreference.category_id
        )
        .filter(
            UserPreference.user_id == user_id
        )
        .all()
    )

    skills = UserSkill.query.filter_by(
        user_id=user_id
    ).all()


    return jsonify({

        "user_id": user.user_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "display_name": user.display_name,
        "email": user.email,
        "role_id": user.role_id,
        "location_id": user.location_id,

        "preferences": [
            {
                "category_id": p.category_id,
                "category_name": p.category_name
            }
            for p in preferences
        ],

        "skills": [
            s.skill_name
            for s in skills
        ]
    })

# -----------------------------
# Update basic profile
# -----------------------------
@user_bp.route("/<int:user_id>/profile", methods=["PUT"])
def update_profile(user_id):

    user = User.query.get_or_404(user_id)

    data = request.get_json() or {}

    user.first_name = data.get(
        "first_name",
        user.first_name
    )

    user.last_name = data.get(
        "last_name",
        user.last_name
    )

    user.display_name = data.get(
        "display_name",
        user.display_name
    )

    user.location_id = data.get(
        "location_id",
        user.location_id
    )


    db.session.commit()


    return jsonify({
        "message": "Profile updated"
    })


# -----------------------------
# Get all available skills
# -----------------------------
@user_bp.route("/skills", methods=["GET"])
def get_skills():

    skills = (
        db.session.query(UserSkill.skill_name)
        .distinct()
        .all()
    )

    return jsonify([
        skill.skill_name
        for skill in skills
    ])


# -----------------------------
# Replace user skills
# -----------------------------
@user_bp.route("/<int:user_id>/skills", methods=["PUT"])
def update_skills(user_id):

    data = request.get_json() or {}

    skills = data.get(
        "skills",
        []
    )


    # remove old skills
    UserSkill.query.filter_by(
        user_id=user_id
    ).delete()


    # add selected skills
    for skill in skills:

        new_skill = UserSkill(
            user_id=user_id,
            skill_name=skill
        )

        db.session.add(new_skill)


    db.session.commit()


    return jsonify({
        "message":"Skills updated",
        "skills":skills
    })


# -----------------------------
# Get available interests/categories
# -----------------------------
@user_bp.route("/interests", methods=["GET"])
def get_interests():

    categories = Category.query.all()


    return jsonify([
        {
            "category_id": category.category_id,
            "category_name": category.category_name
        }
        for category in categories
    ])



# -----------------------------
# Replace user interests
# -----------------------------
@user_bp.route("/<int:user_id>/interests", methods=["PUT"])
def update_interests(user_id):

    data = request.get_json() or {}

    category_ids = data.get(
        "categories",
        []
    )


    # remove existing preferences
    UserPreference.query.filter_by(
        user_id=user_id
    ).delete()



    # add selected preferences
    for category_id in category_ids:

        preference = UserPreference(
            user_id=user_id,
            category_id=category_id
        )

        db.session.add(preference)


    db.session.commit()


    return jsonify({
        "message":"Interests updated",
        "categories":category_ids
    })