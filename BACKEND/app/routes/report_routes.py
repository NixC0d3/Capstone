from flask import Blueprint, jsonify
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

    rows = cursor.fetchall()

    reports = []

    for row in rows:
        reports.append({
            "report_month": row[0],
            "report_year": row[1],
            "total_views": row[2],
            "total_saves": row[3],
            "total_messages": row[4],
            "total_reviews": row[5],
            "total_volunteer_signups": row[6],
            "engagement_score": float(row[7]),
            "growth_rate": float(row[8]),
            "trend_status": row[9]
        })

    cursor.close()
    connection.close()

    return jsonify(reports)