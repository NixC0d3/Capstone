from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Organisation, Category, Location, OrganisationCategory
from sqlalchemy import text
from datetime import datetime, date


organisation_bp = Blueprint("organisation_bp", __name__)


def organisation_to_dict(org):
    """
    Converts an organisation into a dictionary that the frontend can use.
    This includes category and location information from related tables.
    """

    data = org.to_dict()

    # Main category from organisations.category_id
    data["category_name"] = org.category.category_name if org.category else None
    data["category_type"] = org.category.category_type if org.category else None

    # Location details from locations table
    data["parish"] = org.location.parish if org.location else None
    data["town"] = org.location.town if org.location else None
    data["address"] = org.location.address if org.location else None

    # Extra categories from organisation_categories table
    category_rows = (
        db.session.query(Category)
        .join(
            OrganisationCategory,
            Category.category_id == OrganisationCategory.category_id
        )
        .filter(OrganisationCategory.organisation_id == org.organisation_id)
        .all()
    )

    data["categories"] = [
        {
            "category_id": category.category_id,
            "category_name": category.category_name,
            "category_type": category.category_type
        }
        for category in category_rows
    ]

    # If the organisation has no direct category_id, use the first category
    # from organisation_categories as the display category.
    if data["category_name"] is None and category_rows:
        data["category_name"] = category_rows[0].category_name
        data["category_type"] = category_rows[0].category_type
        
    # Rating summary from ratings_reviews table
    rating_row = db.session.execute(
        text("""
            SELECT
                COUNT(*) AS review_count,
                COALESCE(AVG(rating), 0) AS average_rating
            FROM ratings_reviews
            WHERE organisation_id = :organisation_id
              AND COALESCE(is_hidden, FALSE) = FALSE;
        """),
        {"organisation_id": org.organisation_id}
    ).fetchone()

    review_count = int(rating_row.review_count or 0)
    average_rating = round(float(rating_row.average_rating or 0), 1)

    data["review_count"] = review_count
    data["average_rating"] = average_rating

    if review_count > 0:
        data["rating"] = f"{average_rating}/5 ({review_count})"
    else:
        data["rating"] = None

    return data


@organisation_bp.route("", methods=["GET"])
def list_organisations():
    """
    Gets organisations.

    Supports optional filters:
    /api/organisations?search=book
    /api/organisations?category_id=101
    /api/organisations?parish=Kingstown
    /api/organisations?type=business
    """

    search = request.args.get("search", "").strip()
    category_id = request.args.get("category_id", type=int)
    parish = request.args.get("parish", "").strip()
    organisation_type = request.args.get("type", "").strip()

    query = Organisation.query

    # Filter by organisation type: business or charity
    if organisation_type:
        query = query.filter(
            db.func.lower(Organisation.organisation_type) == organisation_type.lower()
        )

    # Search by organisation name
    if search:
        query = query.filter(
            Organisation.organisation_name.ilike(f"%{search}%")
        )

    # Filter by parish/location
    if parish:
        query = query.join(Location).filter(
            db.func.lower(Location.parish) == parish.lower()
        )

    # Filter by category.
    # This checks both:
    # 1. organisations.category_id
    # 2. organisation_categories.category_id
    if category_id:
        query = query.outerjoin(
            OrganisationCategory,
            Organisation.organisation_id == OrganisationCategory.organisation_id
        ).filter(
            db.or_(
                Organisation.category_id == category_id,
                OrganisationCategory.category_id == category_id
            )
        )

    organisations = (
        query
        .distinct()
        .order_by(Organisation.organisation_name.asc())
        .all()
    )

    return jsonify([
        organisation_to_dict(org)
        for org in organisations
    ])


@organisation_bp.route("", methods=["POST"])
def create_organisation():
    """
    Creates a new organisation.
    """

    data = request.get_json() or {}

    # Create location using selected parish + entered details
    location = Location(
        parish=data.get("parish"),
        town=data.get("town"),
        address=data.get("address")
    )

    db.session.add(location)
    db.session.flush()

    organisation = Organisation(
        owner_user_id=data.get("owner_user_id"),
        owner_first_name=data.get("owner_first_name"),
        owner_last_name=data.get("owner_last_name"),
        category_id=data.get("category_id"),
        location_id=location.location_id,
        organisation_name=data.get("organisation_name", ""),
        organisation_type=data.get("organisation_type", "business"),
        description=data.get("description"),
        phone=data.get("phone"),
        email=data.get("email"),
        website_url=data.get("website_url"),
    )

    db.session.add(organisation)
    db.session.flush()

    # Optional: store multiple categories if frontend sends category_ids
    category_ids = data.get("category_ids", [])

    for category_id in category_ids:
        organisation_category = OrganisationCategory(
            organisation_id=organisation.organisation_id,
            category_id=category_id
        )
        db.session.add(organisation_category)

    db.session.commit()

    return jsonify({
        "message": "Organisation created",
        "organisation": organisation_to_dict(organisation)
    }), 201


