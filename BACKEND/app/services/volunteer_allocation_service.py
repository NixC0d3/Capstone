###################ADDED LIBRARIES#####################
from datetime import datetime, time
from app.models import (
    VolunteerNeed, VolunteerRequiredSkill, VolunteerAllocation, 
    User, UserSkill, UserAvailability, Organisation
)
from app.extensions import db
import logging

logger = logging.getLogger(__name__)

###################ADDED LIBRARIES#####################

DEFAULT_MATCHING_WEIGHTS = {
    "skill_weight": 0.50,
    "availability_weight": 0.35,
    "urgency_weight": 0.15,
}

URGENCY_SCORES = {
    "high": 1.0,
    "medium": 0.6,
    "low": 0.3,
}

#-----------------------------------------------------------------------------------------------------------------------------------------
################# CALCULATES SKILL MATCH SCORE #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

def calculate_skill_score(required_skills, user_skills):

    #Does Step 4 in the pseudocode
    required = {skill.lower().strip() for skill in required_skills if skill} #lists of skill names required by the charity
                                                                             #Also get these skills from Melissa because she had some created

    user = {skill.lower().strip() for skill in user_skills if skill} #the skills of the user

    if not required:
        return 0.0

    matched_skills = required.intersection(user)
    return len(matched_skills) / len(required)


def calculate_availability_score(required_start, required_end, user_start, user_end):

    #Does step 5 to calculate the availability score
    # Handles any missing user data
    if not required_start or not required_end or not user_start or not user_end:
        return 0.0
    
    # There needs to be a field regarding when the user is available so as to do the matching
    # Also part of why I imported datetime incase you want to just generate random date and times using faker data as well
    # You'd need the faker library as well

    if isinstance(required_start, time) and isinstance(user_start, time):
        # Full match is when the user is available for the whole required period
        if user_start <= required_start and user_end >= required_end:
            return 1.0
        
        # Partial match is when the user's time overlaps with required time
        if user_start < required_end and user_end > required_start:
            return 0.5
    
    return 0.0
#-----------------------------------------------------------------------------------------------------------------------------------------
################# CALCULATES MATCH SKILL SCORE #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------------------------
################# CALCULATES THE URGENCY LEVEL #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

def calculate_urgency_score(urgency_level):

    #Step 6 of the pseudocode that returns the urgency level as high, medium or low

    return URGENCY_SCORES.get(str(urgency_level).lower(), 0.3)

#-----------------------------------------------------------------------------------------------------------------------------------------
################# CALCULATES THE URGENCY LEVEL #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------------------------
################# CALCULATES THE MATCHING SCORE #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

def calculate_matching_score(skill_score, availability_score, urgency_score, weights=None):

    #step 7 of the pseudocode

    weights = weights or DEFAULT_MATCHING_WEIGHTS

    return (  

        #all variables are floats between 0 and 1

        skill_score * weights.get("skill_weight", 0.50)  
        + availability_score * weights.get("availability_weight", 0.35) 
        + urgency_score * weights.get("urgency_weight", 0.15) 
    )

#-----------------------------------------------------------------------------------------------------------------------------------------
################# CALCULATES THE MATCHING SCORE #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------------------------
################# VOLUNTEER ALLOCATIONS #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

