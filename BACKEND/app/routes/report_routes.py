from flask import Blueprint, request, jsonify
from app.services.trend_score_service import (
    calculate_average_rating,
    calculate_bayesian_rating,
    calculate_engagement_score,
    calculate_trend_score,
    calculate_growth_rate,
    classify_trend_status,
)
from app.models import MonthlyBusinessReport

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

@report_bp.route("/organisation/<int:organisation_id>", methods=["GET"])
def get_organisation_report(organisation_id):

    month = request.args.get("month")
    year = request.args.get("year")

    report = MonthlyBusinessReport.query.filter_by(
        organisation_id=organisation_id,
        report_month=month,
        report_year=year
    ).first()


    if not report:
        return jsonify({
            "error":"Report not found"
        }),404


    return jsonify({
        "month": month,
        "year": year,
        "trend_score": report.trend_score,
        "growth_rate": report.growth_rate,
        "trend_status": report.trend_status,

        "bayesian_rating": report.bayesian_rating,
        "total_reviews": report.total_reviews,

        "profile_views": report.total_views,
        "saves": report.total_saves,
        "messages": report.total_messages,

        #when its added to the table then change this
        #"volunteer_signups": report.volunteer_signups
        "volunteer_signups": 0
    })