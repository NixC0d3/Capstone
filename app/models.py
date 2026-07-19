from datetime import datetime
from .extensions import db

class SerializerMixin:
    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if hasattr(value, "isoformat"):
                value = value.isoformat()
            result[column.name] = value
        return result

class Role(db.Model, SerializerMixin):
    __tablename__ = "roles"

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship("User", backref="role", lazy=True)

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.role_id"), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model, SerializerMixin):
    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    category_type = db.Column(db.String(30), nullable=False)  # business, charity, both

class Location(db.Model, SerializerMixin):
    __tablename__ = "locations"

    location_id = db.Column(db.Integer, primary_key=True)
    parish = db.Column(db.String(100), nullable=True)
    town = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

class Organisation(db.Model, SerializerMixin):
    __tablename__ = "organisations"

    organisation_id = db.Column(db.Integer, primary_key=True)
    owner_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"), nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=True)
    organisation_name = db.Column(db.String(150), nullable=False)
    organisation_type = db.Column(db.String(30), nullable=False)  # business or charity
    description = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    website_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owner = db.relationship("User", backref="owned_organisations", lazy=True)
    category = db.relationship("Category", backref="organisations", lazy=True)
    location = db.relationship("Location", backref="organisations", lazy=True)

class OrganisationImage(db.Model, SerializerMixin):
    __tablename__ = "organisation_images"

    image_id = db.Column(db.Integer, primary_key=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey("organisations.organisation_id"), nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    image_type = db.Column(db.String(50), default="gallery")
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class RatingReview(db.Model, SerializerMixin):
    __tablename__ = "ratings_reviews"

    review_id = db.Column(db.Integer, primary_key=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey("organisations.organisation_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=True)
    is_hidden = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ReviewFlag(db.Model, SerializerMixin):
    __tablename__ = "review_flags"

    flag_id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey("ratings_reviews.review_id"), nullable=False)
    flagged_by_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SavedOrganisation(db.Model, SerializerMixin):
    __tablename__ = "saved_organisations"

    saved_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    organisation_id = db.Column(db.Integer, db.ForeignKey("organisations.organisation_id"), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

class EngagementLog(db.Model, SerializerMixin):
    __tablename__ = "engagement_logs"

    engagement_id = db.Column(db.Integer, primary_key=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey("organisations.organisation_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    engagement_type = db.Column(db.String(50), nullable=False)  # view, save, message, rating, volunteer_signup
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserPreference(db.Model, SerializerMixin):
    __tablename__ = "user_preferences"

    preference_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"), nullable=False)
    preference_weight = db.Column(db.Float, default=1.0)

class Conversation(db.Model, SerializerMixin):
    __tablename__ = "conversations"

    conversation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    organisation_id = db.Column(db.Integer, db.ForeignKey("organisations.organisation_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_message_at = db.Column(db.DateTime, nullable=True)

class Message(db.Model, SerializerMixin):
    __tablename__ = "messages"

    message_id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.conversation_id"), nullable=False)
    sender_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    message_text = db.Column(db.Text, nullable=True)
    encrypted_message_text = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

class VolunteerNeed(db.Model, SerializerMixin):
    __tablename__ = "volunteer_needs"

    volunteer_need_id = db.Column(db.Integer, primary_key=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey("organisations.organisation_id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    needed_date = db.Column(db.Date, nullable=True)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    urgency_level = db.Column(db.String(30), default="medium")
    volunteers_needed = db.Column(db.Integer, default=1)
    status = db.Column(db.String(30), default="open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class VolunteerRequiredSkill(db.Model, SerializerMixin):
    __tablename__ = "volunteer_required_skills"

    required_skill_id = db.Column(db.Integer, primary_key=True)
    volunteer_need_id = db.Column(db.Integer, db.ForeignKey("volunteer_needs.volunteer_need_id"), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)

class VolunteerSignup(db.Model, SerializerMixin):
    __tablename__ = "volunteer_signups"

    signup_id = db.Column(db.Integer, primary_key=True)
    volunteer_need_id = db.Column(db.Integer, db.ForeignKey("volunteer_needs.volunteer_need_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    status = db.Column(db.String(30), default="pending")
    signed_up_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserSkill(db.Model, SerializerMixin):
    __tablename__ = "user_skills"

    user_skill_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)

class UserAvailability(db.Model, SerializerMixin):
    __tablename__ = "user_availability"

    availability_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    available_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

class VolunteerAllocation(db.Model, SerializerMixin):
    __tablename__ = "volunteer_allocations"

    allocation_id = db.Column(db.Integer, primary_key=True)
    volunteer_need_id = db.Column(db.Integer, db.ForeignKey("volunteer_needs.volunteer_need_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    matching_score = db.Column(db.Float, nullable=True)
    allocation_status = db.Column(db.String(30), default="recommended")
    allocated_at = db.Column(db.DateTime, default=datetime.utcnow)

class MonthlyBusinessReport(db.Model, SerializerMixin):
    __tablename__ = "monthly_business_reports"

    report_id = db.Column(db.Integer, primary_key=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey("organisations.organisation_id"), nullable=False)
    report_month = db.Column(db.Integer, nullable=False)
    report_year = db.Column(db.Integer, nullable=False)
    total_views = db.Column(db.Integer, default=0)
    total_saves = db.Column(db.Integer, default=0)
    total_messages = db.Column(db.Integer, default=0)
    total_reviews = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float, nullable=True)
    bayesian_rating = db.Column(db.Float, nullable=True)
    engagement_score = db.Column(db.Float, nullable=True)
    trend_score = db.Column(db.Float, nullable=True)
    growth_rate = db.Column(db.Float, nullable=True)
    trend_status = db.Column(db.String(50), nullable=True)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