def allocate_volunteers(volunteer_need_id, weights=None):

    #Main function that does all steps

    # Step 1 from pseudocode

    logger.info(f"Step 1: Retrieving volunteer need {volunteer_need_id}")

    #gets selected volunteer needs from the database
    need = VolunteerNeed.query.get(volunteer_need_id)

    #error handling
    if not need:
        return {
            "message": f"Volunteer need {volunteer_need_id} not found.",
            "volunteer_need": None,
            "recommended_volunteers": []
        }
    
    # Get required skills from the volunteer need
    required_skill_objects = VolunteerRequiredSkill.query.filter_by(
        volunteer_need_id=volunteer_need_id
    ).all()
    required_skills = [skill.skill_name for skill in required_skill_objects]
    
    # Get the charity organisation details
    charity = Organisation.query.get(need.organisation_id)
    charity_name = charity.organisation_name if charity else "Unknown Charity"
    
    logger.info(f"  Need: {need.title} (ID: {volunteer_need_id})")
    logger.info(f"  Charity: {charity_name}")
    logger.info(f"  Required skills: {required_skills}")
    logger.info(f"  Date: {need.needed_date}")
    logger.info(f"  Time: {need.start_time} - {need.end_time}")
    logger.info(f"  Urgency: {need.urgency_level}")
    logger.info(f"  Amount Volunteers needed: {need.volunteers_needed}")
    
    #Step 2 from Pseudocode

    logger.info("Step 2: Finding available general users")
    
    available_users = []
    
    if need.needed_date and need.start_time and need.end_time:
        # Find users who have availability records that match the required date and time for the charities/non-profit organisations

        availability_records = UserAvailability.query.filter(
            UserAvailability.available_date == need.needed_date,
            UserAvailability.start_time <= need.start_time,
            UserAvailability.end_time >= need.end_time
        ).all()
        
        user_ids = [record.user_id for record in availability_records]
        
        # Filter only the general users
        general_users = User.query.filter(
            User.user_id.in_(user_ids),
            User.role_id == 1  #this is for the general users
        ).all()
        
        available_users = [user.user_id for user in general_users]
    else:

        # If no specific date/time, get all general users that are listed as wanted to be a volunteer
        #But at the same time that feels like additional computations that aren't necessary so I continued with just using all general users
        #Cause if they send in an availability period then I assume they're willing to be a volunteer anyways

        general_users = User.query.filter_by(role_id=1).all()
        available_users = [user.user_id for user in general_users]
    
    logger.info(f"  Found {len(available_users)} available users")
    
    if not available_users:
        return {
            "message": "No volunteers are available for this opportunity.", #sad concept :(
            "volunteer_need": need.to_dict(),
            "recommended_volunteers": [] #sends a list of recommended volunteers
        }


    #Step 3 from the pseudocode
    
    logger.info("Step 3: Retrieving user skills")
    
    # Get skills for all available users 
    user_skills_map = {}
    all_user_skills = UserSkill.query.filter(
        UserSkill.user_id.in_(available_users)
    ).all()

    for skill in all_user_skills:
        if skill.user_id not in user_skills_map:
            user_skills_map[skill.user_id] = []
        user_skills_map[skill.user_id].append(skill.skill_name)

    #Show steps 4-7 to calculate the different user scores
    
    logger.info("Steps 4-7: Calculating the matching scores")
    
    scored_volunteers = []
    
    for user_id in available_users:
        user_skills = user_skills_map.get(user_id, [])
        
        # Step 4 to calculate skill match score
        skill_score = calculate_skill_score(required_skills, user_skills)
        
        # Step 5 to calculate availability score
        availability_score = calculate_availability_score(
            need.start_time,
            need.end_time,
            None,  #user availability data would be here
            None
        )
        # For simplicity, we'll assume users are fully available

        availability_score = 1.0
        
        # Step 6 calculates the urgency score
        urgency_score = calculate_urgency_score(need.urgency_level)
        
        # Step 7 calculates the final matching score
        matching_score = calculate_matching_score(
            skill_score,
            availability_score,
            urgency_score,
            weights
        )
        
        # Print the user's name or email address 
        user = User.query.get(user_id)
        user_name = f"{user.first_name} {user.last_name}" if user else f"User {user_id}"
        
        scored_volunteers.append({
            "user_id": user_id,
            "user_name": user_name,
            "skill_score": round(skill_score, 3),
            "availability_score": round(availability_score, 3),
            "urgency_score": round(urgency_score, 3),
            "matching_score": round(matching_score, 3),
            "matched_skills": [s for s in user_skills if s.lower() in {r.lower() for r in required_skills}]
        })
        
        logger.info(f"  User {user_id}: skill={skill_score:.2f}, avail={availability_score:.2f}, "
                   f"urgency={urgency_score:.2f}, match={matching_score:.2f}")
    
    # Step 8 sorts all the availabile users from the highest matching score to the lowest matching score

    logger.info("Step 8: Sorting volunteers by matching score")
    
    sorted_volunteers = sorted(
        scored_volunteers,
        key=lambda x: x["matching_score"],
        reverse=True
    )
    
    # Step 9 selects top users

    logger.info(f"Step 9: Selecting top {need.volunteers_needed} volunteers")
    
    selected_volunteers = sorted_volunteers[:need.volunteers_needed]
    
    # Insert records into volunteer allocations
    allocations = []
    for volunteer in selected_volunteers:
        allocation = VolunteerAllocation(
            volunteer_need_id=volunteer_need_id,
            user_id=volunteer["user_id"],
            matching_score=volunteer["matching_score"],
            allocation_status="recommended"
        )
        db.session.add(allocation)
        allocations.append(allocation)
    
    db.session.commit()
    
    logger.info(f"  Created {len(allocations)} allocation records")

    #Final step returns the recommended volunteers to the charity user
    
    logger.info("Step 10: Returning recommendations")
    
    return {
        "message": f"Successfully allocated these volunteers {len(selected_volunteers)}.",
        "volunteer_need": {
            "id": need.volunteer_need_id,
            "title": need.title,
            "charity_name": charity_name,
            "required_skills": required_skills,
            "volunteers_needed": need.volunteers_needed,
            "urgency_level": need.urgency_level,
            "date": need.needed_date.isoformat() if need.needed_date else None,
            "start_time": need.start_time.strftime("%H:%M") if need.start_time else None,
            "end_time": need.end_time.strftime("%H:%M") if need.end_time else None
        },
        "recommended_volunteers": selected_volunteers
    }
