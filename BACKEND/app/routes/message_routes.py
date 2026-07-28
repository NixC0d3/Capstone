from flask import Blueprint, request, jsonify
from sqlalchemy import text
from app.extensions import db


message_bp = Blueprint("message_bp", __name__)


def format_datetime(value):
    if value:
        return value.isoformat()
    return None


@message_bp.route("/conversation", methods=["GET"])
def get_conversation():
    """
    Used when a general user clicks 'Get in Touch' from an organisation page.
    It loads the conversation between that general user and that organisation.
    """
    user_id = request.args.get("user_id", type=int)
    organisation_id = request.args.get("organisation_id", type=int)

    if not user_id:
        return jsonify(error="user_id is required"), 400

    if not organisation_id:
        return jsonify(error="organisation_id is required"), 400

    organisation = db.session.execute(
        text("""
            SELECT
                organisation_id,
                organisation_name,
                organisation_type
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

    conversation_id = conversation.conversation_id if conversation else None
    messages = []

    if conversation_id:
        result = db.session.execute(
            text("""
                SELECT
                    m.message_id,
                    m.conversation_id,
                    m.sender_user_id,
                    COALESCE(
                        NULLIF(TRIM(COALESCE(u.display_name, '')), ''),
                        NULLIF(TRIM(COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')), ''),
                        u.email,
                        'User'
                    ) AS sender_name,
                    m.message_text,
                    m.sent_at,
                    m.is_read
                FROM messages m
                JOIN users u
                    ON u.user_id = m.sender_user_id
                WHERE m.conversation_id = :conversation_id
                ORDER BY m.sent_at ASC;
            """),
            {"conversation_id": conversation_id}
        )

        for row in result:
            messages.append({
                "message_id": row.message_id,
                "conversation_id": row.conversation_id,
                "sender_user_id": row.sender_user_id,
                "sender_name": row.sender_name,
                "message_text": row.message_text,
                "sent_at": format_datetime(row.sent_at),
                "is_read": row.is_read
            })

    return jsonify({
        "conversation_id": conversation_id,
        "organisation": {
            "organisation_id": organisation.organisation_id,
            "organisation_name": organisation.organisation_name,
            "organisation_type": organisation.organisation_type
        },
        "messages": messages
    }), 200


@message_bp.route("/inbox", methods=["GET"])
def get_inbox():
    """
    Loads all conversations for:
    - a general user, or
    - a business/charity owner based on organisations.owner_user_id
    """
    user_id = request.args.get("user_id", type=int)

    if not user_id:
        return jsonify(error="user_id is required"), 400

    result = db.session.execute(
        text("""
            SELECT
                c.conversation_id,
                c.user_id AS general_user_id,
                c.organisation_id,
                c.created_at,
                c.last_message_at,

                o.organisation_name,
                o.organisation_type,
                o.owner_user_id,

                COALESCE(
                    NULLIF(TRIM(COALESCE(gu.display_name, '')), ''),
                    NULLIF(TRIM(COALESCE(gu.first_name, '') || ' ' || COALESCE(gu.last_name, '')), ''),
                    gu.email,
                    'General User'
                ) AS general_user_name,

                (
                    SELECT m.message_text
                    FROM messages m
                    WHERE m.conversation_id = c.conversation_id
                    ORDER BY m.sent_at DESC
                    LIMIT 1
                ) AS last_message,

                (
                    SELECT m.sent_at
                    FROM messages m
                    WHERE m.conversation_id = c.conversation_id
                    ORDER BY m.sent_at DESC
                    LIMIT 1
                ) AS last_message_time

            FROM conversations c
            JOIN organisations o
                ON o.organisation_id = c.organisation_id
            JOIN users gu
                ON gu.user_id = c.user_id

            WHERE c.user_id = :user_id
               OR o.owner_user_id = :user_id

            ORDER BY COALESCE(c.last_message_at, c.created_at) DESC;
        """),
        {"user_id": user_id}
    )

    conversations = []

    for row in result:
        conversations.append({
            "conversation_id": row.conversation_id,
            "general_user_id": row.general_user_id,
            "general_user_name": row.general_user_name,
            "organisation_id": row.organisation_id,
            "organisation_name": row.organisation_name,
            "organisation_type": row.organisation_type,
            "owner_user_id": row.owner_user_id,
            "last_message": row.last_message,
            "last_message_time": format_datetime(row.last_message_time),
            "created_at": format_datetime(row.created_at),
            "last_message_at": format_datetime(row.last_message_at)
        })

    return jsonify(conversations), 200


@message_bp.route("/conversation/<int:conversation_id>", methods=["GET"])
def get_messages_by_conversation(conversation_id):
    """
    Loads one full conversation by conversation_id.
    user_id is required so users cannot open conversations that do not belong to them.
    """
    user_id = request.args.get("user_id", type=int)

    if not user_id:
        return jsonify(error="user_id is required"), 400

    conversation = db.session.execute(
        text("""
            SELECT
                c.conversation_id,
                c.user_id AS general_user_id,
                c.organisation_id,
                c.created_at,
                c.last_message_at,

                o.organisation_name,
                o.organisation_type,
                o.owner_user_id,

                COALESCE(
                    NULLIF(TRIM(COALESCE(gu.display_name, '')), ''),
                    NULLIF(TRIM(COALESCE(gu.first_name, '') || ' ' || COALESCE(gu.last_name, '')), ''),
                    gu.email,
                    'General User'
                ) AS general_user_name

            FROM conversations c
            JOIN organisations o
                ON o.organisation_id = c.organisation_id
            JOIN users gu
                ON gu.user_id = c.user_id
            WHERE c.conversation_id = :conversation_id;
        """),
        {"conversation_id": conversation_id}
    ).fetchone()

    if not conversation:
        return jsonify(error="Conversation not found"), 404

    allowed = (
        conversation.general_user_id == user_id
        or conversation.owner_user_id == user_id
    )

    if not allowed:
        return jsonify(error="You do not have permission to view this conversation"), 403

    result = db.session.execute(
        text("""
            SELECT
                m.message_id,
                m.conversation_id,
                m.sender_user_id,
                COALESCE(
                    NULLIF(TRIM(COALESCE(u.display_name, '')), ''),
                    NULLIF(TRIM(COALESCE(u.first_name, '') || ' ' || COALESCE(u.last_name, '')), ''),
                    u.email,
                    'User'
                ) AS sender_name,
                m.message_text,
                m.sent_at,
                m.is_read
            FROM messages m
            JOIN users u
                ON u.user_id = m.sender_user_id
            WHERE m.conversation_id = :conversation_id
            ORDER BY m.sent_at ASC;
        """),
        {"conversation_id": conversation_id}
    )

    messages = []

    for row in result:
        messages.append({
            "message_id": row.message_id,
            "conversation_id": row.conversation_id,
            "sender_user_id": row.sender_user_id,
            "sender_name": row.sender_name,
            "message_text": row.message_text,
            "sent_at": format_datetime(row.sent_at),
            "is_read": row.is_read
        })

    return jsonify({
        "conversation": {
            "conversation_id": conversation.conversation_id,
            "general_user_id": conversation.general_user_id,
            "general_user_name": conversation.general_user_name,
            "organisation_id": conversation.organisation_id,
            "organisation_name": conversation.organisation_name,
            "organisation_type": conversation.organisation_type,
            "owner_user_id": conversation.owner_user_id,
            "created_at": format_datetime(conversation.created_at),
            "last_message_at": format_datetime(conversation.last_message_at)
        },
        "messages": messages
    }), 200


@message_bp.route("/send", methods=["POST"])
def send_message():
    """
    Sends a message.

    For a new conversation:
    - sender_user_id
    - organisation_id
    - message_text

    For an existing conversation:
    - sender_user_id
    - conversation_id
    - message_text
    """
    data = request.get_json() or {}

    sender_user_id = data.get("sender_user_id") or data.get("user_id")
    conversation_id = data.get("conversation_id")
    organisation_id = data.get("organisation_id")
    message_text = data.get("message_text", "").strip()

    if not sender_user_id:
        return jsonify(error="sender_user_id is required"), 400

    sender_user_id = int(sender_user_id)

    if not message_text:
        return jsonify(error="message_text is required"), 400

    # Replying inside an existing conversation
    if conversation_id:
        conversation = db.session.execute(
            text("""
                SELECT
                    c.conversation_id,
                    c.user_id AS general_user_id,
                    c.organisation_id,
                    o.owner_user_id
                FROM conversations c
                JOIN organisations o
                    ON o.organisation_id = c.organisation_id
                WHERE c.conversation_id = :conversation_id;
            """),
            {"conversation_id": conversation_id}
        ).fetchone()

        if not conversation:
            return jsonify(error="Conversation not found"), 404

        allowed = (
            conversation.general_user_id == sender_user_id
            or conversation.owner_user_id == sender_user_id
        )

        if not allowed:
            return jsonify(error="You do not have permission to send in this conversation"), 403

    # Starting a new conversation from an organisation page
    else:
        if not organisation_id:
            return jsonify(error="organisation_id is required when starting a new conversation"), 400

        organisation = db.session.execute(
            text("""
                SELECT organisation_id, owner_user_id
                FROM organisations
                WHERE organisation_id = :organisation_id;
            """),
            {"organisation_id": organisation_id}
        ).fetchone()

        if not organisation:
            return jsonify(error="Organisation not found"), 404

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
                "user_id": sender_user_id,
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
                "user_id": sender_user_id,
                "organisation_id": organisation_id
            }
        ).fetchone()

        conversation_id = conversation.conversation_id

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
            "sender_user_id": sender_user_id,
            "message_text": message_text
        }
    )

    db.session.execute(
        text("""
            UPDATE conversations
            SET last_message_at = CURRENT_TIMESTAMP
            WHERE conversation_id = :conversation_id;
        """),
        {"conversation_id": conversation_id}
    )

    db.session.commit()

    return jsonify({
        "message": "Message sent successfully",
        "conversation_id": conversation_id
    }), 201