@organisation_bp.route("/categories", methods=["GET"])
def get_categories():
    """
    Gets categories.

    Optional:
    /api/organisations/categories?type=business
    /api/organisations/categories?type=charity
    """

    category_type = request.args.get("type", "").strip()

    query = Category.query

    if category_type:
        query = query.filter(
            db.or_(
                db.func.lower(Category.category_type) == category_type.lower(),
                db.func.lower(Category.category_type) == "both"
            )
        )

    categories = query.order_by(Category.category_name.asc()).all()

    return jsonify([
        {
            "category_id": category.category_id,
            "category_name": category.category_name,
            "category_type": category.category_type
        }
        for category in categories
    ])


@organisation_bp.route("/locations", methods=["GET"])
def get_locations():
    """
    Gets unique parishes for the location dropdown.

    This prevents repeated locations in the frontend dropdown.
    """

    rows = (
        db.session.query(
            db.func.min(Location.location_id).label("location_id"),
            Location.parish
        )
        .filter(Location.parish.isnot(None))
        .filter(db.func.trim(Location.parish) != "")
        .group_by(Location.parish)
        .order_by(Location.parish.asc())
        .all()
    )

    return jsonify([
        {
            "location_id": row.location_id,
            "parish": row.parish
        }
        for row in rows
    ])


@organisation_bp.route("/<int:organisation_id>", methods=["GET"])
def get_organisation(organisation_id):
    """
    Gets one organisation by ID.
    """

    organisation = Organisation.query.get_or_404(organisation_id)
    return jsonify(organisation_to_dict(organisation))

@organisation_bp.route("/<int:organisation_id>", methods=["PUT"])
def update_organisation(organisation_id):
    """
    Updates an existing organisation.
    """
    organisation = Organisation.query.get_or_404(organisation_id)
    data = request.get_json() or {}

    organisation.category_id = data.get("category_id", organisation.category_id)
    organisation.organisation_name = data.get("organisation_name", organisation.organisation_name)
    organisation.description = data.get("description", organisation.description)
    organisation.phone = data.get("phone", organisation.phone)
    organisation.email = data.get("email", organisation.email)
    organisation.website_url = data.get("website_url", organisation.website_url)

    # update location
    if organisation.location:
        organisation.location.parish = data.get("parish", organisation.location.parish)
        organisation.location.town = data.get("town",organisation.location.town)
        organisation.location.address = data.get("address",organisation.location.address)
    else:

        location = Location(
            parish=data.get("parish"),
            town=data.get("town"),
            address=data.get("address")
        )

        db.session.add(location)
        db.session.flush()

        organisation.location_id = (location.location_id)

    # Update extra categories
    OrganisationCategory.query.filter_by(
        organisation_id=organisation.organisation_id
    ).delete()

    for category_id in data.get("category_ids", []):
        db.session.add(
            OrganisationCategory(
                organisation_id=organisation.organisation_id,
                category_id=category_id
            )
        )

    db.session.commit()

    return jsonify({
        "message": "Organisation updated",
        "organisation": organisation_to_dict(organisation)
    })

@organisation_bp.route("/owner/<int:user_id>", methods=["GET"])
def get_owner_organisation(user_id):
    organisation = Organisation.query.filter_by(
        owner_user_id=user_id
    ).first()

    if not organisation:
        return jsonify(None), 404

    return jsonify(organisation_to_dict(organisation))
 
 
#Trend score functions   
def get_month_start(year, month):
    return datetime(year, month, 1)


def get_next_month_start(year, month):
    if month == 12:
        return datetime(year + 1, 1, 1)

    return datetime(year, month + 1, 1)


def get_previous_year_month(today):
    if today.month == 1:
        return today.year - 1, 12

    return today.year, today.month - 1


def get_engagement_counts(organisation_id, start_date, end_date):
    """
    Counts engagement activity from engagement_logs for one organisation
    between start_date and end_date.
    """

    row = db.session.execute(
        text("""
            SELECT
                COALESCE(SUM(CASE WHEN engagement_type = 'profile_view' THEN 1 ELSE 0 END), 0) AS profile_views,
                COALESCE(SUM(CASE WHEN engagement_type = 'save' THEN 1 ELSE 0 END), 0) AS saves,
                COALESCE(SUM(CASE WHEN engagement_type = 'message' THEN 1 ELSE 0 END), 0) AS messages,
                COALESCE(SUM(CASE WHEN engagement_type = 'review' THEN 1 ELSE 0 END), 0) AS reviews,
                COALESCE(SUM(CASE WHEN engagement_type = 'volunteer_signup' THEN 1 ELSE 0 END), 0) AS volunteer_signups
            FROM engagement_logs
            WHERE organisation_id = :organisation_id
              AND created_at >= :start_date
              AND created_at < :end_date;
        """),
        {
            "organisation_id": organisation_id,
            "start_date": start_date,
            "end_date": end_date
        }
    ).fetchone()

    return {
        "profile_views": int(row.profile_views or 0),
        "saves": int(row.saves or 0),
        "messages": int(row.messages or 0),
        "reviews": int(row.reviews or 0),
        "volunteer_signups": int(row.volunteer_signups or 0)
    }


