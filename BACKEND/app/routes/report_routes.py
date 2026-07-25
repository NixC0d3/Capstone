from flask import Blueprint, jsonify
import psycopg2

monthly_report_bp = Blueprint("monthly_report", __name__)

DB_NAME = "capstone"
DB_USER = "postgres"
DB_PASSWORD = "password"  # use your working PostgreSQL password
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


def safe_float(value):
    if value is None:
        return 0
    return float(value)


@monthly_report_bp.route("/monthly-report/<int:organisation_id>", methods=["GET"])
def get_monthly_report(organisation_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            o.organisation_name,
            m.organisation_id,
            m.report_month,
            m.report_year,
            m.total_views,
            m.total_saves,
            m.total_messages,
            m.total_reviews,
            m.total_volunteer_signups,
            m.average_rating,
            m.bayesian_rating,
            m.engagement_score,
            m.trend_score,
            m.growth_rate,
            m.trend_status,
            m.generated_at
        FROM monthly_business_reports m
        JOIN organisations o
            ON m.organisation_id = o.organisation_id
        WHERE m.organisation_id = %s
        ORDER BY m.report_year, m.report_month;
        """,
        (organisation_id,)
    )

    rows = cursor.fetchall()
    reports = []

    for row in rows:
        reports.append({
            "organisation_name": row[0],
            "organisation_id": row[1],
            "report_month": row[2],
            "report_year": row[3],
            "month": f"{row[2]}/{row[3]}",

            "total_views": row[4],
            "total_saves": row[5],
            "total_messages": row[6],
            "total_reviews": row[7],
            "total_volunteer_signups": row[8],

            # Extra names for frontend components
            "profile_views": row[4],
            "saves": row[5],
            "messages": row[6],
            "volunteer_signups": row[8],

            "average_rating": safe_float(row[9]),
            "bayesian_rating": safe_float(row[10]),
            "engagement_score": safe_float(row[11]),
            "trend_score": safe_float(row[12]),
            "growth_rate": round(safe_float(row[13]), 2),
            "trend_status": row[14],
            "generated_at": str(row[15])
        })

    cursor.close()
    connection.close()

    return jsonify(reports)
