from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import RatingReview


review_bp = Blueprint("review_bp", __name__)


@review_bp.route("", methods=["POST"])
def create_review():
    data = request.get_json() or {}

    organisation_id = data.get("organisation_id")
    user_id = data.get("user_id")
    rating = data.get("rating")
    review_text = data.get("review_text", "")

    if not organisation_id:
        return jsonify(error="organisation_id is required"), 400

    if not user_id:
        return jsonify(error="user_id is required"), 400

    if rating is None:
        return jsonify(error="rating is required"), 400

    review = RatingReview(
        organisation_id=int(organisation_id),
        user_id=int(user_id),
        rating=int(rating),
        review_text=review_text,
        is_hidden=False
    )

    db.session.add(review)
    db.session.commit()

    return jsonify(
        message="Review submitted successfully",
        review=review.to_dict()
    ), 201


@review_bp.route("/organisation/<int:organisation_id>", methods=["GET"])
def get_reviews_for_organisation(organisation_id):
    reviews = RatingReview.query.filter_by(
        organisation_id=organisation_id,
        is_hidden=False
    ).order_by(
        RatingReview.created_at.desc()
    ).all()

    return jsonify([review.to_dict() for review in reviews]), 200
