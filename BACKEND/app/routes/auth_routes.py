from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User, Role, UserPreference, UserSkill, Category

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

    role_id = data.get("role_id")

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

    try:
        user = User(
            role_id=role_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password
        )

        db.session.add(user)
        db.session.flush()

        frontend_category_map = {
            1: "Restaurant",
            2: "Retail",
            3: "Health",
            4: "Beauty",
            5: "Arts and Crafts",
            6: "HomeCenter",
            7: "Repair",
            8: "Tech",
            9: "Dealership and Parts",
            10: "Construction",
            11: "Excursion",
            12: "Farming",
            13: "Marketing",
            14: "Education",
            15: "Social Safety Net Programmes",
            16: "Food Drives",
            17: "Climate Change",
            18: None,
            19: "Social Safety Net Programmes",
            20: "Arts",
            21: "Clean Up",
            22: "Health Services",
            23: "Homeless Aid",
            24: "Faith-Based"
        }

        frontend_name_map = {
            "Food / Restaurants": "Restaurant",
            "Retail / Clothing": "Retail",
            "Health & Wellness": "Health",
            "Beauty & Personal Care": "Beauty",
            "Arts & Crafts": "Arts and Crafts",
            "Home & Garden": "HomeCenter",
            "Professional Services": "Repair",
            "Technology Services": "Tech",
            "Automotive": "Dealership and Parts",
            "Construction": "Construction",
            "Entertainment": "Excursion",
            "Agriculture": "Farming",
            "Marketing & Design": "Marketing",
            "Education & Youth Development": "Education",
            "Poverty Alleviation": "Social Safety Net Programmes",
            "Food Security": "Food Drives",
            "Environmental Conservation": "Climate Change",
            "Animal Welfare": None,
            "Community Development": "Social Safety Net Programmes",
            "Arts & Culture": "Arts",
            "Disaster Relief": "Clean Up",
            "Elderly Care": "Health Services",
            "Homeless Support": "Homeless Aid",
            "Faith-Based Initiatives": "Faith-Based"
        }

        selected_category_names = []

        business_interests = data.get("businessInterests", [])
        charity_interests = data.get("charityInterests", [])
        preferences = data.get("preferences", [])

        all_interests = business_interests + charity_interests

        for item in all_interests:
            database_name = None

            if isinstance(item, dict):
                frontend_id = item.get("id")
                frontend_name = item.get("name", "").strip()

                if frontend_id:
                    database_name = frontend_category_map.get(int(frontend_id))

                if not database_name and frontend_name:
                    database_name = frontend_name_map.get(frontend_name, frontend_name)

            elif isinstance(item, int):
                database_name = frontend_category_map.get(item)

            elif isinstance(item, str):
                database_name = frontend_name_map.get(item, item)

            if database_name:
                selected_category_names.append(database_name)

        for frontend_id in preferences:
            try:
                database_name = frontend_category_map.get(int(frontend_id))

                if database_name:
                    selected_category_names.append(database_name)

            except ValueError:
                pass

        selected_category_names = list(set(selected_category_names))

        for category_name in selected_category_names:
            category = Category.query.filter_by(
                category_name=category_name
            ).first()

            if category:
                preference = UserPreference(
                    user_id=user.user_id,
                    category_id=category.category_id,
                    preference_weight=1.0
                )

                db.session.add(preference)

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

    except Exception as error:
        db.session.rollback()
        return jsonify(error=str(error)), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    login_value = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    user = User.query.filter(
        db.func.lower(User.email) == login_value
    ).first()

    if not user and "@" not in login_value:
        user = User.query.filter(
            User.email.ilike(f"{login_value}%@civilinfohub.test")
        ).first()

    if not user:
        return jsonify(error="Invalid email or password"), 401

    if user.password_hash != password:
        return jsonify(error="Invalid email or password"), 401

    return jsonify(
        message="Login successful",
        user=user.to_dict()
    ), 200
