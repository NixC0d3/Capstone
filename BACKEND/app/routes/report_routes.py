from flask import Blueprint, request, jsonify
from app.services.trend_score_service import (
    calculate_average_rating,
    calculate_bayesian_rating,
    calculate_engagement_score,
    calculate_trend_score,
    calculate_growth_rate,
    classify_trend_status,
)

report_bp = Blueprint("report_bp", __name__)

@report_bp.route("/trend-score", methods=["POST"])
def calculate_report_demo():
    data = request.get_json() or {}

    total_reviews = data.get("total_reviews", 0)
    total_rating_score = data.get("total_rating_score", 0)
    global_average_rating = data.get("global_average_rating", 0)
    previous_trend_score = data.get("previous_trend_score", 0)

    average_rating = calculate_average_rating(total_rating_score, total_reviews)
    bayesian_rating = calculate_bayesian_rating(
        average_rating,
        total_reviews,
        global_average_rating,
        data.get("minimum_expected_reviews", 5)
    )

    engagement_score = calculate_engagement_score(data.get("engagement_counts", {}))
    trend_score = calculate_trend_score(engagement_score, bayesian_rating)
    growth_rate = calculate_growth_rate(trend_score, previous_trend_score)
    status = classify_trend_status(growth_rate)

    return jsonify(
        average_rating=average_rating,
        bayesian_rating=bayesian_rating,
        engagement_score=engagement_score,
        trend_score=trend_score,
        growth_rate=growth_rate,
        trend_status=status
    )
