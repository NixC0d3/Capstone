DEFAULT_ENGAGEMENT_WEIGHTS = {
    "view_weight": 1,
    "save_weight": 3,
    "message_weight": 4,
    "rating_action_weight": 5,
    "volunteer_signup_weight": 5,
}

DEFAULT_TREND_SETTINGS = {
    "engagement_component_weight": 0.70,
    "rating_component_weight": 0.30,
    "improving_threshold": 5,
    "declining_threshold": -5,
    "minimum_expected_reviews": 5,
}

def calculate_average_rating(total_rating_score, total_reviews):
    if total_reviews == 0:
        return 0
    return total_rating_score / total_reviews

def calculate_bayesian_rating(average_rating, review_count, global_average_rating, minimum_expected_reviews=5):
    # Bayesian rating balances one organisation's rating with the platform-wide average.
    v = review_count
    m = minimum_expected_reviews
    R = average_rating
    C = global_average_rating

    if v + m == 0:
        return 0

    return ((v / (v + m)) * R) + ((m / (v + m)) * C)

def calculate_engagement_score(counts, weights=None):
    weights = weights or DEFAULT_ENGAGEMENT_WEIGHTS

    return (
        counts.get("profile_views", 0) * weights.get("view_weight", 1)
        + counts.get("saves", 0) * weights.get("save_weight", 3)
        + counts.get("messages", 0) * weights.get("message_weight", 4)
        + counts.get("ratings", 0) * weights.get("rating_action_weight", 5)
        + counts.get("volunteer_signups", 0) * weights.get("volunteer_signup_weight", 5)
    )

def convert_rating_to_score(bayesian_rating):
    # Converts a rating out of 5 into a score out of 100.
    return (bayesian_rating / 5) * 100

def calculate_trend_score(engagement_score, bayesian_rating, settings=None):
    settings = settings or DEFAULT_TREND_SETTINGS
    rating_score = convert_rating_to_score(bayesian_rating)

    return (
        engagement_score * settings.get("engagement_component_weight", 0.70)
        + rating_score * settings.get("rating_component_weight", 0.30)
    )

def calculate_growth_rate(current_score, previous_score):
    if previous_score == 0:
        return 0
    return ((current_score - previous_score) / previous_score) * 100

def classify_trend_status(growth_rate, settings=None):
    settings = settings or DEFAULT_TREND_SETTINGS

    if growth_rate > settings.get("improving_threshold", 5):
        return "Improving"
    if growth_rate < settings.get("declining_threshold", -5):
        return "Declining"
    return "Stable"
