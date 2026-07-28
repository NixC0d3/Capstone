from flask import Blueprint, jsonify
from sqlalchemy import text
from app.extensions import db

report_bp = Blueprint("report_bp", __name__)


@report_bp.route("/business-dashboard/<int:user_id>", methods=["GET"])
def get_business_dashboard_report(user_id):
    # Find the business owned by the logged-in business user
    organisation = db.session.execute(
        text("""
            SELECT
                organisation_id,
                organisation_name
            FROM organisations
            WHERE owner_user_id = :user_id
              AND LOWER(organisation_type) = 'business'
            LIMIT 1;
        """),
        {"user_id": user_id}
    ).fetchone()

    if not organisation:
        return jsonify(error="No business found for this user"), 404

    # Get the latest available report for that business
    report = db.session.execute(
        text("""
            SELECT
                report_id,
                organisation_id,
                report_month,
                report_year,
                total_views,
                total_saves,
                total_messages,
                total_reviews,
                average_rating,
                bayesian_rating,
                trend_score,
                trend_status,
                engagement_score,
                growth_rate,
                total_volunteer_signups,
                generated_at
            FROM monthly_business_reports
            WHERE organisation_id = :organisation_id
            ORDER BY report_year DESC, report_month DESC
            LIMIT 1;
        """),
        {"organisation_id": organisation.organisation_id}
    ).fetchone()

    if not report:
        return jsonify({
            "organisation_id": organisation.organisation_id,
            "organisation_name": organisation.organisation_name,
            "trend_score": 0,
            "trend_status": "Stable",
            "growth_rate": 0,
            "bayesian_rating": 0,
            "average_rating": 0,
            "total_views": 0,
            "total_saves": 0,
            "total_messages": 0,
            "total_reviews": 0,
            "engagement_score": 0,
            "total_volunteer_signups": 0
        }), 200

    return jsonify({
        "report_id": report.report_id,
        "organisation_id": report.organisation_id,
        "organisation_name": organisation.organisation_name,
        "report_month": report.report_month,
        "report_year": report.report_year,
        "total_views": report.total_views,
        "total_saves": report.total_saves,
        "total_messages": report.total_messages,
        "total_reviews": report.total_reviews,
        "average_rating": float(report.average_rating or 0),
        "bayesian_rating": float(report.bayesian_rating or 0),
        "trend_score": float(report.trend_score or 0),
        "trend_status": report.trend_status,
        "engagement_score": float(report.engagement_score or 0),
        "growth_rate": float(report.growth_rate or 0),
        "total_volunteer_signups": report.total_volunteer_signups or 0,
        "generated_at": report.generated_at.isoformat() if report.generated_at else None
    }), 200
