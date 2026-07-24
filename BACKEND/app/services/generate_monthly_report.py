import psycopg2

from trend_score_service import (
    calculate_engagement_score,
    calculate_growth_rate,
    classify_trend_status
)


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


def get_engagement_counts(cursor, organisation_id, year, month):
    """
    Counts user activity for one organisation in one month.
    """

    cursor.execute(
        """
        SELECT
            COUNT(*) FILTER (WHERE engagement_type = 'profile_view') AS profile_views,
            COUNT(*) FILTER (WHERE engagement_type = 'save') AS saves,
            COUNT(*) FILTER (WHERE engagement_type = 'message') AS messages,
            COUNT(*) FILTER (WHERE engagement_type = 'rating') AS ratings,
            COUNT(*) FILTER (WHERE engagement_type = 'volunteer_signup') AS volunteer_signups
        FROM engagement_logs
        WHERE organisation_id = %s
          AND EXTRACT(YEAR FROM created_at) = %s
          AND EXTRACT(MONTH FROM created_at) = %s;
        """,
        (organisation_id, year, month)
    )

    row = cursor.fetchone()

    return {
        "profile_views": row[0],
        "saves": row[1],
        "messages": row[2],
        "ratings": row[3],
        "volunteer_signups": row[4]
    }


def get_previous_month_score(cursor, organisation_id, year, month):
    """
    Gets the previous month's engagement score.
    """

    if month == 1:
        previous_month = 12
        previous_year = year - 1
    else:
        previous_month = month - 1
        previous_year = year

    cursor.execute(
        """
        SELECT engagement_score
        FROM monthly_business_reports
        WHERE organisation_id = %s
          AND report_month = %s
          AND report_year = %s;
        """,
        (organisation_id, previous_month, previous_year)
    )

    result = cursor.fetchone()

    if result is None:
        return 0

    return float(result[0])


def save_monthly_report(
    cursor,
    organisation_id,
    year,
    month,
    counts,
    engagement_score,
    growth_rate,
    trend_status
):
    """
    Saves the final report into monthly_business_reports.
    """

    cursor.execute(
        """
        INSERT INTO monthly_business_reports
        (
            organisation_id,
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
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (organisation_id, report_month, report_year)
        DO UPDATE SET
            total_views = EXCLUDED.total_views,
            total_saves = EXCLUDED.total_saves,
            total_messages = EXCLUDED.total_messages,
            total_reviews = EXCLUDED.total_reviews,
            total_volunteer_signups = EXCLUDED.total_volunteer_signups,
            engagement_score = EXCLUDED.engagement_score,
            growth_rate = EXCLUDED.growth_rate,
            trend_status = EXCLUDED.trend_status;
        """,
        (
            organisation_id,
            month,
            year,
            counts["profile_views"],
            counts["saves"],
            counts["messages"],
            counts["ratings"],
            counts["volunteer_signups"],
            engagement_score,
            growth_rate,
            trend_status
        )
    )


def generate_report(organisation_id, year, month):
    connection = get_connection()
    cursor = connection.cursor()

    counts = get_engagement_counts(cursor, organisation_id, year, month)

    engagement_score = calculate_engagement_score(counts)

    previous_score = get_previous_month_score(cursor, organisation_id, year, month)

    if previous_score == 0:
        growth_rate = 0
        trend_status = "Base Month"
    else:
        growth_rate = calculate_growth_rate(engagement_score, previous_score)
        trend_status = classify_trend_status(growth_rate)

    save_monthly_report(
        cursor,
        organisation_id,
        year,
        month,
        counts,
        engagement_score,
        growth_rate,
        trend_status
    )

    connection.commit()
    cursor.close()
    connection.close()

    print("Monthly report generated successfully.")
    print("Organisation ID:", organisation_id)
    print("Month:", month)
    print("Year:", year)
    print("Counts:", counts)
    print("Engagement Score:", engagement_score)
    print("Growth Rate:", round(growth_rate, 2))
    print("Trend Status:", trend_status)


if __name__ == "__main__":
    generate_report(organisation_id=159, year=2026, month=5)
    generate_report(organisation_id=159, year=2026, month=6)