def calculate_weighted_engagement_score(counts):
    """
    Weighted engagement formula.
    Higher-value actions receive more points.
    """

    return (
        counts.get("profile_views", 0) * 1
        + counts.get("saves", 0) * 3
        + counts.get("messages", 0) * 4
        + counts.get("reviews", 0) * 5
        + counts.get("volunteer_signups", 0) * 5
    )


def calculate_growth_rate(previous_score, current_score):
    if previous_score == 0 and current_score == 0:
        return 0.0

    if previous_score == 0 and current_score > 0:
        return 100.0

    return round(((current_score - previous_score) / previous_score) * 100, 2)


def calculate_trend_label(growth_rate):
    if growth_rate > 10:
        return "Improving"

    if growth_rate < -10:
        return "Declining"

    return "Stable"


def calculate_trend_score(previous_score, current_score, growth_rate):
    """
    Converts the comparison into a score out of 100.

    If there is no activity at all, score stays 0.
    If current activity improves, score goes up.
    If current activity drops, score goes down.
    """

    if previous_score == 0 and current_score == 0:
        return 0

    if previous_score == 0 and current_score > 0:
        return 100

    score = 50 + (growth_rate / 2)
    score = max(0, min(100, score))

    return round(score)


def calculate_bayesian_rating(organisation_id):
    """
    Calculates Bayesian rating so that organisations with few reviews
    are not unfairly ranked too high or too low.
    """

    global_row = db.session.execute(
        text("""
            SELECT COALESCE(AVG(rating), 0) AS global_average
            FROM ratings_reviews
            WHERE COALESCE(is_hidden, FALSE) = FALSE;
        """)
    ).fetchone()

    org_row = db.session.execute(
        text("""
            SELECT
                COUNT(*) AS review_count,
                COALESCE(AVG(rating), 0) AS average_rating
            FROM ratings_reviews
            WHERE organisation_id = :organisation_id
              AND COALESCE(is_hidden, FALSE) = FALSE;
        """),
        {"organisation_id": organisation_id}
    ).fetchone()

    global_average = float(global_row.global_average or 0)
    review_count = int(org_row.review_count or 0)
    organisation_average = float(org_row.average_rating or 0)

    minimum_reviews = 5

    if review_count == 0:
        return round(global_average, 1), 0

    bayesian_rating = (
        (review_count / (review_count + minimum_reviews)) * organisation_average
        + (minimum_reviews / (review_count + minimum_reviews)) * global_average
    )

    return round(bayesian_rating, 1), review_count


@organisation_bp.route("/<int:organisation_id>/dashboard-report", methods=["GET"])
def get_dashboard_report(organisation_id):
    """
    Generates the dashboard report dynamically.

    It compares previous-month engagement with current-month engagement.
    Every time the user clicks Generate Report, this recalculates from
    engagement_logs, so the score is not hardcoded.
    """

    organisation = Organisation.query.get_or_404(organisation_id)

    today = date.today()

    current_year = today.year
    current_month = today.month

    previous_year, previous_month = get_previous_year_month(today)

    current_start = get_month_start(current_year, current_month)
    current_end = get_next_month_start(current_year, current_month)

    previous_start = get_month_start(previous_year, previous_month)
    previous_end = get_next_month_start(previous_year, previous_month)

    previous_counts = get_engagement_counts(
        organisation_id,
        previous_start,
        previous_end
    )

    current_counts = get_engagement_counts(
        organisation_id,
        current_start,
        current_end
    )

    previous_score = calculate_weighted_engagement_score(previous_counts)
    current_score = calculate_weighted_engagement_score(current_counts)

    growth_rate = calculate_growth_rate(previous_score, current_score)
    trend_label = calculate_trend_label(growth_rate)
    trend_score = calculate_trend_score(
        previous_score,
        current_score,
        growth_rate
    )

    bayesian_rating, total_reviews = calculate_bayesian_rating(organisation_id)

    previous_month_label = previous_start.strftime("%B")
    current_month_label = current_start.strftime("%B")

    return jsonify({
        "organisation_id": organisation.organisation_id,
        "organisation_name": organisation.organisation_name,
        "organisation_type": organisation.organisation_type,

        "previous_month_label": previous_month_label,
        "current_month_label": current_month_label,

        "previous_month": previous_counts,
        "current_month": current_counts,

        "previous_score": previous_score,
        "current_score": current_score,

        "trend_score": trend_score,
        "growth_rate": growth_rate,
        "trend_label": trend_label,
        "trend_status": trend_label,

        "bayesian_rating": bayesian_rating,
        "total_reviews": total_reviews
    }), 200
