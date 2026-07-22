from datetime import datetime
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Conversation, Message

message_bp = Blueprint("message_bp", __name__)

@message_bp.route("/conversations", methods=["POST"])
def create_or_get_conversation():
    data = request.get_json() or {}

    conversation = Conversation.query.filter_by(
        user_id=data.get("user_id"),
        organisation_id=data.get("organisation_id")
    ).first()

    if not conversation:
        conversation = Conversation(
            user_id=data.get("user_id"),
            organisation_id=data.get("organisation_id")
        )
        db.session.add(conversation)
        db.session.commit()

    return jsonify(conversation.to_dict())

@message_bp.route("", methods=["POST"])
def send_message():
    data = request.get_json() or {}

    message = Message(
        conversation_id=data.get("conversation_id"),
        sender_user_id=data.get("sender_user_id"),
        message_text=data.get("message_text"),
        encrypted_message_text=data.get("encrypted_message_text")
    )

    conversation = Conversation.query.get(data.get("conversation_id"))
    if conversation:
        conversation.last_message_at = datetime.utcnow()

    db.session.add(message)
    db.session.commit()

    return jsonify(message="Message sent", data=message.to_dict()), 201
