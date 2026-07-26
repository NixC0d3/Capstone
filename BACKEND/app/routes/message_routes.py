from flask import Blueprint, request, jsonify
from sqlalchemy import text
from app.extensions import db


message_bp = Blueprint("message_bp", __name__)


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

    # Prevent duplicate conversation rows
    db.session.execute(text("""
        CREATE UNIQUE INDEX IF NOT EXISTS unique_user_org_conversation
        ON conversations(user_id, organisation_id);
    """))

    # Create conversation if it does not exist
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

    conversation_id = conversation.conversation_id

    # Insert message
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
            "conversation_id": conversation_id,
            "sender_user_id": user_id,
            "message_text": message_text
        }
    )

    db.session.commit()

    return jsonify(
        message="Message sent successfully",
        conversation_id=conversation_id
    ), 201
