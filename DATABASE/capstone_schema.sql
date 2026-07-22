--
-- PostgreSQL database dump
--

\restrict dEYoKzrWh7hSB3SCdiN19cI0FizS5kXiiekpdhZszppd10jmienjahHkeH2OG3d

-- Dumped from database version 17.10 (Debian 17.10-0+deb13u1)
-- Dumped by pg_dump version 17.10 (Debian 17.10-0+deb13u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    category_id integer NOT NULL,
    category_name character varying(100) NOT NULL,
    category_type character varying(30) NOT NULL,
    CONSTRAINT categories_category_type_check CHECK (((category_type)::text = ANY ((ARRAY['business'::character varying, 'charity'::character varying, 'both'::character varying])::text[])))
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: categories_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_category_id_seq OWNER TO postgres;

--
-- Name: categories_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_category_id_seq OWNED BY public.categories.category_id;


--
-- Name: conversations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.conversations (
    conversation_id integer NOT NULL,
    user_id integer NOT NULL,
    organisation_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    last_message_at timestamp without time zone
);


ALTER TABLE public.conversations OWNER TO postgres;

--
-- Name: conversations_conversation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.conversations_conversation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.conversations_conversation_id_seq OWNER TO postgres;

--
-- Name: conversations_conversation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.conversations_conversation_id_seq OWNED BY public.conversations.conversation_id;


--
-- Name: engagement_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.engagement_logs (
    engagement_id integer NOT NULL,
    organisation_id integer NOT NULL,
    user_id integer,
    engagement_type character varying(50) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT engagement_logs_engagement_type_check CHECK (((engagement_type)::text = ANY ((ARRAY['profile_view'::character varying, 'save'::character varying, 'message'::character varying, 'rating'::character varying, 'volunteer_signup'::character varying])::text[])))
);


ALTER TABLE public.engagement_logs OWNER TO postgres;

--
-- Name: engagement_logs_engagement_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.engagement_logs_engagement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.engagement_logs_engagement_id_seq OWNER TO postgres;

--
-- Name: engagement_logs_engagement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.engagement_logs_engagement_id_seq OWNED BY public.engagement_logs.engagement_id;


--
-- Name: locations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.locations (
    location_id integer NOT NULL,
    parish character varying(100),
    town character varying(100),
    address text,
    latitude double precision,
    longitude double precision
);


ALTER TABLE public.locations OWNER TO postgres;

--
-- Name: locations_location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.locations_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.locations_location_id_seq OWNER TO postgres;

--
-- Name: locations_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.locations_location_id_seq OWNED BY public.locations.location_id;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.messages (
    message_id integer NOT NULL,
    sender_user_id integer NOT NULL,
    message_text text,
    sent_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    is_read boolean DEFAULT false,
    conversation_id integer NOT NULL,
    encrypted_message_text text
);


ALTER TABLE public.messages OWNER TO postgres;

--
-- Name: messages_message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.messages_message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.messages_message_id_seq OWNER TO postgres;

--
-- Name: messages_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.messages_message_id_seq OWNED BY public.messages.message_id;


--
-- Name: monthly_business_reports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.monthly_business_reports (
    report_id integer NOT NULL,
    organisation_id integer NOT NULL,
    report_month integer NOT NULL,
    report_year integer NOT NULL,
    total_views integer DEFAULT 0,
    total_saves integer DEFAULT 0,
    total_messages integer DEFAULT 0,
    total_reviews integer DEFAULT 0,
    average_rating double precision,
    bayesian_rating double precision,
    trend_score double precision,
    trend_status character varying(50),
    generated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    engagement_score double precision,
    growth_rate double precision,
    CONSTRAINT monthly_business_reports_report_month_check CHECK (((report_month >= 1) AND (report_month <= 12)))
);


ALTER TABLE public.monthly_business_reports OWNER TO postgres;

--
-- Name: monthly_business_reports_report_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.monthly_business_reports_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.monthly_business_reports_report_id_seq OWNER TO postgres;

--
-- Name: monthly_business_reports_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.monthly_business_reports_report_id_seq OWNED BY public.monthly_business_reports.report_id;


--
-- Name: organisation_images; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organisation_images (
    image_id integer NOT NULL,
    organisation_id integer NOT NULL,
    image_url text NOT NULL,
    image_type character varying(50) DEFAULT 'gallery'::character varying,
    uploaded_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT organisation_images_image_type_check CHECK (((image_type)::text = ANY ((ARRAY['profile'::character varying, 'gallery'::character varying, 'catalogue'::character varying, 'event'::character varying])::text[])))
);


ALTER TABLE public.organisation_images OWNER TO postgres;

--
-- Name: organisation_images_image_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.organisation_images_image_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.organisation_images_image_id_seq OWNER TO postgres;

--
-- Name: organisation_images_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.organisation_images_image_id_seq OWNED BY public.organisation_images.image_id;


--
-- Name: organisations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organisations (
    organisation_id integer NOT NULL,
    owner_user_id integer NOT NULL,
    category_id integer,
    location_id integer,
    organisation_name character varying(150) NOT NULL,
    organisation_type character varying(30) NOT NULL,
    description text,
    website_url character varying(255),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    phone character varying(50),
    email character varying(120),
    CONSTRAINT organisations_organisation_type_check CHECK (((organisation_type)::text = ANY ((ARRAY['business'::character varying, 'charity'::character varying])::text[])))
);


ALTER TABLE public.organisations OWNER TO postgres;

--
-- Name: organisations_organisation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.organisations_organisation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.organisations_organisation_id_seq OWNER TO postgres;

--
-- Name: organisations_organisation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.organisations_organisation_id_seq OWNED BY public.organisations.organisation_id;


--
-- Name: ratings_reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ratings_reviews (
    review_id integer NOT NULL,
    organisation_id integer NOT NULL,
    user_id integer NOT NULL,
    rating integer NOT NULL,
    review_text text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    is_hidden boolean DEFAULT false,
    CONSTRAINT ratings_reviews_rating_check CHECK (((rating >= 1) AND (rating <= 5)))
);


ALTER TABLE public.ratings_reviews OWNER TO postgres;

--
-- Name: ratings_reviews_review_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ratings_reviews_review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ratings_reviews_review_id_seq OWNER TO postgres;

--
-- Name: ratings_reviews_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ratings_reviews_review_id_seq OWNED BY public.ratings_reviews.review_id;


--
-- Name: review_flags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.review_flags (
    flag_id integer NOT NULL,
    review_id integer NOT NULL,
    flagged_by_user_id integer NOT NULL,
    reason text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.review_flags OWNER TO postgres;

--
-- Name: review_flags_flag_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.review_flags_flag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.review_flags_flag_id_seq OWNER TO postgres;

--
-- Name: review_flags_flag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.review_flags_flag_id_seq OWNED BY public.review_flags.flag_id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    role_id integer NOT NULL,
    role_name character varying(50) NOT NULL
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: roles_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_role_id_seq OWNER TO postgres;

--
-- Name: roles_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_role_id_seq OWNED BY public.roles.role_id;


--
-- Name: saved_organisations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.saved_organisations (
    saved_id integer NOT NULL,
    user_id integer NOT NULL,
    organisation_id integer NOT NULL,
    saved_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.saved_organisations OWNER TO postgres;

--
-- Name: saved_organisations_saved_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.saved_organisations_saved_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.saved_organisations_saved_id_seq OWNER TO postgres;

--
-- Name: saved_organisations_saved_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.saved_organisations_saved_id_seq OWNED BY public.saved_organisations.saved_id;


--
-- Name: user_availability; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_availability (
    availability_id integer NOT NULL,
    user_id integer NOT NULL,
    available_date date NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    CONSTRAINT valid_availability_time CHECK ((end_time > start_time))
);


ALTER TABLE public.user_availability OWNER TO postgres;

--
-- Name: user_availability_availability_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_availability_availability_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_availability_availability_id_seq OWNER TO postgres;

--
-- Name: user_availability_availability_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_availability_availability_id_seq OWNED BY public.user_availability.availability_id;


--
-- Name: user_preferences; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_preferences (
    preference_id integer NOT NULL,
    user_id integer NOT NULL,
    category_id integer NOT NULL,
    preference_weight double precision DEFAULT 1,
    CONSTRAINT user_preferences_preference_weight_check CHECK (((preference_weight >= (1)::double precision) AND (preference_weight <= (5)::double precision)))
);


ALTER TABLE public.user_preferences OWNER TO postgres;

--
-- Name: user_preferences_preference_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_preferences_preference_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_preferences_preference_id_seq OWNER TO postgres;

--
-- Name: user_preferences_preference_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_preferences_preference_id_seq OWNED BY public.user_preferences.preference_id;


--
-- Name: user_skills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_skills (
    user_skill_id integer NOT NULL,
    user_id integer NOT NULL,
    skill_name character varying(100) NOT NULL
);


ALTER TABLE public.user_skills OWNER TO postgres;

--
-- Name: user_skills_user_skill_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_skills_user_skill_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_skills_user_skill_id_seq OWNER TO postgres;

--
-- Name: user_skills_user_skill_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_skills_user_skill_id_seq OWNED BY public.user_skills.user_skill_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    role_id integer NOT NULL,
    first_name character varying(80) NOT NULL,
    last_name character varying(80) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(255),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: volunteer_allocations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.volunteer_allocations (
    allocation_id integer NOT NULL,
    volunteer_need_id integer NOT NULL,
    user_id integer NOT NULL,
    matching_score double precision,
    allocation_status character varying(30) DEFAULT 'recommended'::character varying,
    allocated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT volunteer_allocations_allocation_status_check CHECK (((allocation_status)::text = ANY ((ARRAY['recommended'::character varying, 'accepted'::character varying, 'declined'::character varying, 'cancelled'::character varying])::text[])))
);


ALTER TABLE public.volunteer_allocations OWNER TO postgres;

--
-- Name: volunteer_allocations_allocation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.volunteer_allocations_allocation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.volunteer_allocations_allocation_id_seq OWNER TO postgres;

--
-- Name: volunteer_allocations_allocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.volunteer_allocations_allocation_id_seq OWNED BY public.volunteer_allocations.allocation_id;


--
-- Name: volunteer_needs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.volunteer_needs (
    volunteer_need_id integer NOT NULL,
    organisation_id integer NOT NULL,
    title character varying(150) NOT NULL,
    description text,
    urgency_level character varying(30),
    status character varying(30) DEFAULT 'open'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    needed_date date,
    start_time time without time zone,
    end_time time without time zone,
    volunteers_needed integer,
    CONSTRAINT volunteer_needs_status_check CHECK (((status)::text = ANY ((ARRAY['open'::character varying, 'closed'::character varying, 'cancelled'::character varying])::text[]))),
    CONSTRAINT volunteer_needs_urgency_level_check CHECK (((urgency_level)::text = ANY ((ARRAY['low'::character varying, 'medium'::character varying, 'high'::character varying])::text[])))
);


ALTER TABLE public.volunteer_needs OWNER TO postgres;

--
-- Name: volunteer_needs_volunteer_need_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.volunteer_needs_volunteer_need_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.volunteer_needs_volunteer_need_id_seq OWNER TO postgres;

--
-- Name: volunteer_needs_volunteer_need_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.volunteer_needs_volunteer_need_id_seq OWNED BY public.volunteer_needs.volunteer_need_id;


--
-- Name: volunteer_required_skills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.volunteer_required_skills (
    required_skill_id integer NOT NULL,
    volunteer_need_id integer NOT NULL,
    skill_name character varying(100) NOT NULL
);


ALTER TABLE public.volunteer_required_skills OWNER TO postgres;

--
-- Name: volunteer_required_skills_required_skill_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.volunteer_required_skills_required_skill_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.volunteer_required_skills_required_skill_id_seq OWNER TO postgres;

--
-- Name: volunteer_required_skills_required_skill_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.volunteer_required_skills_required_skill_id_seq OWNED BY public.volunteer_required_skills.required_skill_id;


--
-- Name: volunteer_signups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.volunteer_signups (
    signup_id integer NOT NULL,
    volunteer_need_id integer NOT NULL,
    user_id integer NOT NULL,
    status character varying(30) DEFAULT 'pending'::character varying,
    signed_up_at timestamp without time zone,
    CONSTRAINT volunteer_signups_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'approved'::character varying, 'rejected'::character varying, 'cancelled'::character varying])::text[])))
);


