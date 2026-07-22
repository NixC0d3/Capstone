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
