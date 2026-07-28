from typing import Optional
import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, Date, DateTime, Double, ForeignKeyConstraint, Index, Integer, JSON, PrimaryKeyConstraint, String, Table, Text, Time, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Categories(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        CheckConstraint("category_type::text = ANY (ARRAY['business'::character varying, 'charity'::character varying, 'both'::character varying]::text[])", name='categories_category_type_check'),
        PrimaryKeyConstraint('category_id', name='categories_pkey')
    )

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(100), nullable=False)
    category_type: Mapped[str] = mapped_column(String(30), nullable=False)

    organisations: Mapped[list['Organisations']] = relationship('Organisations', back_populates='category')
    user_preferences: Mapped[list['UserPreferences']] = relationship('UserPreferences', back_populates='category')
    organisation_categories: Mapped[list['OrganisationCategories']] = relationship('OrganisationCategories', back_populates='category')


class Locations(Base):
    __tablename__ = 'locations'
    __table_args__ = (
        PrimaryKeyConstraint('location_id', name='locations_pkey'),
    )

    location_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    parish: Mapped[Optional[str]] = mapped_column(String(100))
    town: Mapped[Optional[str]] = mapped_column(String(100))
    address: Mapped[Optional[str]] = mapped_column(Text)

    users: Mapped[list['Users']] = relationship('Users', back_populates='location')
    organisations: Mapped[list['Organisations']] = relationship('Organisations', back_populates='location')


t_organisation_login_credentials_view = Table(
    'organisation_login_credentials_view', Base.metadata,
    Column('organisation_id', Integer),
    Column('organisation_name', String(150)),
    Column('organisation_type', String(30)),
    Column('user_id', Integer),
    Column('role_id', Integer),
    Column('display_name', String(150)),
    Column('login_email', String(120)),
    Column('demo_password', String(255)),
    Column('location_id', Integer),
    Column('parish', String(100)),
    Column('town', String(100)),
    Column('created_at', DateTime),
    Column('last_login_at', DateTime)
)


t_organisation_monthly_report_view = Table(
    'organisation_monthly_report_view', Base.metadata,
    Column('organisation_name', String(150)),
    Column('organisation_id', Integer),
    Column('report_month', Integer),
    Column('report_year', Integer),
    Column('total_views', Integer),
    Column('total_saves', Integer),
    Column('total_messages', Integer),
    Column('total_reviews', Integer),
    Column('total_volunteer_signups', Integer),
    Column('average_rating', Double(53)),
    Column('bayesian_rating', Double(53)),
    Column('engagement_score', Double(53)),
    Column('trend_score', Double(53)),
    Column('growth_rate', Double(53)),
    Column('trend_status', String(50)),
    Column('generated_at', DateTime)
)


class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        PrimaryKeyConstraint('role_id', name='roles_pkey'),
        UniqueConstraint('role_name', name='roles_role_name_key')
    )

    role_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_name: Mapped[str] = mapped_column(String(50), nullable=False)

    users: Mapped[list['Users']] = relationship('Users', back_populates='role')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        ForeignKeyConstraint(['location_id'], ['locations.location_id'], ondelete='SET NULL', name='fk_users_location'),
        ForeignKeyConstraint(['role_id'], ['roles.role_id'], name='users_role_id_fkey'),
        PrimaryKeyConstraint('user_id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key')
    )

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(Integer, nullable=False)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    location_id: Mapped[Optional[int]] = mapped_column(Integer)
    last_login_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    display_name: Mapped[Optional[str]] = mapped_column(String(150))

    location: Mapped[Optional['Locations']] = relationship('Locations', back_populates='users')
    role: Mapped['Roles'] = relationship('Roles', back_populates='users')
    organisations: Mapped[list['Organisations']] = relationship('Organisations', back_populates='owner_user')
    user_availability: Mapped[list['UserAvailability']] = relationship('UserAvailability', back_populates='user')
    user_preferences: Mapped[list['UserPreferences']] = relationship('UserPreferences', back_populates='user')
    user_skills: Mapped[list['UserSkills']] = relationship('UserSkills', back_populates='user')
    conversations: Mapped[list['Conversations']] = relationship('Conversations', back_populates='user')
    engagement_logs: Mapped[list['EngagementLogs']] = relationship('EngagementLogs', back_populates='user')
    ratings_reviews: Mapped[list['RatingsReviews']] = relationship('RatingsReviews', back_populates='user')
    saved_organisations: Mapped[list['SavedOrganisations']] = relationship('SavedOrganisations', back_populates='user')
    messages: Mapped[list['Messages']] = relationship('Messages', back_populates='sender_user')
    review_flags: Mapped[list['ReviewFlags']] = relationship('ReviewFlags', back_populates='flagged_by_user')
    volunteer_allocations: Mapped[list['VolunteerAllocations']] = relationship('VolunteerAllocations', back_populates='user')
    volunteer_signups: Mapped[list['VolunteerSignups']] = relationship('VolunteerSignups', back_populates='user')


