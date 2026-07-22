from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Organisation

organisation_bp = Blueprint("organisation_bp", __name__)

@organisation_bp.route("", methods=["GET"])
def list_organisations():
    organisation_type = request.args.get("type")
    query = Organisation.query

    if organisation_type:
        query = query.filter_by(organisation_type=organisation_type)

    organisations = query.order_by(Organisation.organisation_name.asc()).all()
    return jsonify([org.to_dict() for org in organisations])

@organisation_bp.route("/<int:organisation_id>", methods=["GET"])
def get_organisation(organisation_id):
    organisation = Organisation.query.get_or_404(organisation_id)
    return jsonify(organisation.to_dict())

@organisation_bp.route("", methods=["POST"])
def create_organisation():
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
    db.session.commit()

    return jsonify(message="Organisation created", organisation=organisation.to_dict()), 201
