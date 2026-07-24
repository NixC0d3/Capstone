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
import psycopg2

monthly_report_bp = Blueprint("monthly_report", __name__)

DB_NAME = "capstone"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"


def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


@monthly_report_bp.route("/monthly-report/<int:organisation_id>", methods=["GET"])
def get_monthly_report(organisation_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            report_month,
            report_year,
            total_views,
            total_saves,
            total_messages,
            total_reviews,
            total_volunteer_signups,
            engagement_score,
            growth_rate,
            trend_status
        FROM monthly_business_reports
        WHERE organisation_id = %s
        ORDER BY report_year, report_month;
        """,
        (organisation_id,)
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
