from flask import Blueprint, request, jsonify
from sqlalchemy import text
from app.extensions import db


message_bp = Blueprint("message_bp", __name__)


@message_bp.route("/conversation", methods=["GET"])
def get_conversation():
    user_id = request.args.get("user_id", type=int)
    organisation_id = request.args.get("organisation_id", type=int)

    if not user_id:
        return jsonify(error="user_id is required"), 400

    if not organisation_id:
        return jsonify(error="organisation_id is required"), 400

    organisation = db.session.execute(
        text("""
            SELECT organisation_id, organisation_name, organisation_type
            FROM organisations
            WHERE organisation_id = :organisation_id;
        """),
        {"organisation_id": organisation_id}
    ).fetchone()

    if not organisation:
        return jsonify(error="Organisation not found"), 404

    conversation = db.session.execute(
        text("""
            SELECT conversation_id
            FROM conversations
            WHERE user_id = :user_id
              AND organisation_id = :organisation_id;
        """),
        {
            "user_id": user_id,
            "organisation_id": organisation_id
        }
    ).fetchone()

    messages = []

    if conversation:
        result = db.session.execute(
            text("""
                SELECT
                    m.message_id,
                    m.conversation_id,
                    m.sender_user_id,
                    COALESCE(u.display_name, u.first_name || ' ' || u.last_name) AS sender_name,
                    m.message_text,
                    m.sent_at,
                    m.is_read
                FROM messages m
                JOIN users u
                    ON u.user_id = m.sender_user_id
                WHERE m.conversation_id = :conversation_id
                ORDER BY m.sent_at ASC;
            """),
            {"conversation_id": conversation.conversation_id}
        )

        for row in result:
            messages.append({
                "message_id": row.message_id,
                "conversation_id": row.conversation_id,
                "sender_user_id": row.sender_user_id,
                "sender_name": row.sender_name,
                "message_text": row.message_text,
                "sent_at": row.sent_at.isoformat() if row.sent_at else None,
                "is_read": row.is_read
            })

    return jsonify({
        "organisation": {
            "organisation_id": organisation.organisation_id,
            "organisation_name": organisation.organisation_name,
            "organisation_type": organisation.organisation_type
        },
        "messages": messages
    }), 200


@message_bp.route("/send", methods=["POST"])
def send_message():
    data = request.get_json() or {}

    user_id = data.get("user_id")
    organisation_id = data.get("organisation_id")
    message_text = data.get("message_text", "").strip()

    if not user_id:
        return jsonify(error="user_id is required"), 400

    if not organisation_id:
        return jsonify(error="organisation_id is required"), 400

    if not message_text:
        return jsonify(error="message_text is required"), 400

    # Create conversation if it does not already exist.
    db.session.execute(
        text("""
            INSERT INTO conversations
            (
                user_id,
                organisation_id,
                created_at,
                last_message_at
            )
            VALUES
            (
                :user_id,
                :organisation_id,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            )
            ON CONFLICT (user_id, organisation_id)
            DO UPDATE SET last_message_at = CURRENT_TIMESTAMP;
        """),
        {
            "user_id": user_id,
            "organisation_id": organisation_id
        }
    )

    conversation = db.session.execute(
        text("""
            SELECT conversation_id
            FROM conversations
            WHERE user_id = :user_id
              AND organisation_id = :organisation_id;
        """),
        {
            "user_id": user_id,
            "organisation_id": organisation_id
        }
    ).fetchone()

    db.session.execute(
        text("""
            INSERT INTO messages
            (
                conversation_id,
                sender_user_id,
                message_text,
                sent_at,
                is_read
            )
            VALUES
            (
                :conversation_id,
                :sender_user_id,
                :message_text,
                CURRENT_TIMESTAMP,
                FALSE
            );
        """),
        {
            "conversation_id": conversation.conversation_id,
            "sender_user_id": user_id,
            "message_text": message_text
        }
    )

    db.session.commit()

    return jsonify(
        message="Message sent successfully",
        conversation_id=conversation.conversation_id
    ), 201