class Organisations(Base):
    __tablename__ = 'organisations'
    __table_args__ = (
        CheckConstraint("organisation_type::text = ANY (ARRAY['business'::character varying, 'charity'::character varying]::text[])", name='organisations_organisation_type_check'),
        ForeignKeyConstraint(['category_id'], ['categories.category_id'], name='organisations_category_id_fkey'),
        ForeignKeyConstraint(['location_id'], ['locations.location_id'], name='organisations_location_id_fkey'),
        ForeignKeyConstraint(['owner_user_id'], ['users.user_id'], name='organisations_owner_user_id_fkey'),
        PrimaryKeyConstraint('organisation_id', name='organisations_pkey')
    )

    organisation_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    owner_user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    organisation_name: Mapped[str] = mapped_column(String(150), nullable=False)
    organisation_type: Mapped[str] = mapped_column(String(30), nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(Integer)
    location_id: Mapped[Optional[int]] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)
    website_url: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[Optional[str]] = mapped_column(String(120))

    category: Mapped[Optional['Categories']] = relationship('Categories', back_populates='organisations')
    location: Mapped[Optional['Locations']] = relationship('Locations', back_populates='organisations')
    owner_user: Mapped['Users'] = relationship('Users', back_populates='organisations')
    conversations: Mapped[list['Conversations']] = relationship('Conversations', back_populates='organisation')
    engagement_logs: Mapped[list['EngagementLogs']] = relationship('EngagementLogs', back_populates='organisation')
    monthly_business_reports: Mapped[list['MonthlyBusinessReports']] = relationship('MonthlyBusinessReports', back_populates='organisation')
    organisation_categories: Mapped[list['OrganisationCategories']] = relationship('OrganisationCategories', back_populates='organisation')
    organisation_images: Mapped[list['OrganisationImages']] = relationship('OrganisationImages', back_populates='organisation')
    ratings_reviews: Mapped[list['RatingsReviews']] = relationship('RatingsReviews', back_populates='organisation')
    saved_organisations: Mapped[list['SavedOrganisations']] = relationship('SavedOrganisations', back_populates='organisation')
    volunteer_needs: Mapped[list['VolunteerNeeds']] = relationship('VolunteerNeeds', back_populates='organisation')


class UserAvailability(Base):
    __tablename__ = 'user_availability'
    __table_args__ = (
        CheckConstraint('end_time > start_time', name='valid_availability_time'),
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='user_availability_user_id_fkey'),
        PrimaryKeyConstraint('availability_id', name='user_availability_pkey')
    )

    availability_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    available_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    start_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    end_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)

    user: Mapped['Users'] = relationship('Users', back_populates='user_availability')


class UserFactors(Users):
    __tablename__ = 'user_factors'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='user_factors_user_id_fkey'),
        PrimaryKeyConstraint('user_id', name='user_factors_pkey')
    )

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    factors: Mapped[dict] = mapped_column(JSON, nullable=False)
    trained_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))


class UserPreferences(Base):
    __tablename__ = 'user_preferences'
    __table_args__ = (
        CheckConstraint('preference_weight >= 1::double precision AND preference_weight <= 5::double precision', name='user_preferences_preference_weight_check'),
        ForeignKeyConstraint(['category_id'], ['categories.category_id'], name='user_preferences_category_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='user_preferences_user_id_fkey'),
        PrimaryKeyConstraint('preference_id', name='user_preferences_pkey')
    )

    preference_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    preference_weight: Mapped[Optional[float]] = mapped_column(Double(53), server_default=text('1'))

    category: Mapped['Categories'] = relationship('Categories', back_populates='user_preferences')
    user: Mapped['Users'] = relationship('Users', back_populates='user_preferences')


class UserSkills(Base):
    __tablename__ = 'user_skills'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='user_skills_user_id_fkey'),
        PrimaryKeyConstraint('user_skill_id', name='user_skills_pkey')
    )

    user_skill_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_name: Mapped[str] = mapped_column(String(100), nullable=False)

    user: Mapped['Users'] = relationship('Users', back_populates='user_skills')