ALTER TABLE public.volunteer_signups OWNER TO postgres;

--
-- Name: volunteer_signups_signup_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.volunteer_signups_signup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.volunteer_signups_signup_id_seq OWNER TO postgres;

--
-- Name: volunteer_signups_signup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.volunteer_signups_signup_id_seq OWNED BY public.volunteer_signups.signup_id;


--
-- Name: categories category_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN category_id SET DEFAULT nextval('public.categories_category_id_seq'::regclass);


--
-- Name: conversations conversation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conversations ALTER COLUMN conversation_id SET DEFAULT nextval('public.conversations_conversation_id_seq'::regclass);


--
-- Name: engagement_logs engagement_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.engagement_logs ALTER COLUMN engagement_id SET DEFAULT nextval('public.engagement_logs_engagement_id_seq'::regclass);


--
-- Name: locations location_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations ALTER COLUMN location_id SET DEFAULT nextval('public.locations_location_id_seq'::regclass);


--
-- Name: messages message_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages ALTER COLUMN message_id SET DEFAULT nextval('public.messages_message_id_seq'::regclass);


--
-- Name: monthly_business_reports report_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monthly_business_reports ALTER COLUMN report_id SET DEFAULT nextval('public.monthly_business_reports_report_id_seq'::regclass);


