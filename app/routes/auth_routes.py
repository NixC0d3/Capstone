from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    user = User(
        role_id=data.get("role_id"),
        first_name=data.get("first_name", ""),
        last_name=data.get("last_name", ""),
        email=data.get("email", ""),
        password_hash=data.get("password", "")
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(message="User registered successfully", user=user.to_dict()), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(email=data.get("email")).first()

    if not user:
        return jsonify(error="Invalid login details"), 401

    # Replace this with proper password hashing/JWT before final deployment.
    return jsonify(message="Login successful", user=user.to_dict())