class Conversations(Base):
    __tablename__ = 'conversations'
    __table_args__ = (
        ForeignKeyConstraint(['organisation_id'], ['organisations.organisation_id'], name='conversations_organisation_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='conversations_user_id_fkey'),
        PrimaryKeyConstraint('conversation_id', name='conversations_pkey'),
        Index('unique_user_org_conversation', 'user_id', 'organisation_id', unique=True)
    )

    conversation_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    organisation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    last_message_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    organisation: Mapped['Organisations'] = relationship('Organisations', back_populates='conversations')
    user: Mapped['Users'] = relationship('Users', back_populates='conversations')
    messages: Mapped[list['Messages']] = relationship('Messages', back_populates='conversation')


class EngagementLogs(Base):
    __tablename__ = 'engagement_logs'
    __table_args__ = (
        CheckConstraint("engagement_type::text = ANY (ARRAY['profile_view'::character varying, 'save'::character varying, 'message'::character varying, 'rating'::character varying, 'review'::character varying, 'volunteer_signup'::character varying]::text[])", name='engagement_logs_engagement_type_check'),
        ForeignKeyConstraint(['organisation_id'], ['organisations.organisation_id'], name='engagement_logs_organisation_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='engagement_logs_user_id_fkey'),
        PrimaryKeyConstraint('engagement_id', name='engagement_logs_pkey')
    )

    engagement_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    organisation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    engagement_type: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    organisation: Mapped['Organisations'] = relationship('Organisations', back_populates='engagement_logs')
    user: Mapped[Optional['Users']] = relationship('Users', back_populates='engagement_logs')


class MonthlyBusinessReports(Base):
    __tablename__ = 'monthly_business_reports'
    __table_args__ = (
        CheckConstraint('report_month >= 1 AND report_month <= 12', name='monthly_business_reports_report_month_check'),
        ForeignKeyConstraint(['organisation_id'], ['organisations.organisation_id'], name='monthly_business_reports_organisation_id_fkey'),
        PrimaryKeyConstraint('report_id', name='monthly_business_reports_pkey'),
        UniqueConstraint('organisation_id', 'report_month', 'report_year', name='unique_monthly_report'),
        Index('unique_monthly_report_idx', 'organisation_id', 'report_month', 'report_year', unique=True)
    )

    report_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    organisation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    report_month: Mapped[int] = mapped_column(Integer, nullable=False)
    report_year: Mapped[int] = mapped_column(Integer, nullable=False)
    total_views: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    total_saves: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    total_messages: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    total_reviews: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    average_rating: Mapped[Optional[float]] = mapped_column(Double(53))
    bayesian_rating: Mapped[Optional[float]] = mapped_column(Double(53))
    trend_score: Mapped[Optional[float]] = mapped_column(Double(53))
    trend_status: Mapped[Optional[str]] = mapped_column(String(50))
    generated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    engagement_score: Mapped[Optional[float]] = mapped_column(Double(53))
    growth_rate: Mapped[Optional[float]] = mapped_column(Double(53))
    total_volunteer_signups: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))

    organisation: Mapped['Organisations'] = relationship('Organisations', back_populates='monthly_business_reports')


class OrganisationCategories(Base):
    __tablename__ = 'organisation_categories'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['categories.category_id'], ondelete='CASCADE', name='fk_org_category_category'),
        ForeignKeyConstraint(['organisation_id'], ['organisations.organisation_id'], ondelete='CASCADE', name='fk_org_category_organisation'),
        PrimaryKeyConstraint('organisation_category_id', name='organisation_categories_pkey'),
        UniqueConstraint('organisation_id', 'category_id', name='unique_organisation_category')
    )

    organisation_category_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    organisation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)

    category: Mapped['Categories'] = relationship('Categories', back_populates='organisation_categories')
    organisation: Mapped['Organisations'] = relationship('Organisations', back_populates='organisation_categories')