--
-- Name: organisation_images image_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organisation_images ALTER COLUMN image_id SET DEFAULT nextval('public.organisation_images_image_id_seq'::regclass);


--
-- Name: organisations organisation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organisations ALTER COLUMN organisation_id SET DEFAULT nextval('public.organisations_organisation_id_seq'::regclass);


--
-- Name: ratings_reviews review_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ratings_reviews ALTER COLUMN review_id SET DEFAULT nextval('public.ratings_reviews_review_id_seq'::regclass);


--
-- Name: review_flags flag_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review_flags ALTER COLUMN flag_id SET DEFAULT nextval('public.review_flags_flag_id_seq'::regclass);


--
-- Name: roles role_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN role_id SET DEFAULT nextval('public.roles_role_id_seq'::regclass);


--
-- Name: saved_organisations saved_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saved_organisations ALTER COLUMN saved_id SET DEFAULT nextval('public.saved_organisations_saved_id_seq'::regclass);


--
-- Name: user_availability availability_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_availability ALTER COLUMN availability_id SET DEFAULT nextval('public.user_availability_availability_id_seq'::regclass);


--
-- Name: user_preferences preference_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_preferences ALTER COLUMN preference_id SET DEFAULT nextval('public.user_preferences_preference_id_seq'::regclass);


