from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Organisation, Category, Location, OrganisationCategory


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

    organisation = Organisation(
        owner_user_id=data.get("owner_user_id"),
        category_id=data.get("category_id"),
        location_id=data.get("location_id"),
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
