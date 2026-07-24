"""
Recommendation API Routes
=========================

Register this blueprint in BACKEND/app/__init__.py:

    from app.routes.recommendation_routes import recommendation_bp
    app.register_blueprint(recommendation_bp, url_prefix="/api/recommendations")

Useful URLs after Flask starts:

    POST http://localhost:5001/api/recommendations/train
    POST http://localhost:5001/api/recommendations/train/database
    POST http://localhost:5001/api/recommendations/train/spreadsheet

If spreadsheet organisation IDs are 1000, 1001, 1002...
but the database uses 1, 2, 3..., use organisation_id_offset=-999.
    GET  http://localhost:5001/api/recommendations/user/30001
    GET  http://localhost:5001/api/recommendations/spreadsheet-preview
"""

from flask import Blueprint, jsonify, request

from app.services.recommendation_service import (
    get_recommendations,
    get_recommendations_with_explanations,
    spreadsheet_preview,
    train_svd_model,
    train_svd_model_from_database,
    train_svd_model_from_spreadsheet,
)

recommendation_bp = Blueprint("recommendation_bp", __name__)


@recommendation_bp.route("/train", methods=["POST"])
def train_model():
    """
    Train the recommender and store UserFactor and OrganisationFactor vectors.

    Default source is database.

    JSON body examples:

        {"source": "database"}

        {"source": "spreadsheet", "user_id_offset": 30000}

    Query string also works:

        /api/recommendations/train?source=spreadsheet&user_id_offset=30000
    """
    data = request.get_json(silent=True) or {}

    source = data.get("source") or request.args.get("source", "database")
    max_components = int(
        data.get("max_components") or request.args.get("max_components", 10)
    )
    user_id_offset = int(
        data.get("user_id_offset") or request.args.get("user_id_offset", 0)
    )
    organisation_id_offset = int(
        data.get("organisation_id_offset") or request.args.get("organisation_id_offset", 0)
    )

    result = train_svd_model(
        source=source,
        max_components=max_components,
        user_id_offset=user_id_offset,
        organisation_id_offset=organisation_id_offset,
    )

    status_code = 200 if result.get("trained") else 400

    return jsonify(result), status_code


@recommendation_bp.route("/train/database", methods=["POST"])
def train_model_from_database():
    """
    Train using real app data from ratings, saved organisations, and engagement logs.
    """
    data = request.get_json(silent=True) or {}

    max_components = int(
        data.get("max_components") or request.args.get("max_components", 10)
    )

    result = train_svd_model_from_database(max_components=max_components)
    status_code = 200 if result.get("trained") else 400

    return jsonify(result), status_code


@recommendation_bp.route("/train/spreadsheet", methods=["POST"])
def train_model_from_spreadsheet():
    """
    Train using the Excel spreadsheet.

    Use user_id_offset=30000 if the spreadsheet user IDs are 1, 2, 3...
    but your seeded database user IDs are 30001, 30002, 30003...
    """
    data = request.get_json(silent=True) or {}

    max_components = int(
        data.get("max_components") or request.args.get("max_components", 10)
    )
    user_id_offset = int(
        data.get("user_id_offset") or request.args.get("user_id_offset", 0)
    )
    organisation_id_offset = int(
        data.get("organisation_id_offset") or request.args.get("organisation_id_offset", 0)
    )

    result = train_svd_model_from_spreadsheet(
        max_components=max_components,
        user_id_offset=user_id_offset,
        organisation_id_offset=organisation_id_offset,
    )

    status_code = 200 if result.get("trained") else 400

    return jsonify(result), status_code


@recommendation_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_recommendations(user_id):
    """
    Return recommendations for a selected user.

    Example:
        /api/recommendations/user/30001?top_n=5
    """
    top_n = request.args.get("top_n", 10, type=int)
    include_explanations = request.args.get(
        "include_explanations",
        "true",
    ).lower() == "true"

    if include_explanations:
        result = get_recommendations_with_explanations(user_id, top_n)
    else:
        result = get_recommendations(user_id, top_n)

    return jsonify(result), 200


@recommendation_bp.route("/spreadsheet-preview", methods=["GET"])
def preview_spreadsheet():
    """
    Check whether Flask can find and read the spreadsheet.

    Example:
        /api/recommendations/spreadsheet-preview?user_id_offset=30000
    """
    user_id_offset = request.args.get("user_id_offset", 0, type=int)
    organisation_id_offset = request.args.get("organisation_id_offset", 0, type=int)
    sample_size = request.args.get("sample_size", 10, type=int)

    result = spreadsheet_preview(
        user_id_offset=user_id_offset,
        organisation_id_offset=organisation_id_offset,
        sample_size=sample_size,
    )

    return jsonify(result), 200