--
-- Name: user_skills user_skill_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_skills ALTER COLUMN user_skill_id SET DEFAULT nextval('public.user_skills_user_skill_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Name: volunteer_allocations allocation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volunteer_allocations ALTER COLUMN allocation_id SET DEFAULT nextval('public.volunteer_allocations_allocation_id_seq'::regclass);


--
-- Name: volunteer_needs volunteer_need_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volunteer_needs ALTER COLUMN volunteer_need_id SET DEFAULT nextval('public.volunteer_needs_volunteer_need_id_seq'::regclass);


--
-- Name: volunteer_required_skills required_skill_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volunteer_required_skills ALTER COLUMN required_skill_id SET DEFAULT nextval('public.volunteer_required_skills_required_skill_id_seq'::regclass);


--
-- Name: volunteer_signups signup_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volunteer_signups ALTER COLUMN signup_id SET DEFAULT nextval('public.volunteer_signups_signup_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_id);


--
-- Name: conversations conversations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_pkey PRIMARY KEY (conversation_id);


--
-- Name: engagement_logs engagement_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.engagement_logs
    ADD CONSTRAINT engagement_logs_pkey PRIMARY KEY (engagement_id);


--
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (location_id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (message_id);


--
-- Name: monthly_business_reports monthly_business_reports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monthly_business_reports
    ADD CONSTRAINT monthly_business_reports_pkey PRIMARY KEY (report_id);


--
-- Name: organisation_images organisation_images_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organisation_images
    ADD CONSTRAINT organisation_images_pkey PRIMARY KEY (image_id);


--
-- Name: organisations organisations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organisations
    ADD CONSTRAINT organisations_pkey PRIMARY KEY (organisation_id);


--
-- Name: ratings_reviews ratings_reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ratings_reviews
    ADD CONSTRAINT ratings_reviews_pkey PRIMARY KEY (review_id);


--
-- Name: review_flags review_flags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review_flags
    ADD CONSTRAINT review_flags_pkey PRIMARY KEY (flag_id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role_id);


--
-- Name: roles roles_role_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_role_name_key UNIQUE (role_name);


--
-- Name: saved_organisations saved_organisations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saved_organisations
    ADD CONSTRAINT saved_organisations_pkey PRIMARY KEY (saved_id);


--
-- Name: user_availability user_availability_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_availability
    ADD CONSTRAINT user_availability_pkey PRIMARY KEY (availability_id);


--
-- Name: user_preferences user_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_pkey PRIMARY KEY (preference_id);


--
-- Name: user_skills user_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_skills
    ADD CONSTRAINT user_skills_pkey PRIMARY KEY (user_skill_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: volunteer_allocations volunteer_allocations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volunteer_allocations
    ADD CONSTRAINT volunteer_allocations_pkey PRIMARY KEY (allocation_id);


--
-- Name: volunteer_needs volunteer_needs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volunteer_needs
    ADD CONSTRAINT volunteer_needs_pkey PRIMARY KEY (volunteer_need_id);


--
-- Name: volunteer_required_skills volunteer_required_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volunteer_required_skills
    ADD CONSTRAINT volunteer_required_skills_pkey PRIMARY KEY (required_skill_id);


--
-- Name: volunteer_signups volunteer_signups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volunteer_signups
    ADD CONSTRAINT volunteer_signups_pkey PRIMARY KEY (signup_id);


--
-- Name: conversations conversations_organisation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id);


--
-- Name: conversations conversations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: engagement_logs engagement_logs_organisation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.engagement_logs
    ADD CONSTRAINT engagement_logs_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id);


--
-- Name: engagement_logs engagement_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.engagement_logs
    ADD CONSTRAINT engagement_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: messages messages_conversation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_conversation_id_fkey FOREIGN KEY (conversation_id) REFERENCES public.conversations(conversation_id);


--
-- Name: messages messages_sender_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_sender_user_id_fkey FOREIGN KEY (sender_user_id) REFERENCES public.users(user_id);


--
-- Name: monthly_business_reports monthly_business_reports_organisation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monthly_business_reports
    ADD CONSTRAINT monthly_business_reports_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id);


--
-- Name: organisation_images organisation_images_organisation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organisation_images
    ADD CONSTRAINT organisation_images_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id);


