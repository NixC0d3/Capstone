import psycopg2

from trend_score_service import (
    calculate_average_rating,
    calculate_bayesian_rating,
    calculate_engagement_score,
    calculate_trend_score,
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
    Gets the previous month's trend score.
    """

    if month == 1:
        previous_month = 12
        previous_year = year - 1
    else:
        previous_month = month - 1
        previous_year = year

    cursor.execute(
        """
        SELECT COALESCE(trend_score, engagement_score)
        FROM monthly_business_reports
        WHERE organisation_id = %s
          AND report_month = %s
          AND report_year = %s;
        """,
        (organisation_id, previous_month, previous_year)
    )

    result = cursor.fetchone()

    if result is None or result[0] is None:
        return 0

    return float(result[0])


def save_monthly_report(
    cursor,
    organisation_id,
    year,
    month,
    counts,
    average_rating,
    bayesian_rating,
    engagement_score,
    trend_score,
    growth_rate,
    trend_status
):
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
            average_rating,
            bayesian_rating,
            engagement_score,
            trend_score,
            growth_rate,
            trend_status
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (organisation_id, report_month, report_year)
        DO UPDATE SET
            total_views = EXCLUDED.total_views,
            total_saves = EXCLUDED.total_saves,
            total_messages = EXCLUDED.total_messages,
            total_reviews = EXCLUDED.total_reviews,
            total_volunteer_signups = EXCLUDED.total_volunteer_signups,
            average_rating = EXCLUDED.average_rating,
            bayesian_rating = EXCLUDED.bayesian_rating,
            engagement_score = EXCLUDED.engagement_score,
            trend_score = EXCLUDED.trend_score,
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
            average_rating,
            bayesian_rating,
            engagement_score,
            trend_score,
            growth_rate,
            trend_status
        )
    )
    
def get_rating_stats(cursor, organisation_id, year, month):
    """
    Gets the average rating and number of reviews for one organisation in one month.
    """

    cursor.execute(
        """
        SELECT
            COALESCE(SUM(rating), 0) AS total_rating_score,
            COUNT(*) AS total_reviews
        FROM ratings_reviews
        WHERE organisation_id = %s
          AND EXTRACT(YEAR FROM created_at) = %s
          AND EXTRACT(MONTH FROM created_at) = %s;
        """,
        (organisation_id, year, month)
    )

    row = cursor.fetchone()

    return {
        "total_rating_score": float(row[0]),
        "total_reviews": row[1]
    }
    
def get_global_average_rating(cursor):
    """
    Gets the average rating across all organisations.
    This is used for Bayesian rating.
    """

    cursor.execute(
        """
        SELECT COALESCE(AVG(rating), 0)
        FROM ratings_reviews;
        """
    )

    result = cursor.fetchone()
    return float(result[0])
    

def generate_report(organisation_id, year, month):
    connection = get_connection()
    cursor = connection.cursor()

    # 1. Get engagement activity counts
    counts = get_engagement_counts(cursor, organisation_id, year, month)

    # 2. Calculate engagement score
    engagement_score = calculate_engagement_score(counts)

    # 3. Get rating stats for this organisation/month
    rating_stats = get_rating_stats(cursor, organisation_id, year, month)

    average_rating = calculate_average_rating(
        rating_stats["total_rating_score"],
        rating_stats["total_reviews"]
    )

    # 4. Get global average rating across all organisations
    global_average_rating = get_global_average_rating(cursor)

    # 5. Calculate Bayesian rating
    bayesian_rating = calculate_bayesian_rating(
        average_rating,
        rating_stats["total_reviews"],
        global_average_rating
    )

    # 6. Calculate final trend score
    trend_score = calculate_trend_score(
        engagement_score,
        bayesian_rating
    )

    # 7. Compare this month's trend score to the previous month
    previous_score = get_previous_month_score(cursor, organisation_id, year, month)

    if previous_score == 0:
        growth_rate = 0
        trend_status = "Base Month"
    else:
        growth_rate = calculate_growth_rate(trend_score, previous_score)
        trend_status = classify_trend_status(growth_rate)

    # 8. Save the full report
    save_monthly_report(
        cursor,
        organisation_id,
        year,
        month,
        counts,
        average_rating,
        bayesian_rating,
        engagement_score,
        trend_score,
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
    print("Average Rating:", round(average_rating, 2))
    print("Bayesian Rating:", round(bayesian_rating, 2))
    print("Engagement Score:", engagement_score)
    print("Trend Score:", round(trend_score, 2))
    print("Growth Rate:", round(growth_rate, 2))
    print("Trend Status:", trend_status)

if __name__ == "__main__":
    generate_report(organisation_id=159, year=2026, month=5)
    generate_report(organisation_id=159, year=2026, month=6)
