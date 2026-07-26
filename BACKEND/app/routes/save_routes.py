from flask import Blueprint, request, jsonify
from sqlalchemy import text
from app.extensions import db


save_bp = Blueprint("save_bp", __name__)


@save_bp.route("", methods=["POST"])
def save_organisation():
    data = request.get_json() or {}

    user_id = data.get("user_id")
    organisation_id = data.get("organisation_id")

    if not user_id:
        return jsonify(error="user_id is required"), 400

    if not organisation_id:
        return jsonify(error="organisation_id is required"), 400

    # Prevent the same user saving the same organisation many times
    db.session.execute(text("""
        CREATE UNIQUE INDEX IF NOT EXISTS unique_user_saved_org
        ON saved_organisations(user_id, organisation_id);
    """))

    db.session.execute(
        text("""
            INSERT INTO saved_organisations
            (
                user_id,
                organisation_id,
                saved_at
            )
            VALUES
            (
                :user_id,
                :organisation_id,
                CURRENT_TIMESTAMP
            )
            ON CONFLICT (user_id, organisation_id)
            DO NOTHING;
        """),
        {
            "user_id": user_id,
            "organisation_id": organisation_id
        }
    )

    db.session.commit()

    return jsonify(message="Organisation saved successfully"), 201


@save_bp.route("", methods=["DELETE"])
def unsave_organisation():
    data = request.get_json() or {}

    user_id = data.get("user_id")
    organisation_id = data.get("organisation_id")

    if not user_id:
        return jsonify(error="user_id is required"), 400

    if not organisation_id:
        return jsonify(error="organisation_id is required"), 400

    db.session.execute(
        text("""
            DELETE FROM saved_organisations
            WHERE user_id = :user_id
              AND organisation_id = :organisation_id;
        """),
        {
            "user_id": user_id,
            "organisation_id": organisation_id
        }
    )

    db.session.commit()

    return jsonify(message="Organisation removed from saved list"), 200
