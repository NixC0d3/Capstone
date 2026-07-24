from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User, UserPreference, UserSkill, Category

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    first_name = data.get("first_name", "").strip()
    last_name = data.get("last_name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not first_name or not last_name or not email or not password:
        return jsonify(error="Missing required fields"), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify(error="An account with this email already exists"), 400

    # The Vue wizard may send role_id directly.
    role_id = data.get("role_id")

    # If role_id is not sent, use userType from the wizard.
    if not role_id:
        user_type = data.get("userType", "Community Member")

        role_name = "general_user"

        if user_type == "Business Owner":
            role_name = "business_user"
        elif user_type == "Charity Representative":
            role_name = "charity_user"

        role = Role.query.filter_by(role_name=role_name).first()

        if not role:
            return jsonify(error=f"Role not found: {role_name}"), 400

        role_id = role.role_id

    user = User(
        role_id=role_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=password
    )

    db.session.add(user)
    db.session.flush()

    # ---------------------------------
    # Save preferences/interests
    # ---------------------------------
    preferences = data.get("preferences", [])

    # If preferences was not sent, build it from businessInterests and charityInterests.
    if not preferences:
        business_interests = data.get("businessInterests", [])
        charity_interests = data.get("charityInterests", [])

        for item in business_interests:
            if isinstance(item, dict) and "id" in item:
                preferences.append(item["id"])
            else:
                preferences.append(item)

        for item in charity_interests:
            if isinstance(item, dict) and "id" in item:
                preferences.append(item["id"])
            else:
                preferences.append(item)

    for category_id in preferences:
        preference = UserPreference(
            user_id=user.user_id,
            category_id=int(category_id),
            preference_weight=1.0
        )

        db.session.add(preference)

    # ---------------------------------
    # Save volunteer skills
    # ---------------------------------
    skills = data.get("skills", [])

    for skill in skills:
        user_skill = UserSkill(
            user_id=user.user_id,
            skill_name=skill
        )

        db.session.add(user_skill)

    db.session.commit()

    return jsonify(
        message="User registered successfully",
        user=user.to_dict()
    ), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    login_value = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    user = User.query.filter(
        db.func.lower(User.email) == login_value
    ).first()

    # Allows imported demo usernames like gen10, bus1000, char2000
    if not user and "@" not in login_value:
        user = User.query.filter(
            User.email.ilike(f"{login_value}%@civilinfohub.test")
        ).first()

    if not user:
        return jsonify(error="Invalid email or password"), 401

    # Imported Excel users have plain passwords like pass10.
    # New users may later use hashed passwords.
    if user.password_hash != password:
        return jsonify(error="Invalid email or password"), 401

    return jsonify(
        message="Login successful",
        user=user.to_dict()
    ), 200
