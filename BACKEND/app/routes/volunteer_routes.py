from flask import Blueprint, request, jsonify, session
from app.extensions import db
from datetime import datetime, time
import logging

# Import database models
from app.models import (
    VolunteerNeed, 
    VolunteerSignup, 
    UserSkill, 
    VolunteerRequiredSkill, 
    VolunteerAllocation,
    User, 
    Organisation
)

from app.services.volunteer_allocation_service import (
    calculate_skill_score,
    calculate_urgency_score,
    calculate_matching_score,
    allocate_volunteers,
    get_volunteer_allocation_status,
    update_allocation_status
)
logger = logging.getLogger(__name__)

volunteer_bp = Blueprint("volunteer_bp", __name__)

#-----------------------------------------------------------------------------------------------------------------------------------------
################# VOLUNTEER NEED ENDPOINT #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

@volunteer_bp.route("/needs", methods=["GET"])
def list_volunteer_needs():

    charity_id = request.args.get('organisation_id')
    
    if charity_id:
        # Filter needs if we need to get the needs of one specific charrity
        # useful for admin
        needs = VolunteerNeed.query.filter_by(
            organisation_id=charity_id
        ).order_by(VolunteerNeed.created_at.desc()).all()
    else:
        # Get all needs by newest added

        needs = VolunteerNeed.query.order_by(VolunteerNeed.created_at.desc()).all()
    
    return jsonify([need.to_dict() for need in needs])

#-----------------------------------------------------------------------------------------------------------------------------------------
################# VOLUNTEER NEED ENDPOINT #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------
################# GENERAL USER SIGNS UP FOR A VOLUNTEER NEED #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

@volunteer_bp.route("/needs/<int:volunteer_need_id>/signup", methods=["POST"])
def signup_for_volunteer_need(volunteer_need_id):

    #Is done by the general user

    # Get user_id 
    data = request.get_json() or {}
    user_id = data.get("user_id") or session.get("user_id")
    
    # Validate that the user ID was entered
    if not user_id:
        return jsonify({"message": "User ID required."}), 400
    
    # Check if the volunteer need exists and its availability
    need = VolunteerNeed.query.get(volunteer_need_id)
    if not need:
        return jsonify({"message": "Volunteer need not found."}), 404
    
    if need.status != "open":
        return jsonify({"message": "This volunteer opportunity is no longer open."}), 400
    
    # Check if the user has already signed up for this need
    existing = VolunteerSignup.query.filter_by(
        volunteer_need_id=volunteer_need_id,
        user_id=user_id
    ).first()
    
    if existing:
        return jsonify({"message": "You have already signed up."}), 400

    # Create a new signup record
    signup = VolunteerSignup(
        volunteer_need_id=volunteer_need_id,
        user_id=user_id,
        status="pending"  # New signups start as 'pending'
    )

    # Save to database
    db.session.add(signup)
    db.session.commit()

    return jsonify({
        "message": "Volunteer sign-up recorded successfully.",
        "signup": signup.to_dict()
    }), 201

#-----------------------------------------------------------------------------------------------------------------------------------------
################# GENERAL USER SIGNS UP FOR A VOLUNTEER NEED #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------
################# GET ALL VOLUNTEER SIGNUPS OF A SPECIFIC USER #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------


@volunteer_bp.route("/user/<int:user_id>/signups", methods=["GET"])
def get_user_volunteer_signups(user_id):

    #Lists all the volunteer signups of a specific general user

    # Get all signups for the user
    signups = VolunteerSignup.query.filter_by(user_id=user_id).all()
    result = []
    
    for signup in signups:
        
        need = VolunteerNeed.query.get(signup.volunteer_need_id)
        
        org = Organisation.query.get(need.organisation_id) if need else None
        
        result.append({
            "signup_id": signup.signup_id,
            "volunteer_need": need.to_dict() if need else None,
            "organisation": org.to_dict() if org else None,
            "status": signup.status,
            "signed_up_at": signup.signed_up_at.isoformat() if signup.signed_up_at else None
        })
    
    return jsonify(result)

#-----------------------------------------------------------------------------------------------------------------------------------------
################# GET ALL VOLUNTEER SIGN UPS OF A SPECIFIC USER ENDPOINT #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------
################# ALLOCATE VOLUNTEERS #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

@volunteer_bp.route("/needs/<int:volunteer_need_id>/allocate", methods=["POST"])
def allocate_volunteers_endpoint(volunteer_need_id):

    #does the actuall allocation of volunteers

    data = request.get_json() or {}
    #get the matching score weights 
    weights = data.get("weights")
    
    # Call the main allocation function 
    result = allocate_volunteers(volunteer_need_id, weights)
    
    # Check if the allocation failed
    if result.get("recommended_volunteers") is None:
        return jsonify({"message": result["message"]}), 404
    
    # Return allocation results
    return jsonify(result), 200

#-----------------------------------------------------------------------------------------------------------------------------------------
################# ALLOCATE VOLUNTEERS #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------
################# VOLUNTEER ALLOCATION STATUS #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------


@volunteer_bp.route("/allocations/<int:allocation_id>/status", methods=["PUT"])
def update_allocation_status_endpoint(allocation_id):

    ##updates the status of the volunteer allocation

    # Get the new status from the request
    data = request.get_json() or {}
    new_status = data.get("status")
    
    # Validate that a status was provided
    if not new_status:
        return jsonify({"message": "Status is required."}), 400
    
    allowed_statuses = ["recommended", "accepted", "declined", "confirmed"]
    if new_status not in allowed_statuses:
        return jsonify({
            "message": f"Invalid status. Allowed: {', '.join(allowed_statuses)}"
        }), 400
    
    # Updates the allocation status
    result = update_allocation_status(allocation_id, new_status)
    
    # Checks if the allocation was found
    if "not found" in result["message"]:
        return jsonify(result), 404
    
    return jsonify(result), 200

#-----------------------------------------------------------------------------------------------------------------------------------------
################# VOLUNTEER ALLOCATION STATUS #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

####----------was there before

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
