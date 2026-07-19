from flask import Blueprint, jsonify, request
from app.models import RatingReview
from app.services.recommendation_service import recommend_with_svd

recommendation_bp = Blueprint("recommendation_bp", __name__)

@recommendation_bp.route("/<int:user_id>", methods=["GET"])
def get_recommendations(user_id):
    top_n = int(request.args.get("top_n", 5))

    ratings = [
        {
            "user_id": review.user_id,
            "organisation_id": review.organisation_id,
            "rating": review.rating
        }
        for review in RatingReview.query.filter_by(is_hidden=False).all()
    ]

    result = recommend_with_svd(ratings, selected_user_id=user_id, top_n=top_n)
    return jsonify(result)