class OrganisationFactors(Organisations):
    __tablename__ = 'organisation_factors'
    __table_args__ = (
        ForeignKeyConstraint(['organisation_id'], ['organisations.organisation_id'], name='organisation_factors_organisation_id_fkey'),
        PrimaryKeyConstraint('organisation_id', name='organisation_factors_pkey')
    )

    organisation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    factors: Mapped[dict] = mapped_column(JSON, nullable=False)
    trained_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))


class OrganisationImages(Base):
    __tablename__ = 'organisation_images'
    __table_args__ = (
        CheckConstraint("image_type::text = ANY (ARRAY['profile'::character varying, 'gallery'::character varying, 'catalogue'::character varying, 'event'::character varying]::text[])", name='organisation_images_image_type_check'),
        ForeignKeyConstraint(['organisation_id'], ['organisations.organisation_id'], name='organisation_images_organisation_id_fkey'),
        PrimaryKeyConstraint('image_id', name='organisation_images_pkey')
    )

    image_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    organisation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    image_type: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'gallery'::character varying"))
    uploaded_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    organisation: Mapped['Organisations'] = relationship('Organisations', back_populates='organisation_images')


class RatingsReviews(Base):
    __tablename__ = 'ratings_reviews'
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='ratings_reviews_rating_check'),
        ForeignKeyConstraint(['organisation_id'], ['organisations.organisation_id'], name='ratings_reviews_organisation_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='ratings_reviews_user_id_fkey'),
        PrimaryKeyConstraint('review_id', name='ratings_reviews_pkey')
    )

    review_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    organisation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    review_text: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    is_hidden: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    organisation: Mapped['Organisations'] = relationship('Organisations', back_populates='ratings_reviews')
    user: Mapped['Users'] = relationship('Users', back_populates='ratings_reviews')
    review_flags: Mapped[list['ReviewFlags']] = relationship('ReviewFlags', back_populates='review')


