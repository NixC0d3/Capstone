from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import VolunteerNeed, VolunteerSignup, UserSkill
from app.services.volunteer_allocation_service import (
    calculate_skill_score,
    calculate_urgency_score,
    calculate_matching_score,
)

volunteer_bp = Blueprint("volunteer_bp", __name__)

@volunteer_bp.route("/needs", methods=["GET"])
def list_volunteer_needs():
    needs = VolunteerNeed.query.order_by(VolunteerNeed.created_at.desc()).all()
    return jsonify([need.to_dict() for need in needs])

@volunteer_bp.route("/needs", methods=["POST"])
def create_volunteer_need():
    data = request.get_json() or {}

    need = VolunteerNeed(
        organisation_id=data.get("organisation_id"),
        title=data.get("title", ""),
        description=data.get("description"),
        urgency_level=data.get("urgency_level", "medium"),
        volunteers_needed=data.get("volunteers_needed", 1)
    )

    db.session.add(need)
    db.session.commit()

    return jsonify(message="Volunteer need created", volunteer_need=need.to_dict()), 201

@volunteer_bp.route("/needs/<int:volunteer_need_id>/signup", methods=["POST"])
def signup_for_volunteer_need(volunteer_need_id):
    data = request.get_json() or {}

    signup = VolunteerSignup(
        volunteer_need_id=volunteer_need_id,
        user_id=data.get("user_id"),
        status="pending"
    )

    db.session.add(signup)
    db.session.commit()

    return jsonify(message="Volunteer sign-up recorded", signup=signup.to_dict()), 201

@volunteer_bp.route("/match-score", methods=["POST"])
def demo_match_score():
    data = request.get_json() or {}

    skill_score = calculate_skill_score(
        data.get("required_skills", []),
        data.get("user_skills", [])
    )
    urgency_score = calculate_urgency_score(data.get("urgency_level", "medium"))
    availability_score = data.get("availability_score", 0)

    matching_score = calculate_matching_score(skill_score, availability_score, urgency_score)

    return jsonify(
        skill_score=skill_score,
        availability_score=availability_score,
        urgency_score=urgency_score,
        matching_score=matching_score
    )