--
-- Name: organisations organisations_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organisations
    ADD CONSTRAINT organisations_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(category_id);


--
-- Name: organisations organisations_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organisations
    ADD CONSTRAINT organisations_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.locations(location_id);


--
-- Name: organisations organisations_owner_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organisations
    ADD CONSTRAINT organisations_owner_user_id_fkey FOREIGN KEY (owner_user_id) REFERENCES public.users(user_id);


--
-- Name: ratings_reviews ratings_reviews_organisation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ratings_reviews
    ADD CONSTRAINT ratings_reviews_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id);


--
-- Name: ratings_reviews ratings_reviews_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ratings_reviews
    ADD CONSTRAINT ratings_reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: review_flags review_flags_flagged_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review_flags
    ADD CONSTRAINT review_flags_flagged_by_user_id_fkey FOREIGN KEY (flagged_by_user_id) REFERENCES public.users(user_id);


--
-- Name: review_flags review_flags_review_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review_flags
    ADD CONSTRAINT review_flags_review_id_fkey FOREIGN KEY (review_id) REFERENCES public.ratings_reviews(review_id);


--
-- Name: saved_organisations saved_organisations_organisation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saved_organisations
    ADD CONSTRAINT saved_organisations_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id);


--
-- Name: saved_organisations saved_organisations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saved_organisations
    ADD CONSTRAINT saved_organisations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_availability user_availability_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_availability
    ADD CONSTRAINT user_availability_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_preferences user_preferences_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(category_id);


--
-- Name: user_preferences user_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_skills user_skills_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_skills
    ADD CONSTRAINT user_skills_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(role_id);


--
-- Name: volunteer_allocations volunteer_allocations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volunteer_allocations
    ADD CONSTRAINT volunteer_allocations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: volunteer_allocations volunteer_allocations_volunteer_need_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volunteer_allocations
    ADD CONSTRAINT volunteer_allocations_volunteer_need_id_fkey FOREIGN KEY (volunteer_need_id) REFERENCES public.volunteer_needs(volunteer_need_id);


--
-- Name: volunteer_needs volunteer_needs_organisation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volunteer_needs
    ADD CONSTRAINT volunteer_needs_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id);


--
-- Name: volunteer_required_skills volunteer_required_skills_volunteer_need_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volunteer_required_skills
    ADD CONSTRAINT volunteer_required_skills_volunteer_need_id_fkey FOREIGN KEY (volunteer_need_id) REFERENCES public.volunteer_needs(volunteer_need_id);


--
-- Name: volunteer_signups volunteer_signups_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volunteer_signups
    ADD CONSTRAINT volunteer_signups_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: volunteer_signups volunteer_signups_volunteer_need_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volunteer_signups
    ADD CONSTRAINT volunteer_signups_volunteer_need_id_fkey FOREIGN KEY (volunteer_need_id) REFERENCES public.volunteer_needs(volunteer_need_id);


--
-- PostgreSQL database dump complete
--

\unrestrict dEYoKzrWh7hSB3SCdiN19cI0FizS5kXiiekpdhZszppd10jmienjahHkeH2OG3d