#-----------------------------------------------------------------------------------------------------------------------------------------
################# VOLUNTEER ALLOCATIONS #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------------------------
################# ALLOCATION STATUS - Optional #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

def get_volunteer_allocation_status(volunteer_need_id):

    ##gets the status of the volunteer allocations for a specific need
    ##useful for the charity user

    allocations = VolunteerAllocation.query.filter_by(
        volunteer_need_id=volunteer_need_id
    ).all()
    
    return {
        "volunteer_need_id": volunteer_need_id,
        "allocations": [
            {
                "user_id": alloc.user_id,
                "matching_score": alloc.matching_score,
                "status": alloc.allocation_status,
                "allocated_at": alloc.allocated_at.isoformat() if alloc.allocated_at else None
            }
            for alloc in allocations
        ]
    }
#-----------------------------------------------------------------------------------------------------------------------------------------
################# ALLOCATION STATUS #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------------------------
################# UPDATES TO ALLOCATION STATUS #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

def update_allocation_status(allocation_id, new_status):
    
    ##updates the status of the volunteer allocation for general users so they know their current status
    allocation = VolunteerAllocation.query.get(allocation_id)
    if not allocation:
        return {"message": f"Allocation {allocation_id} not found."}
    
    allocation.allocation_status = new_status
    db.session.commit()
    
    return {
        "message": f"Allocation {allocation_id} updated to '{new_status}'.",
        "allocation": allocation.to_dict()
    }

#-----------------------------------------------------------------------------------------------------------------------------------------
################# UPDATES TO ALLOCATION STATUS #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------




###################WAS HERE BEFORE#####################

def calculate_skill_score(required_skills, user_skills):
    required = {skill.lower().strip() for skill in required_skills if skill}
    user = {skill.lower().strip() for skill in user_skills if skill}

    if not required:
        return 0

    matched_skills = required.intersection(user)
    return len(matched_skills) / len(required)

def calculate_availability_score(required_start, required_end, user_start, user_end):
    # Full match: user is available for the whole required period.
    if user_start <= required_start and user_end >= required_end:
        return 1.0

    # Partial match: user's time overlaps with required time.
    if user_start < required_end and user_end > required_start:
        return 0.5

    return 0

def calculate_urgency_score(urgency_level):
    return URGENCY_SCORES.get(str(urgency_level).lower(), 0.3)

def calculate_matching_score(skill_score, availability_score, urgency_score, weights=None):
    weights = weights or DEFAULT_MATCHING_WEIGHTS

    return (
        skill_score * weights.get("skill_weight", 0.50)
        + availability_score * weights.get("availability_weight", 0.35)
        + urgency_score * weights.get("urgency_weight", 0.15)
    )

def rank_volunteers(volunteers):
    # volunteers should be a list of dictionaries containing matching_score.
    return sorted(volunteers, key=lambda item: item.get("matching_score", 0), reverse=True)
