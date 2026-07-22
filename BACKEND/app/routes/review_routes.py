from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import RatingReview, ReviewFlag

review_bp = Blueprint("review_bp", __name__)

@review_bp.route("", methods=["POST"])
def create_review():
    data = request.get_json() or {}

    review = RatingReview(
        organisation_id=data.get("organisation_id"),
        user_id=data.get("user_id"),
        rating=data.get("rating"),
        review_text=data.get("review_text")
    )

    db.session.add(review)
    db.session.commit()

    return jsonify(message="Review added", review=review.to_dict()), 201

@review_bp.route("/<int:review_id>/flag", methods=["POST"])
def flag_review(review_id):
    data = request.get_json() or {}

    flag = ReviewFlag(
        review_id=review_id,
        flagged_by_user_id=data.get("flagged_by_user_id"),
        reason=data.get("reason", "")
    )

    db.session.add(flag)
    db.session.commit()

    return jsonify(message="Review flagged", flag=flag.to_dict()), 201