class SavedOrganisations(Base):
    __tablename__ = 'saved_organisations'
    __table_args__ = (
        ForeignKeyConstraint(['organisation_id'], ['organisations.organisation_id'], name='saved_organisations_organisation_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='saved_organisations_user_id_fkey'),
        PrimaryKeyConstraint('saved_id', name='saved_organisations_pkey'),
        Index('unique_user_saved_org', 'user_id', 'organisation_id', unique=True)
    )

    saved_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    organisation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    saved_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    organisation: Mapped['Organisations'] = relationship('Organisations', back_populates='saved_organisations')
    user: Mapped['Users'] = relationship('Users', back_populates='saved_organisations')


class VolunteerNeeds(Base):
    __tablename__ = 'volunteer_needs'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['open'::character varying, 'closed'::character varying, 'cancelled'::character varying]::text[])", name='volunteer_needs_status_check'),
        CheckConstraint("urgency_level::text = ANY (ARRAY['low'::character varying, 'medium'::character varying, 'high'::character varying]::text[])", name='volunteer_needs_urgency_level_check'),
        ForeignKeyConstraint(['organisation_id'], ['organisations.organisation_id'], name='volunteer_needs_organisation_id_fkey'),
        PrimaryKeyConstraint('volunteer_need_id', name='volunteer_needs_pkey')
    )

    volunteer_need_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    organisation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    urgency_level: Mapped[Optional[str]] = mapped_column(String(30))
    status: Mapped[Optional[str]] = mapped_column(String(30), server_default=text("'open'::character varying"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    needed_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    start_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    end_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    volunteers_needed: Mapped[Optional[int]] = mapped_column(Integer)

    organisation: Mapped['Organisations'] = relationship('Organisations', back_populates='volunteer_needs')
    volunteer_allocations: Mapped[list['VolunteerAllocations']] = relationship('VolunteerAllocations', back_populates='volunteer_need')
    volunteer_required_skills: Mapped[list['VolunteerRequiredSkills']] = relationship('VolunteerRequiredSkills', back_populates='volunteer_need')
    volunteer_signups: Mapped[list['VolunteerSignups']] = relationship('VolunteerSignups', back_populates='volunteer_need')


class Messages(Base):
    __tablename__ = 'messages'
    __table_args__ = (
        ForeignKeyConstraint(['conversation_id'], ['conversations.conversation_id'], name='messages_conversation_id_fkey'),
        ForeignKeyConstraint(['sender_user_id'], ['users.user_id'], name='messages_sender_user_id_fkey'),
        PrimaryKeyConstraint('message_id', name='messages_pkey')
    )

    message_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sender_user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    conversation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    message_text: Mapped[Optional[str]] = mapped_column(Text)
    sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    is_read: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    encrypted_message_text: Mapped[Optional[str]] = mapped_column(Text)

    conversation: Mapped['Conversations'] = relationship('Conversations', back_populates='messages')
    sender_user: Mapped['Users'] = relationship('Users', back_populates='messages')


class ReviewFlags(Base):
    __tablename__ = 'review_flags'
    __table_args__ = (
        ForeignKeyConstraint(['flagged_by_user_id'], ['users.user_id'], name='review_flags_flagged_by_user_id_fkey'),
        ForeignKeyConstraint(['review_id'], ['ratings_reviews.review_id'], name='review_flags_review_id_fkey'),
        PrimaryKeyConstraint('flag_id', name='review_flags_pkey')
    )

    flag_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    review_id: Mapped[int] = mapped_column(Integer, nullable=False)
    flagged_by_user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    flagged_by_user: Mapped['Users'] = relationship('Users', back_populates='review_flags')
    review: Mapped['RatingsReviews'] = relationship('RatingsReviews', back_populates='review_flags')


class VolunteerAllocations(Base):
    __tablename__ = 'volunteer_allocations'
    __table_args__ = (
        CheckConstraint("allocation_status::text = ANY (ARRAY['pending'::character varying, 'allocated'::character varying, 'accepted'::character varying, 'rejected'::character varying, 'completed'::character varying, 'cancelled'::character varying]::text[])", name='volunteer_allocations_allocation_status_check'),
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='volunteer_allocations_user_id_fkey'),
        ForeignKeyConstraint(['volunteer_need_id'], ['volunteer_needs.volunteer_need_id'], name='volunteer_allocations_volunteer_need_id_fkey'),
        PrimaryKeyConstraint('allocation_id', name='volunteer_allocations_pkey')
    )

    allocation_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    volunteer_need_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    matching_score: Mapped[Optional[float]] = mapped_column(Double(53))
    allocation_status: Mapped[Optional[str]] = mapped_column(String(30), server_default=text("'recommended'::character varying"))
    allocated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped['Users'] = relationship('Users', back_populates='volunteer_allocations')
    volunteer_need: Mapped['VolunteerNeeds'] = relationship('VolunteerNeeds', back_populates='volunteer_allocations')


class VolunteerRequiredSkills(Base):
    __tablename__ = 'volunteer_required_skills'
    __table_args__ = (
        ForeignKeyConstraint(['volunteer_need_id'], ['volunteer_needs.volunteer_need_id'], name='volunteer_required_skills_volunteer_need_id_fkey'),
        PrimaryKeyConstraint('required_skill_id', name='volunteer_required_skills_pkey')
    )

    required_skill_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    volunteer_need_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_name: Mapped[str] = mapped_column(String(100), nullable=False)

    volunteer_need: Mapped['VolunteerNeeds'] = relationship('VolunteerNeeds', back_populates='volunteer_required_skills')


class VolunteerSignups(Base):
    __tablename__ = 'volunteer_signups'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['pending'::character varying, 'approved'::character varying, 'rejected'::character varying, 'cancelled'::character varying]::text[])", name='volunteer_signups_status_check'),
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='volunteer_signups_user_id_fkey'),
        ForeignKeyConstraint(['volunteer_need_id'], ['volunteer_needs.volunteer_need_id'], name='volunteer_signups_volunteer_need_id_fkey'),
        PrimaryKeyConstraint('signup_id', name='volunteer_signups_pkey')
    )

    signup_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    volunteer_need_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[Optional[str]] = mapped_column(String(30), server_default=text("'pending'::character varying"))
    signed_up_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    user: Mapped['Users'] = relationship('Users', back_populates='volunteer_signups')
    volunteer_need: Mapped['VolunteerNeeds'] = relationship('VolunteerNeeds', back_populates='volunteer_signups')
