--
-- PostgreSQL database dump
--

\restrict BdZoxhMgwjdZYKRPbVwwDvmBTPHkCRJkcERikXw0gZAnKdIUVgfjzaX6jsj4Mho

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

ALTER TABLE IF EXISTS ONLY public.volunteer_signups DROP CONSTRAINT IF EXISTS volunteer_signups_volunteer_need_id_fkey;
ALTER TABLE IF EXISTS ONLY public.volunteer_signups DROP CONSTRAINT IF EXISTS volunteer_signups_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.volunteer_required_skills DROP CONSTRAINT IF EXISTS volunteer_required_skills_volunteer_need_id_fkey;
ALTER TABLE IF EXISTS ONLY public.volunteer_needs DROP CONSTRAINT IF EXISTS volunteer_needs_organisation_id_fkey;
ALTER TABLE IF EXISTS ONLY public.volunteer_allocations DROP CONSTRAINT IF EXISTS volunteer_allocations_volunteer_need_id_fkey;
ALTER TABLE IF EXISTS ONLY public.volunteer_allocations DROP CONSTRAINT IF EXISTS volunteer_allocations_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_role_id_fkey;
ALTER TABLE IF EXISTS ONLY public.user_skills DROP CONSTRAINT IF EXISTS user_skills_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.user_preferences DROP CONSTRAINT IF EXISTS user_preferences_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.user_preferences DROP CONSTRAINT IF EXISTS user_preferences_category_id_fkey;
ALTER TABLE IF EXISTS ONLY public.user_factors DROP CONSTRAINT IF EXISTS user_factors_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.user_availability DROP CONSTRAINT IF EXISTS user_availability_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.saved_organisations DROP CONSTRAINT IF EXISTS saved_organisations_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.saved_organisations DROP CONSTRAINT IF EXISTS saved_organisations_organisation_id_fkey;
ALTER TABLE IF EXISTS ONLY public.review_flags DROP CONSTRAINT IF EXISTS review_flags_review_id_fkey;
ALTER TABLE IF EXISTS ONLY public.review_flags DROP CONSTRAINT IF EXISTS review_flags_flagged_by_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.ratings_reviews DROP CONSTRAINT IF EXISTS ratings_reviews_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.ratings_reviews DROP CONSTRAINT IF EXISTS ratings_reviews_organisation_id_fkey;
ALTER TABLE IF EXISTS ONLY public.organisations DROP CONSTRAINT IF EXISTS organisations_owner_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.organisations DROP CONSTRAINT IF EXISTS organisations_location_id_fkey;
ALTER TABLE IF EXISTS ONLY public.organisations DROP CONSTRAINT IF EXISTS organisations_category_id_fkey;
ALTER TABLE IF EXISTS ONLY public.organisation_images DROP CONSTRAINT IF EXISTS organisation_images_organisation_id_fkey;
ALTER TABLE IF EXISTS ONLY public.organisation_factors DROP CONSTRAINT IF EXISTS organisation_factors_organisation_id_fkey;
ALTER TABLE IF EXISTS ONLY public.monthly_business_reports DROP CONSTRAINT IF EXISTS monthly_business_reports_organisation_id_fkey;
ALTER TABLE IF EXISTS ONLY public.messages DROP CONSTRAINT IF EXISTS messages_sender_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.messages DROP CONSTRAINT IF EXISTS messages_conversation_id_fkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS fk_users_location;
ALTER TABLE IF EXISTS ONLY public.organisation_categories DROP CONSTRAINT IF EXISTS fk_org_category_organisation;
ALTER TABLE IF EXISTS ONLY public.organisation_categories DROP CONSTRAINT IF EXISTS fk_org_category_category;
ALTER TABLE IF EXISTS ONLY public.engagement_logs DROP CONSTRAINT IF EXISTS engagement_logs_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.engagement_logs DROP CONSTRAINT IF EXISTS engagement_logs_organisation_id_fkey;
ALTER TABLE IF EXISTS ONLY public.conversations DROP CONSTRAINT IF EXISTS conversations_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.conversations DROP CONSTRAINT IF EXISTS conversations_organisation_id_fkey;
DROP TRIGGER IF EXISTS trg_log_save_engagement ON public.saved_organisations;
DROP TRIGGER IF EXISTS trg_log_rating_engagement ON public.ratings_reviews;
DROP TRIGGER IF EXISTS trg_log_message_engagement ON public.messages;
DROP INDEX IF EXISTS public.unique_monthly_report_idx;
ALTER TABLE IF EXISTS ONLY public.volunteer_signups DROP CONSTRAINT IF EXISTS volunteer_signups_pkey;
ALTER TABLE IF EXISTS ONLY public.volunteer_required_skills DROP CONSTRAINT IF EXISTS volunteer_required_skills_pkey;
ALTER TABLE IF EXISTS ONLY public.volunteer_needs DROP CONSTRAINT IF EXISTS volunteer_needs_pkey;
ALTER TABLE IF EXISTS ONLY public.volunteer_allocations DROP CONSTRAINT IF EXISTS volunteer_allocations_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_email_key;
ALTER TABLE IF EXISTS ONLY public.user_skills DROP CONSTRAINT IF EXISTS user_skills_pkey;
ALTER TABLE IF EXISTS ONLY public.user_preferences DROP CONSTRAINT IF EXISTS user_preferences_pkey;
ALTER TABLE IF EXISTS ONLY public.user_factors DROP CONSTRAINT IF EXISTS user_factors_pkey;
ALTER TABLE IF EXISTS ONLY public.user_availability DROP CONSTRAINT IF EXISTS user_availability_pkey;
ALTER TABLE IF EXISTS ONLY public.organisation_categories DROP CONSTRAINT IF EXISTS unique_organisation_category;
ALTER TABLE IF EXISTS ONLY public.monthly_business_reports DROP CONSTRAINT IF EXISTS unique_monthly_report;
ALTER TABLE IF EXISTS ONLY public.saved_organisations DROP CONSTRAINT IF EXISTS saved_organisations_pkey;
ALTER TABLE IF EXISTS ONLY public.roles DROP CONSTRAINT IF EXISTS roles_role_name_key;
ALTER TABLE IF EXISTS ONLY public.roles DROP CONSTRAINT IF EXISTS roles_pkey;
ALTER TABLE IF EXISTS ONLY public.review_flags DROP CONSTRAINT IF EXISTS review_flags_pkey;
ALTER TABLE IF EXISTS ONLY public.ratings_reviews DROP CONSTRAINT IF EXISTS ratings_reviews_pkey;
ALTER TABLE IF EXISTS ONLY public.organisations DROP CONSTRAINT IF EXISTS organisations_pkey;
ALTER TABLE IF EXISTS ONLY public.organisation_images DROP CONSTRAINT IF EXISTS organisation_images_pkey;
ALTER TABLE IF EXISTS ONLY public.organisation_factors DROP CONSTRAINT IF EXISTS organisation_factors_pkey;
ALTER TABLE IF EXISTS ONLY public.organisation_categories DROP CONSTRAINT IF EXISTS organisation_categories_pkey;
ALTER TABLE IF EXISTS ONLY public.monthly_business_reports DROP CONSTRAINT IF EXISTS monthly_business_reports_pkey;
ALTER TABLE IF EXISTS ONLY public.messages DROP CONSTRAINT IF EXISTS messages_pkey;
ALTER TABLE IF EXISTS ONLY public.locations DROP CONSTRAINT IF EXISTS locations_pkey;
ALTER TABLE IF EXISTS ONLY public.engagement_logs DROP CONSTRAINT IF EXISTS engagement_logs_pkey;
ALTER TABLE IF EXISTS ONLY public.conversations DROP CONSTRAINT IF EXISTS conversations_pkey;
ALTER TABLE IF EXISTS ONLY public.categories DROP CONSTRAINT IF EXISTS categories_pkey;
ALTER TABLE IF EXISTS ONLY public.alembic_version DROP CONSTRAINT IF EXISTS alembic_version_pkc;
ALTER TABLE IF EXISTS public.volunteer_signups ALTER COLUMN signup_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.volunteer_required_skills ALTER COLUMN required_skill_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.volunteer_needs ALTER COLUMN volunteer_need_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.volunteer_allocations ALTER COLUMN allocation_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.users ALTER COLUMN user_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.user_skills ALTER COLUMN user_skill_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.user_preferences ALTER COLUMN preference_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.user_availability ALTER COLUMN availability_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.saved_organisations ALTER COLUMN saved_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.roles ALTER COLUMN role_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.review_flags ALTER COLUMN flag_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.ratings_reviews ALTER COLUMN review_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.organisations ALTER COLUMN organisation_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.organisation_images ALTER COLUMN image_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.organisation_categories ALTER COLUMN organisation_category_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.monthly_business_reports ALTER COLUMN report_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.messages ALTER COLUMN message_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.locations ALTER COLUMN location_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.engagement_logs ALTER COLUMN engagement_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.conversations ALTER COLUMN conversation_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.categories ALTER COLUMN category_id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.volunteer_signups_signup_id_seq;
DROP TABLE IF EXISTS public.volunteer_signups;
DROP SEQUENCE IF EXISTS public.volunteer_required_skills_required_skill_id_seq;
DROP TABLE IF EXISTS public.volunteer_required_skills;
DROP SEQUENCE IF EXISTS public.volunteer_needs_volunteer_need_id_seq;
DROP TABLE IF EXISTS public.volunteer_needs;
DROP SEQUENCE IF EXISTS public.volunteer_allocations_allocation_id_seq;
DROP TABLE IF EXISTS public.volunteer_allocations;
DROP SEQUENCE IF EXISTS public.users_user_id_seq;
DROP SEQUENCE IF EXISTS public.user_skills_user_skill_id_seq;
DROP TABLE IF EXISTS public.user_skills;
DROP SEQUENCE IF EXISTS public.user_preferences_preference_id_seq;
DROP TABLE IF EXISTS public.user_preferences;
DROP TABLE IF EXISTS public.user_factors;
DROP SEQUENCE IF EXISTS public.user_availability_availability_id_seq;
DROP TABLE IF EXISTS public.user_availability;
DROP SEQUENCE IF EXISTS public.saved_organisations_saved_id_seq;
DROP TABLE IF EXISTS public.saved_organisations;
DROP SEQUENCE IF EXISTS public.roles_role_id_seq;
DROP TABLE IF EXISTS public.roles;
DROP SEQUENCE IF EXISTS public.review_flags_flag_id_seq;
DROP TABLE IF EXISTS public.review_flags;
DROP SEQUENCE IF EXISTS public.ratings_reviews_review_id_seq;
DROP TABLE IF EXISTS public.ratings_reviews;
DROP SEQUENCE IF EXISTS public.organisations_organisation_id_seq;
DROP VIEW IF EXISTS public.organisation_monthly_report_view;
DROP VIEW IF EXISTS public.organisation_login_credentials_view;
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.organisations;
DROP SEQUENCE IF EXISTS public.organisation_images_image_id_seq;
DROP TABLE IF EXISTS public.organisation_images;
DROP TABLE IF EXISTS public.organisation_factors;
DROP SEQUENCE IF EXISTS public.organisation_categories_organisation_category_id_seq;
DROP TABLE IF EXISTS public.organisation_categories;
DROP SEQUENCE IF EXISTS public.monthly_business_reports_report_id_seq;
DROP TABLE IF EXISTS public.monthly_business_reports;
DROP SEQUENCE IF EXISTS public.messages_message_id_seq;
DROP TABLE IF EXISTS public.messages;
DROP SEQUENCE IF EXISTS public.locations_location_id_seq;
DROP TABLE IF EXISTS public.locations;
DROP SEQUENCE IF EXISTS public.engagement_logs_engagement_id_seq;
DROP TABLE IF EXISTS public.engagement_logs;
DROP SEQUENCE IF EXISTS public.conversations_conversation_id_seq;
DROP TABLE IF EXISTS public.conversations;
DROP SEQUENCE IF EXISTS public.categories_category_id_seq;
DROP TABLE IF EXISTS public.categories;
DROP TABLE IF EXISTS public.alembic_version;
DROP FUNCTION IF EXISTS public.log_save_engagement();
DROP FUNCTION IF EXISTS public.log_rating_engagement();
DROP FUNCTION IF EXISTS public.log_message_engagement();
--
-- Name: log_message_engagement(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.log_message_engagement() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    org_id INT;
BEGIN
    SELECT organisation_id
    INTO org_id
    FROM conversations
    WHERE conversation_id = NEW.conversation_id;

    IF org_id IS NOT NULL THEN
        INSERT INTO engagement_logs
        (
            organisation_id,
            user_id,
            engagement_type,
            created_at
        )
        VALUES
        (
            org_id,
            NEW.sender_user_id,
            'message',
            CURRENT_TIMESTAMP
        );
    END IF;

    RETURN NEW;
END;
$$;


--
-- Name: log_rating_engagement(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.log_rating_engagement() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO engagement_logs
    (
        organisation_id,
        user_id,
        engagement_type,
        created_at
    )
    VALUES
    (
        NEW.organisation_id,
        NEW.user_id,
        'rating',
        CURRENT_TIMESTAMP
    );

    RETURN NEW;
END;
$$;


--
-- Name: log_save_engagement(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.log_save_engagement() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO engagement_logs
    (
        organisation_id,
        user_id,
        engagement_type,
        created_at
    )
    VALUES
    (
        NEW.organisation_id,
        NEW.user_id,
        'save',
        CURRENT_TIMESTAMP
    );

    RETURN NEW;
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.categories (
    category_id integer NOT NULL,
    category_name character varying(100) NOT NULL,
    category_type character varying(30) NOT NULL,
    CONSTRAINT categories_category_type_check CHECK (((category_type)::text = ANY ((ARRAY['business'::character varying, 'charity'::character varying, 'both'::character varying])::text[])))
);


--
-- Name: categories_category_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.categories_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: categories_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.categories_category_id_seq OWNED BY public.categories.category_id;


--
-- Name: conversations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.conversations (
    conversation_id integer NOT NULL,
    user_id integer NOT NULL,
    organisation_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    last_message_at timestamp without time zone
);


--
-- Name: conversations_conversation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.conversations_conversation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: conversations_conversation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.conversations_conversation_id_seq OWNED BY public.conversations.conversation_id;


--
-- Name: engagement_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.engagement_logs (
    engagement_id integer NOT NULL,
    organisation_id integer NOT NULL,
    user_id integer,
    engagement_type character varying(50) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT engagement_logs_engagement_type_check CHECK (((engagement_type)::text = ANY ((ARRAY['profile_view'::character varying, 'save'::character varying, 'message'::character varying, 'rating'::character varying, 'volunteer_signup'::character varying])::text[])))
);


--
-- Name: engagement_logs_engagement_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.engagement_logs_engagement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: engagement_logs_engagement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.engagement_logs_engagement_id_seq OWNED BY public.engagement_logs.engagement_id;


--
-- Name: locations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.locations (
    location_id integer NOT NULL,
    parish character varying(100),
    town character varying(100),
    address text
);


--
-- Name: locations_location_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.locations_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: locations_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.locations_location_id_seq OWNED BY public.locations.location_id;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: messages_message_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.messages_message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: messages_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.messages_message_id_seq OWNED BY public.messages.message_id;


--
-- Name: monthly_business_reports; Type: TABLE; Schema: public; Owner: -
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
    total_volunteer_signups integer DEFAULT 0,
    CONSTRAINT monthly_business_reports_report_month_check CHECK (((report_month >= 1) AND (report_month <= 12)))
);


--
-- Name: monthly_business_reports_report_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.monthly_business_reports_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: monthly_business_reports_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.monthly_business_reports_report_id_seq OWNED BY public.monthly_business_reports.report_id;


--
-- Name: organisation_categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.organisation_categories (
    organisation_category_id integer NOT NULL,
    organisation_id integer NOT NULL,
    category_id integer NOT NULL
);


--
-- Name: organisation_categories_organisation_category_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.organisation_categories_organisation_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: organisation_categories_organisation_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.organisation_categories_organisation_category_id_seq OWNED BY public.organisation_categories.organisation_category_id;


--
-- Name: organisation_factors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.organisation_factors (
    organisation_id integer NOT NULL,
    factors json NOT NULL,
    trained_at timestamp without time zone DEFAULT now()
);


--
-- Name: organisation_images; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.organisation_images (
    image_id integer NOT NULL,
    organisation_id integer NOT NULL,
    image_url text NOT NULL,
    image_type character varying(50) DEFAULT 'gallery'::character varying,
    uploaded_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT organisation_images_image_type_check CHECK (((image_type)::text = ANY ((ARRAY['profile'::character varying, 'gallery'::character varying, 'catalogue'::character varying, 'event'::character varying])::text[])))
);


--
-- Name: organisation_images_image_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.organisation_images_image_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: organisation_images_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.organisation_images_image_id_seq OWNED BY public.organisation_images.image_id;


--
-- Name: organisations; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    role_id integer NOT NULL,
    first_name character varying(80) NOT NULL,
    last_name character varying(80) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(255),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    location_id integer,
    last_login_at timestamp without time zone,
    display_name character varying(150)
);


--
-- Name: organisation_login_credentials_view; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.organisation_login_credentials_view AS
 SELECT o.organisation_id,
    o.organisation_name,
    o.organisation_type,
    u.user_id,
    u.role_id,
    u.display_name,
    u.email AS login_email,
    u.password_hash AS demo_password,
    u.location_id,
    l.parish,
    l.town,
    u.created_at,
    u.last_login_at
   FROM ((public.organisations o
     JOIN public.users u ON ((u.user_id = o.owner_user_id)))
     LEFT JOIN public.locations l ON ((l.location_id = u.location_id)))
  ORDER BY o.organisation_type, o.organisation_name;


--
-- Name: organisation_monthly_report_view; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.organisation_monthly_report_view AS
 SELECT o.organisation_name,
    m.organisation_id,
    m.report_month,
    m.report_year,
    m.total_views,
    m.total_saves,
    m.total_messages,
    m.total_reviews,
    m.total_volunteer_signups,
    m.average_rating,
    m.bayesian_rating,
    m.engagement_score,
    m.trend_score,
    m.growth_rate,
    m.trend_status,
    m.generated_at
   FROM (public.monthly_business_reports m
     JOIN public.organisations o ON ((m.organisation_id = o.organisation_id)));


--
-- Name: organisations_organisation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.organisations_organisation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: organisations_organisation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.organisations_organisation_id_seq OWNED BY public.organisations.organisation_id;


--
-- Name: ratings_reviews; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: ratings_reviews_review_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ratings_reviews_review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ratings_reviews_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ratings_reviews_review_id_seq OWNED BY public.ratings_reviews.review_id;


--
-- Name: review_flags; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.review_flags (
    flag_id integer NOT NULL,
    review_id integer NOT NULL,
    flagged_by_user_id integer NOT NULL,
    reason text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: review_flags_flag_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.review_flags_flag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: review_flags_flag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.review_flags_flag_id_seq OWNED BY public.review_flags.flag_id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    role_id integer NOT NULL,
    role_name character varying(50) NOT NULL
);


--
-- Name: roles_role_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.roles_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: roles_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.roles_role_id_seq OWNED BY public.roles.role_id;


--
-- Name: saved_organisations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.saved_organisations (
    saved_id integer NOT NULL,
    user_id integer NOT NULL,
    organisation_id integer NOT NULL,
    saved_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: saved_organisations_saved_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.saved_organisations_saved_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: saved_organisations_saved_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.saved_organisations_saved_id_seq OWNED BY public.saved_organisations.saved_id;


--
-- Name: user_availability; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_availability (
    availability_id integer NOT NULL,
    user_id integer NOT NULL,
    available_date date NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    CONSTRAINT valid_availability_time CHECK ((end_time > start_time))
);


--
-- Name: user_availability_availability_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_availability_availability_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_availability_availability_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_availability_availability_id_seq OWNED BY public.user_availability.availability_id;


--
-- Name: user_factors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_factors (
    user_id integer NOT NULL,
    factors json NOT NULL,
    trained_at timestamp without time zone DEFAULT now()
);


--
-- Name: user_preferences; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_preferences (
    preference_id integer NOT NULL,
    user_id integer NOT NULL,
    category_id integer NOT NULL,
    preference_weight double precision DEFAULT 1,
    CONSTRAINT user_preferences_preference_weight_check CHECK (((preference_weight >= (1)::double precision) AND (preference_weight <= (5)::double precision)))
);


--
-- Name: user_preferences_preference_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_preferences_preference_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_preferences_preference_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_preferences_preference_id_seq OWNED BY public.user_preferences.preference_id;


--
-- Name: user_skills; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_skills (
    user_skill_id integer NOT NULL,
    user_id integer NOT NULL,
    skill_name character varying(100) NOT NULL
);


--
-- Name: user_skills_user_skill_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_skills_user_skill_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_skills_user_skill_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_skills_user_skill_id_seq OWNED BY public.user_skills.user_skill_id;


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: volunteer_allocations; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: volunteer_allocations_allocation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.volunteer_allocations_allocation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: volunteer_allocations_allocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.volunteer_allocations_allocation_id_seq OWNED BY public.volunteer_allocations.allocation_id;


--
-- Name: volunteer_needs; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: volunteer_needs_volunteer_need_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.volunteer_needs_volunteer_need_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: volunteer_needs_volunteer_need_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.volunteer_needs_volunteer_need_id_seq OWNED BY public.volunteer_needs.volunteer_need_id;


--
-- Name: volunteer_required_skills; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.volunteer_required_skills (
    required_skill_id integer NOT NULL,
    volunteer_need_id integer NOT NULL,
    skill_name character varying(100) NOT NULL
);


--
-- Name: volunteer_required_skills_required_skill_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.volunteer_required_skills_required_skill_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: volunteer_required_skills_required_skill_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.volunteer_required_skills_required_skill_id_seq OWNED BY public.volunteer_required_skills.required_skill_id;


--
-- Name: volunteer_signups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.volunteer_signups (
    signup_id integer NOT NULL,
    volunteer_need_id integer NOT NULL,
    user_id integer NOT NULL,
    status character varying(30) DEFAULT 'pending'::character varying,
    signed_up_at timestamp without time zone,
    CONSTRAINT volunteer_signups_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'approved'::character varying, 'rejected'::character varying, 'cancelled'::character varying])::text[])))
);


--
-- Name: volunteer_signups_signup_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.volunteer_signups_signup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: volunteer_signups_signup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.volunteer_signups_signup_id_seq OWNED BY public.volunteer_signups.signup_id;


--
-- Name: categories category_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories ALTER COLUMN category_id SET DEFAULT nextval('public.categories_category_id_seq'::regclass);


--
-- Name: conversations conversation_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conversations ALTER COLUMN conversation_id SET DEFAULT nextval('public.conversations_conversation_id_seq'::regclass);


--
-- Name: engagement_logs engagement_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.engagement_logs ALTER COLUMN engagement_id SET DEFAULT nextval('public.engagement_logs_engagement_id_seq'::regclass);


--
-- Name: locations location_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations ALTER COLUMN location_id SET DEFAULT nextval('public.locations_location_id_seq'::regclass);


--
-- Name: messages message_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages ALTER COLUMN message_id SET DEFAULT nextval('public.messages_message_id_seq'::regclass);


--
-- Name: monthly_business_reports report_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monthly_business_reports ALTER COLUMN report_id SET DEFAULT nextval('public.monthly_business_reports_report_id_seq'::regclass);


--
-- Name: organisation_categories organisation_category_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisation_categories ALTER COLUMN organisation_category_id SET DEFAULT nextval('public.organisation_categories_organisation_category_id_seq'::regclass);


--
-- Name: organisation_images image_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisation_images ALTER COLUMN image_id SET DEFAULT nextval('public.organisation_images_image_id_seq'::regclass);


--
-- Name: organisations organisation_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisations ALTER COLUMN organisation_id SET DEFAULT nextval('public.organisations_organisation_id_seq'::regclass);


--
-- Name: ratings_reviews review_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ratings_reviews ALTER COLUMN review_id SET DEFAULT nextval('public.ratings_reviews_review_id_seq'::regclass);


--
-- Name: review_flags flag_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.review_flags ALTER COLUMN flag_id SET DEFAULT nextval('public.review_flags_flag_id_seq'::regclass);


--
-- Name: roles role_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles ALTER COLUMN role_id SET DEFAULT nextval('public.roles_role_id_seq'::regclass);


--
-- Name: saved_organisations saved_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saved_organisations ALTER COLUMN saved_id SET DEFAULT nextval('public.saved_organisations_saved_id_seq'::regclass);


--
-- Name: user_availability availability_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_availability ALTER COLUMN availability_id SET DEFAULT nextval('public.user_availability_availability_id_seq'::regclass);


--
-- Name: user_preferences preference_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_preferences ALTER COLUMN preference_id SET DEFAULT nextval('public.user_preferences_preference_id_seq'::regclass);


--
-- Name: user_skills user_skill_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_skills ALTER COLUMN user_skill_id SET DEFAULT nextval('public.user_skills_user_skill_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Name: volunteer_allocations allocation_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.volunteer_allocations ALTER COLUMN allocation_id SET DEFAULT nextval('public.volunteer_allocations_allocation_id_seq'::regclass);


--
-- Name: volunteer_needs volunteer_need_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.volunteer_needs ALTER COLUMN volunteer_need_id SET DEFAULT nextval('public.volunteer_needs_volunteer_need_id_seq'::regclass);


--
-- Name: volunteer_required_skills required_skill_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.volunteer_required_skills ALTER COLUMN required_skill_id SET DEFAULT nextval('public.volunteer_required_skills_required_skill_id_seq'::regclass);


--
-- Name: volunteer_signups signup_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.volunteer_signups ALTER COLUMN signup_id SET DEFAULT nextval('public.volunteer_signups_signup_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
f8e8305670c4
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.categories (category_id, category_name, category_type) FROM stdin;
101	Restaurant	business
102	Beauty	business
103	Arts	business
104	Tech	business
105	HomeCenter	business
106	Retail	business
107	Rental and Planning	business
108	Repair	business
109	Construction	business
110	Dealership and Parts	business
111	Shipping	business
112	Fashion	business
113	Arts and Crafts	business
114	Health	business
115	Wholesale and Grocery	business
116	Marketing	business
118	Finance	business
119	Salon	business
120	Excursion	business
121	Farming	business
122	Social Safety Net Progammes	charity
117	Education	both
123	Climate Change	charity
124	Clean Up	charity
125	Thrifting	charity
126	Food Drives	charity
127	Scholarships	charity
128	Homeless Aid	charity
129	Health Services	charity
130	Faith-Based	charity
\.


--
-- Data for Name: conversations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.conversations (conversation_id, user_id, organisation_id, created_at, last_message_at) FROM stdin;
\.


--
-- Data for Name: engagement_logs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.engagement_logs (engagement_id, organisation_id, user_id, engagement_type, created_at) FROM stdin;
2	159	366	profile_view	2026-05-01 00:00:00
3	159	374	profile_view	2026-05-02 00:00:00
4	159	362	save	2026-05-03 00:00:00
5	159	366	message	2026-05-04 00:00:00
6	159	366	rating	2026-05-05 00:00:00
8	159	2	profile_view	2026-06-02 00:00:00
9	159	3	profile_view	2026-06-03 00:00:00
10	159	2	save	2026-06-04 00:00:00
11	159	3	save	2026-06-05 00:00:00
12	159	3	message	2026-06-06 00:00:00
13	159	2	rating	2026-06-07 00:00:00
14	159	2	volunteer_signup	2026-06-08 00:00:00
7	159	\N	profile_view	2026-06-01 00:00:00
15	203	366	profile_view	2026-07-26 05:53:12.661184
\.


--
-- Data for Name: locations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.locations (location_id, parish, town, address) FROM stdin;
2	St. Catherine	Portmore	George Lee Boulevard, Passage Fort
3	St. Catherine	Spanish Town	10 king street, Spanish Town, Jamaica
4	St. Catherine	Linstead	Lot 210 Charlemont F/S, Linstead, 000000
5	St. Catherine	Spanish Town	Lot 12 Twickenham Park
6	St. Catherine	Spanish Town	25 Old Market Street
7	St. Catherine	Portmore	Lot 2 Naggo Head Industrial Complex
8	St. Catherine	Portmore	6 Cairo Street
9	St. Catherine	Spanish Town	Shop 2 367 Essex Drive Greendale
10	St. Catherine	Portmore	Lot 56 Cookson Avenue Naggo Head Industrial Estate
11	St. Catherine	Spanish Town	St. Jago Shopping Center Burke Road
12	St. Catherine	Portmore	237 Silverstone Greater Portmore
13	St. Catherine	Portmore	6A Portmore Mall
32	St. Ann	Runaway Bay	Main Street, Priory
33	St. Ann	Ocho Rios	2 Market Street
34	St. Ann	St. Ann's Bay	Bravo Street
35	St. Ann	Ocho Rios	5 Newlyn Street
36	St. Ann	Ocho Rios	Ocean Village Shopping Centre
37	St. Ann	Ocho Rios	88 Main Street
38	St. Ann	Ocho Rios	72 Main Street
39	St. Ann	Ocho Rios	Top Road Brown’s Town
40	St. Ann	St. Ann's Bay	9 Harbour Street
41	St. Ann	Ocho Rios	Shop 18 Eight Rivers Towne Centre
42	St. Ann	Ocho Rios	105 Main Street
43	St. Ann	Ocho Rios	Shop 3 Island Plaza
44	St. Ann	Ocho Rios	Shop 12 DaCosta Drive
45	Clarendon	Denbigh	90 Muirhead Avenue
46	Clarendon	Denbigh	Foga Road
47	Clarendon	Denbigh	23 East Street
48	Clarendon	May Pen	3 Mcarthur Avenue
49	Clarendon	May Pen	41 Manchester Avenue
50	Clarendon	May Pen	8 Manchester Avenye
51	Clarendon	May Pen	31 Main Street
52	Clarendon	May Pen	1A Chapelton Road
53	Clarendon	May Pen	36-40 Manchester Avenue
54	Clarendon	May Pen	2-4 Church Street
55	Manchester	Mandeville	Lot 19 Leaders Plaza
56	Manchester	Mandeville	Shop 29 & 30 Mid Way Mall 17 Caledonia Road
57	Manchester	Mandeville	15A Jams Warehouse Complex
58	Manchester	Mandeville	Main St Christiana
59	Manchester	Mandeville	6 Ward Avenue
60	Manchester	Mandeville	Shop 24 Caledonia Plaza
61	Manchester	Mandeville	Main Street Porus
62	Manchester	Mandeville	Shop #3 Global Plaza
63	Manchester	Christiana	Shop 9 Syldian Court
64	Manchester	Mandeville	93 Manchester Road
65	St. Elizabeth	Santa Cruz	113 Main Street
66	St. Elizabeth	Black River	11 High Street
67	St. Elizabeth	Black River	Priestman River
68	St. Elizabeth	Santa Cruz	1 institution Drive
69	St. Elizabeth	Black River	24 Central Road
70	St. Elizabeth	Santa Cruz	Main Street
71	St. Elizabeth	Santa Cruz	2 Brigade Street
72	St. Elizabeth	Santa Cruz	Shop 1b Manifest Plaza
73	St. Elizabeth	Santa Cruz	Shop 25 Phillips Plaza
74	St. Elizabeth	Santa Cruz	79 Main Street
75	Portland	Annotto Bay	Shop 8 Bay Centre Plaza Main Street
76	Portland	Port Antonio	2A Harbour Street
77	Portland	Port Antonio	10 William Street
78	Portland	Port Antonio	Shop 7 Jamaica National Building Plaza Society Plaza 21 Harbour Street
79	Portland	Port Antonio	1 Harbour Street
80	Portland	Port Antonio	11 Harbour Street
81	Portland	Buff Bay	Shop 1A 3 St Georges Street
82	Portland	Port Antonio	1 Allan Avenue
83	Portland	Port Antonio	82 West Street
84	Portland	Port Antonio	18 West Street
85	Portland	Port Antonio	27 West Street
86	St. Thomas	Yallahs	Lot 16 Yallahs Industrial Estate
87	St. Thomas	Yallahs	Lot 52C Albion Parkway
88	St. Thomas	Morant Bay	Shop 14A Morant Bay Shopping Plaza
89	St. Thomas	Port Morant	Leith Hall Main Road
90	St. Thomas	Morant Bay	49 Queens Street
91	St. Thomas	White Hall	Golden Valley District
92	St. Thomas	Morant Bay	59 Queen
93	St. Thomas	Morant Bay	Shop 12 Morant Bay Shopping Centre
94	St. Thomas	Morant Bay	9 West Street
95	St. Thomas	Morant Bay	2 East Street
96	Westmoreland	Savanna-la-Mar	82B Great George Street
97	Westmoreland	Savanna-la-Mar	Meylers Avenue
98	Westmoreland	Savanna-la-Mar	119 Great George Street
99	Westmoreland	Savanna-la-Mar	Shop 5 Chantilly Road
100	Westmoreland	Savanna-la-Mar	Shop 2 115 Great George
101	Westmoreland	Dunbars River	Smithfield Road
102	Westmoreland	Savanna-la-Mar	118 Great Georges Street
103	Westmoreland	Savanna-la-Mar	Shop 1 Winners Plaza
104	Westmoreland	Savanna-la-Mar	54 Beckford St
105	Westmoreland	Savanna-la-Mar	Shop 4 124 Great George Street
106	St. James	Montego Bay	Shop 24-26 City Centre Building
107	St. James	Montego Bay	15 Queens Street
108	St. James	Montego Bay	20 Sunset Boulevard
109	St. James	Montego Bay	17 Barnett Street
110	St. James	Montego Bay	8 Humber Avenue
111	St. James	Greenwood	Wiltshire
112	St. James	Montego Bay	Lot 1 Fairfield
113	St. James	Montego Bay	10 Church Street
114	St. James	Montego Bay	Shop G 108B Baywest Centre
115	St. James	Montego Bay	Shop 18-19 Montego Bay Trade Centre Catherine Hall
116	St. James	Montego Bay	Shop 7 & 8, St Clavers Avenue
117	St. James	Montego Bay	100 Barnett Street
118	Trewlany	Falmouth	13 Market Street
119	Trewlany	Falmouth	Water Square
120	Trewlany	Rio Bueno	Rio Bueno Sea Side
121	Trewlany	Falmouth	Foreshore Road
122	Trewlany	Falmouth	316 Foreshore Road
123	Trewlany	Falmouth	Florence Hall Village
124	Trewlany	St Flemings	3 Queens
125	Trewlany	Falmouth	26 Duke Street
126	Trewlany	Falmouth	23 Market Street
127	St. Mary	Highgate	Shop 3 Central Plaza
128	St. Mary	Highgate	Main Street
129	St. Mary	Port Maria	Tres Hills
130	St. Mary	Port Maria	12 Stennett Street
131	St. Mary	Salt Gut	Huddersfield
132	St. Mary	Annotto Bay	Main Street
133	St. Mary	Tower Isle	Main Street Rio Nuevo
134	St. Mary	Tower Isle	Gayle
135	St. Mary	Tower Isle	14e Pompano Commercial Complex
136	St. Mary	Tower Isle	Main Road
137	Hanover	HopeWell	Main Road
138	Hanover	HopeWell	Main Street
139	Hanover	Lucea	25 Hanover Street
140	Hanover	HopeWell	Shop 16 Hopewell Mall
141	Hanover	Lucea	Shop 1 Midtown Mall
142	Hanover	Lucea	Shop 23 Midtown Mall
143	Hanover	Lucea	Main Street
144	St. Catherine	Spanish Town	9 Monk Street
145	St. Catherine	Portmore	George Lee Boulevard
156	Clarendon	May Pen	28 Main Street
157	St. Elizabeth	Treasure Beach	Calabash Bay P.A
158	St. James	Montego Bay	12 Bogue Road
159	IslandWide	IslandWide	\N
14	St. Andrew	Kingston	6-12 Newport Boulevard, Newport Commercial Center
15	St. Andrew	Kingston	Donhead Avenure, Kingston 6
16	St. Andrew	Kingston	64 Darley Crescent
17	St. Andrew	Kingston	-
18	St. Andrew	Kingston	Shp #12, 42 Old Hope Rd,Kgn 5
19	St. Andrew	Half Way Tree	Shop 28 Limelight Plaza Half Way Tree
20	St. Andrew	Half Way Tree	Shop #19, Upstairs, Bargain Mall, Clock Tower Plaza
21	St. Andrew	Kingston	134 1/4 Upper King Street
22	St. Andrew	Kingston	9 Ashoka Road
23	St. Andrew	Kingston	10 South Road
24	St. Andrew	Kingston	8 Melmac Avenue
25	St. Andrew	Richmond Park	33 Queens Avenue
26	St. Andrew	Kingston	3a Torrie Avenue
27	St. Andrew	Red Hills	90b Redhills Road
28	St. Andrew	Kingston	22B Old Hope Road
29	St. Andrew	Duhaney Park	35 Dawn Avenue
30	St. Andrew	Kingston	12 Lady Musgrave Road
31	St. Andrew	Kingston	5 Sandringham Avenue
146	St. Andrew	Kingston	28 Collins Green Avenue
147	St. Andrew	Kingston	27 Red Hills Rd
148	St. Andrew	Kingston	28 Beechwood Avenue
149	St. Andrew	Kingston	16 Lady Musgrave Road
150	St. Andrew	Kingston	2E Camp Road
151	St. Andrew	Kingston	12c Collie Smith Drive
152	St. Andrew	Kingston	6 Collie Smith Drive
153	St. Andrew	Kingston	191 Constant Spring Road
154	St. Andrew	Kingston	2B Camp Road
155	St. Andrew	Kingston	122-126 Tower Street
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.messages (message_id, sender_user_id, message_text, sent_at, is_read, conversation_id, encrypted_message_text) FROM stdin;
\.


--
-- Data for Name: monthly_business_reports; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.monthly_business_reports (report_id, organisation_id, report_month, report_year, total_views, total_saves, total_messages, total_reviews, average_rating, bayesian_rating, trend_score, trend_status, generated_at, engagement_score, growth_rate, total_volunteer_signups) FROM stdin;
1	159	5	2026	2	1	1	1	0	4	33.8	Base Month	2026-07-24 14:56:42.076562	14	0	0
2	159	6	2026	3	2	1	1	0	4	40.099999999999994	Improving	2026-07-24 15:07:47.523587	23	18.63905325443786	1
\.


--
-- Data for Name: organisation_categories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.organisation_categories (organisation_category_id, organisation_id, category_id) FROM stdin;
1	159	101
2	160	102
3	161	103
4	161	104
5	162	105
6	163	104
7	163	106
8	164	106
9	164	107
10	165	104
11	165	106
12	166	105
13	166	108
14	166	109
15	167	108
16	167	106
17	168	108
18	168	110
19	169	110
22	171	111
23	171	106
24	172	102
25	172	112
26	173	102
27	174	113
28	175	102
29	175	114
30	176	112
31	177	112
32	178	114
33	179	106
34	179	115
35	180	114
36	180	102
37	181	114
38	182	106
39	183	116
40	184	116
41	184	104
42	185	116
43	186	116
44	187	117
45	187	118
46	188	117
47	188	106
48	189	115
49	190	101
50	191	114
51	191	102
52	191	119
53	192	101
54	193	120
55	193	119
56	194	108
57	194	110
58	195	101
59	195	115
60	196	101
61	197	108
62	197	105
63	197	109
64	198	102
65	198	119
66	199	105
67	199	106
68	200	104
69	200	117
70	200	106
71	201	102
72	201	105
73	202	115
74	203	102
75	203	105
76	204	109
77	204	105
78	205	101
79	206	108
80	206	106
81	206	110
82	207	104
83	207	108
84	207	106
85	208	106
86	208	103
87	208	112
88	208	102
89	209	108
90	209	110
91	209	106
92	210	121
93	210	106
94	211	108
95	211	110
96	212	110
97	212	108
98	213	106
99	213	104
100	214	105
101	214	106
102	215	106
103	215	110
104	216	108
105	216	105
106	216	121
107	217	112
108	217	105
109	217	108
110	218	110
111	218	106
112	219	104
113	219	106
114	219	108
115	220	112
116	220	102
117	221	101
118	222	105
119	222	109
120	223	101
121	223	115
122	224	104
123	224	106
124	225	117
125	225	103
126	225	104
127	226	110
128	226	106
129	227	102
130	227	112
131	227	106
132	228	120
133	229	102
134	229	103
135	230	104
136	230	106
137	230	109
138	231	106
139	231	115
140	232	106
141	232	115
142	232	105
146	234	102
147	234	119
148	234	115
149	235	104
150	236	104
151	237	104
152	237	108
153	238	106
154	238	117
155	239	101
156	240	105
157	240	106
158	241	115
159	241	106
160	242	106
161	242	117
162	242	104
163	243	109
164	243	105
165	244	105
166	244	108
167	245	108
168	245	104
169	246	101
170	247	115
171	247	106
172	248	120
173	249	112
174	249	102
175	249	108
176	250	101
177	250	115
178	251	105
179	251	115
180	252	105
181	252	112
182	252	106
183	253	105
184	253	112
185	253	106
186	254	106
187	254	105
188	254	109
189	255	106
190	255	110
191	255	108
192	256	107
193	257	120
194	257	104
195	258	101
196	258	120
197	259	107
198	259	102
199	259	106
200	260	101
201	261	101
202	261	115
203	262	102
204	262	112
205	262	105
206	262	104
207	263	112
208	263	108
209	263	106
210	264	104
211	264	108
212	265	105
213	265	106
214	266	101
215	266	115
216	267	108
217	267	105
218	267	109
219	268	101
220	269	101
221	270	115
222	271	106
223	271	104
224	170	106
225	170	104
226	272	110
227	272	108
228	272	104
229	273	104
230	273	106
231	273	105
232	274	108
233	274	110
234	275	104
235	275	116
236	275	107
237	276	101
238	277	105
239	277	109
240	278	101
241	279	108
242	279	104
243	280	110
244	280	106
245	280	108
246	281	110
247	281	108
248	282	101
249	233	108
250	233	112
251	283	106
252	283	105
253	284	105
254	284	106
255	285	101
256	286	117
257	286	116
258	287	109
259	287	105
260	288	107
261	289	107
262	290	107
263	291	106
264	291	108
265	291	105
266	292	101
267	293	110
268	294	101
269	294	115
270	295	101
271	296	106
272	296	117
273	297	107
274	298	106
275	298	117
276	299	122
277	299	117
278	300	123
279	300	124
280	300	122
281	301	125
282	302	126
283	302	127
284	302	128
285	302	122
286	303	129
287	304	129
288	305	130
289	306	130
290	307	130
291	307	122
292	308	122
293	308	127
294	308	117
295	309	117
296	309	129
297	310	117
298	310	127
299	310	122
300	311	122
301	311	128
302	312	129
303	313	122
304	313	117
305	313	123
306	314	128
307	314	129
308	315	126
309	315	128
\.


--
-- Data for Name: organisation_factors; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.organisation_factors (organisation_id, factors, trained_at) FROM stdin;
229	[0.0]	2026-07-24 01:16:57.18198
309	[1.0]	2026-07-24 01:16:57.18198
\.


--
-- Data for Name: organisation_images; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.organisation_images (image_id, organisation_id, image_url, image_type, uploaded_at) FROM stdin;
\.


--
-- Data for Name: organisations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.organisations (organisation_id, owner_user_id, category_id, location_id, organisation_name, organisation_type, description, website_url, created_at, phone, email) FROM stdin;
171	377	111	14	Inventory Solutions Limited	business	Giving you all the shipping services you need.	\N	2026-07-20 04:04:35.510866	8769486635	admin@insolutionsjm.com
162	383	105	5	Anpanda Ltd	business	Sells home supplies like countertops	\N	2026-07-20 04:04:35.455555	8979073561	anpanda12@gmail.com
238	378	106	81	Affordable Books & Things	business	Find books for school and more.	\N	2026-07-20 04:04:36.069455	8769961394	affordablebooksbbay@yahoo.com
249	381	112	92	Hypnotized Fashion	business	The newest trends and outfits done by our Tailors	\N	2026-07-20 04:04:36.186013	8763553917	andrereid1111@gmail.com
296	415	106	141	Clare Sonia E	business	Book dealers and book shop.	\N	2026-07-20 04:04:36.64673	8769569710	\N
206	376	108	49	Absolute Distributors	business	Absolute Distributors has been your appliance and air conditioning parts store since 2005. We are trusted distributors of refrigeration and air conditioning parts, AC units, evaporator cores, cabin filters and compressors for cars, SUVs, refrigerated trucks, and buses. If you need parts and accessories for air conditioners, then turn to Absolute Accessories.	\N	2026-07-20 04:04:35.763985	8768191937	absolutedistributors@gmail.com
264	379	104	107	Airtech Refrigeration Ltd	business	Airtech Refrigeration Ltd provides services which includes Residential, Commercial & Central Units / Split Units.	\N	2026-07-20 04:04:36.392511	8769524307	airtechrefrigeration@yahoo.com
225	380	117	68	Andjos Data Processing	business	This small bus started as an internet cafe with four computers all connected to one printer. It later grew in approximately one year, to 10 computers connected to two small printers. Still, like all good entrepreneurs, Andrea Johnson Hill continued to seek new ways of making her bus better. The bus later offered services such as designing funeral, wedding, and church programmes, dinner tickets, bookmarkers, and flyers.	\N	2026-07-20 04:04:35.940313	8769669304	andjosdata2004@gmail.com
312	382	129	156	Angels of Love	charity	Health and Voluntary Services for critically ill underprivileged children of Jamaica	https://www.angelsofloveja.org/	2026-07-20 04:04:36.803659	8768088888	angelsofloveja@gmail.com
229	384	102	72	Art 'N' Tings	business	Book-Dealer's Retail	\N	2026-07-20 04:04:35.980111	8769669613	\N
224	385	104	67	Astra Technology Ltd	business	The Legend: The late Perry Henzell co-wrote and directed Jamaica’s first major motion picture that burst reggae into new international consciousness. According to Rolling Stone, The Harder They Come has the best movie soundtrack of all time. The legacy endures, all over, just right.	\N	2026-07-20 04:04:35.929461	8769131200	\N
230	386	104	73	Atneil J. Braham & Associates Co. Ltd	business	Atneil Braham & Associates provides digital mapping services and solutions using various software and techniques such as contour mapping, parcel mapping, cadastral mapping, and utility mapping.	\N	2026-07-20 04:04:35.990479	8769662823	atneilbrahamcompany@gmail.com
252	387	105	95	Authur Barrett & Sons Ltd	business	Fabrics, Electronics, Appliances &\nFurniture	\N	2026-07-20 04:04:36.224229	8767341159	\N
301	388	125	146	Back on the Rack	charity	We are a charity thrift store where all proceeds supplment Missionaries of the Poor's meal program.	https://www.instagram.com/botrjamaica/	2026-07-20 04:04:36.713334	8763121510	\N
226	389	110	69	Bari Enterprises & Auto Parts	business	Bari Enterprises & Auto Parts Specializes in parts for Toyota Nissan and Honda batteries Tyres lubricants auto accessories.	\N	2026-07-20 04:04:35.952415	8769652994	\N
191	390	114	34	Bay Spa	business	A full service spa offering massage, facial, waxing, hair, beauty, nails - manicures & pedicures.	\N	2026-07-20 04:04:35.64247	8767257043	\N
214	391	105	57	Better Bathrooms & Beyond	business	Better Bathrooms & Beyond is an Import & Distribution Company, which is owned & operated by Marsha Parchment. BB&B opened its doors in June of 2014 & since then have been bringing quality products from around the world to the residents of Central Jamaica.	bb-b.myshopify.com	2026-07-20 04:04:35.843138	8765106961	bbandbja@yahoo.com
204	392	109	47	BC Blocks & Building Supplies	business	BC Blocks and Building Supplies Hardware Retail, Cement and Blocks, Steel, Lumber, Plumbing equipments, Wires, Doors, Bathroom accessories and Electrical equipments.	\N	2026-07-20 04:04:35.748271	8769862018	bcblocks@yahoo.com
217	393	112	60	The New Best Decorators Ltd	business	The New Best Decorators Ltd is the best with over 35 years of experience. We are a family-owned bus. We measure, we make¸ and we install. We custom make drapes, curtains, bedspreads, blinds, and re-upholster of sofas and chairs.	\N	2026-07-20 04:04:35.875049	8769624952	bestdec@hotmail.com
267	394	108	110	E & S Best For Less Aluminum and Canvas Awning	business	At Best for Less Awnings, we specialise in building and installing awnings. We offer aluminium and canvas awnings, canopies, carports and aluminium sliding windows. We also wash and repair your awnings.	\N	2026-07-20 04:04:36.436535	8767848800	bestforlessawnings@yahoo.com
283	395	106	128	Bedward's Enterprise Trading Co Ltd	business	Hardware-Retail	\N	2026-07-20 04:04:36.551706	8769922501	betcoltd@gmail.com
222	396	105	65	Better Deal Windows	business	Provides the best windows and home items.	\N	2026-07-20 04:04:35.912044	8769963318	\N
277	397	105	121	Better Price Hardware	business	Better Price Hardware stocks a wide selection of hardware items in one convenient location at the best prices. We stock tools, chemicals, paints, ply doors, windows, cement and much more.	\N	2026-07-20 04:04:36.509082	8766175559	\N
227	398	102	70	Billionhair Extensions	business	Wig and Hair Supplier	\N	2026-07-20 04:04:35.962767	8762394332	billionhairextensionsja@gmail.com
184	399	116	27	Blue Peak Digital Limited	business	We are a digital company that specializes in website , software,digital marketing and SEO	https://bluepeakdigital.com/	2026-07-20 04:04:35.594211	8768557751	\N
270	400	115	113	B & N Meats	business	B&N Meats has what you need and more. We stock a wide variety of meats that include poultry, mutton, beef, and fish. Over the years, we have established ourselves as the trusted source for quality meats for persons in Montego Bay, Westmoreland, Hanover, Falmouth, and neighboring communities.	\N	2026-07-20 04:04:36.454447	8769796427	\N
232	401	106	75	Bob's Supercentre	business	At Bob's Supercentre, we supply all your needs. We have clothes, appliances, electronics, phones, liquor, and food. Visit us today for all your household needs.	www.bobsupercentre.com	2026-07-20 04:04:36.009547	8764527943	bobssupercentre@gmail.com
305	402	130	150	Boys Brigade	charity	The Boys' Brigade care for and challenge young people through a program of informal education underpinned by the Christian faith.	\N	2026-07-20 04:04:36.7461	8769290089	boysbrigade@hotmail.com
313	403	122	157	BREDS	charity	BREDS seeks to foster community empowerment through programs designed to enhance the education, vocational training, recreation and livelihoods of Treasure Beach community members and to ensure the sustainability of the environment that nurtures the community.	http://www.breds.org/	2026-07-20 04:04:36.812097	8769650748	\N
180	404	114	23	Bree Botanicals	business	Bree Botanicals is more than just a skincare brand—we are a movement dedicated to promoting self-care, confidence, and natural beauty through our handcrafted organic soaps and body oils. As a woman-owned bus in Jamaica, we are committed to sustainability and creating high-quality products that cater to individuals who prioritize clean beauty.	https://www.instagram.com/bree_botanicals/	2026-07-20 04:04:35.568975	8763729392	\N
287	405	109	132	Broadway House	business	As a family-operated bus, we have served St. Mary and the North Coast for over 50 years. Our wide range of products includes lumber, plumbing, hardware, painting, and electrical supplies. We also carry kitchen and bathroom fixtures, housewares, and appliances.	\N	2026-07-20 04:04:36.58323	8769662202	\N
263	406	112	106	Bryan's Jewellery & Leather Affair	business	Bryan's Jewellery & Leather Affair repairs watches, clocks, and jewellery. Bryan's Jewellery & Leather Affair sells fashion jewellery, handbags, stainless steel and silver jewellery, clocks, gift items, perfumes and colognes.	\N	2026-07-20 04:04:36.377176	8769523053	\N
165	407	104	8	Cablepro Data Servs Ltd	business	CablePro Data Services has been serving the industry of technology from 2002. We are a trusted provider of comprehensive technology solutions, specializing in biometrics, UPS systems, surveillance cameras, advanced cooling systems, and a full range of computer networking services. With a commitment to quality and cutting-edge innovation, we support businesses in securing, optimizing, and maintaining their critical infrastructure.\n\nOur team of experienced technicians and network specialists brings in-depth knowledge and hands-on expertise to every project, ensuring that each client receives customized solutions tailored to their unique needs. Implementing robust security systems, designing energy-efficient cooling for data centers, or providing reliable power backup solutions, Cable Pro Data Services is dedicated to enhancing operational efficiency and security. We pride ourselves on our responsiveness, technical expertise, and dedication to building lasting partnerships with our clients. At Cable Pro, we make it our mission to keep you connected, secure, and ready for the future!	www.cableprodataservices.com/	2026-07-20 04:04:35.473851	8769393852	\N
192	408	101	35	Calabash Ital Restaurant	business	Vegan Restaurant	\N	2026-07-20 04:04:35.649474	8765705565	\N
187	409	117	30	Caribbean Credit Repair Association (CCRA)	business	The Caribbean Credit Repair Association (CCRA) is dedicated to empowering individuals to take control of their financial futures. We specialize in offering capacity-building programs through comprehensive online training, focusing on credit restoration and management. Our mission is to educate and inspire people to enhance their financial knowledge and improve their creditworthiness.	https://financiallyfocusedtv.gurucan.com/	2026-07-20 04:04:35.614686	8768247712	\N
200	410	104	43	Computer bus Supplies (CBS)	business	At Computer bus Supplies, we provide the bus community, education sector, and individuals with computer supplies and accessories, and stationery. We stock the best brands such as HP, Dell, Canon, Brother, Epson, and Samsung.	\N	2026-07-20 04:04:35.712969	8769745851	cbsochorios@hotmail.com
160	411	102	3	Chantal's Beauty Artistry	business	Make-up and Lash services	Chantal's Beauty Artistry	2026-07-20 04:04:35.442727	8763957788	chantalbentartistry@gmail.com
285	412	101	130	Chicken Hut	business	Best restaurant and dining experience you can find.	\N	2026-07-20 04:04:36.564964	8769942371	\N
250	413	101	93	Chicken & More	business	Restaurant and providing all your food needs.	\N	2026-07-20 04:04:36.198888	8767036220	\N
273	414	104	117	Chin's Radio Sales & Service Ltd	business	Established in 1969, Chin's Radio Sales & Service Ltd. is western Jamaica's number one source for excellent exquisite heirloom quality furniture, bedding products and first-class appliances.	\N	2026-07-20 04:04:36.484377	8769522654	chinsradiosales@cwjamaica.com
255	416	106	98	Clarke's Variety Store	business	Motorcycles, Motor Scooters & ATV's-Service, Supplies & Repair	\N	2026-07-20 04:04:36.266111	8769183027	\N
251	417	105	94	Classic Super Shop & Wholesale Outlet	business	Grocers-Wholesale based in the heart of Morant Bay.	\N	2026-07-20 04:04:36.210891	8769829264	classicsupershop741@gmail.com
284	418	105	129	Colhas Appliance Services	business	If you are looking for professional service, precise and prompt response, you won't lose with ColHas. The technicians has not only provided excellent service but is well knowledgeable about the kitchen equipment.	\N	2026-07-20 04:04:36.558498	8765976508	\N
257	419	120	100	Computaz & Beyond Ltd	business	Computaz & Beyond Ltd. is proficient in computer sales and repairs. Additionally, services offered are: computer accessories sale, internet cafe and networking.	\N	2026-07-20 04:04:36.289017	8769554599	\N
241	420	115	84	Coronation Bakery	business	Coronation Bakery sells hard-dough breads, cornbreads, rolls, Easter buns and pastries.	\N	2026-07-20 04:04:36.096281	8769932710	coronationbakery@hotmail.com
163	421	104	6	Creatif Dot Solutions	business	At the heart of what we do is Economic and social development through team work and excellent service delivery. We pride ourselves in the following: Quick turnaround time Same day service Pickup and delivery and other customized services to meet the needs of our customers	https://www.instagram.com/creatifdots/	2026-07-20 04:04:35.46166	8769032265	creatifdotsolutions@yahoo.com
239	422	101	82	C & S Smoothie Bar & Kitchen	business	One stop shop for a good smoothie	\N	2026-07-20 04:04:36.077958	8762991394	\N
216	423	108	59	Central Agricultural Supplies Co Ltd (Casco Ltd)	business	Central Agricultural Supplies Company Ltd (CASCO), was established in 1976. We distribute feeds, fertilisers, agricultural chemicals and equipment to central and western Jamaica.	www.donaldwitterlimited.com	2026-07-20 04:04:35.863559	8769623084	customerservice@cascoltd.com
209	424	108	52	Dangel Auto Spares & Accessories Ltd	business	At Dangel Auto Spares & Accessories Ltd., we stock a wide range of accessories for all motor vehicle brands. Moreover, our customers trust us to provide new and used parts that are durable and fully functional to suit their auto needs.	www.dangelautojamaica.com/	2026-07-20 04:04:35.795793	8769867140	dangelautospares@gmail.com
269	425	101	112	Day-O Plantation Restaurant & Bar	business	Day-O Plantation Restaurant & Bar owned and operated by Jennifer and Paul Hurlock, located in the lush tropical hills, just 3 miles west of Montego Bay City has been in operation over ten years. We have become a favourite destination for weddings, wedding reception venue rental, wedding arrangement and consultancy services, catering and fine dining in Montego Bay.	\N	2026-07-20 04:04:36.448552	8769521825	dayorest@yahoo.com
240	426	105	83	Deluxe Furnishing Store	business	Deluxe Furnishing Store provides first class furniture & appliances, Mattress, Divan Beds, Wardrobe, Living Room, Dining and Patio Set.	\N	2026-07-20 04:04:36.086785	8769224915	\N
282	427	101	126	Donna's Caribbean Restaurant	business	Affordable dining and catering services	\N	2026-07-20 04:04:36.538087	8766175175	donnasatfalmouth@gmail.com
247	428	115	90	Downtown Payless	business	Dry Goods	\N	2026-07-20 04:04:36.162386	8765785419	downtownpaylesswholesale@yahoo.com
290	429	107	135	Dream Wedding Ja	business	Dream Weddings Jamaica has been helping brides create special wedding memories by providing assistance through every aspect of the planning process. Whether a bride (or member of the party) is in need of a nudge in the right direction or full scale wedding planning, Nikki and her staff are there to help. In addition to expert planning advice, DWJ also offers brides help in designing unique wedding invitations, wedding programs, map cards and weekend event itineraries and many more services.	\N	2026-07-20 04:04:36.603604	8769754793	\N
169	430	110	12	Efficient Auto Company Ltd	business	Efficient Auto Company Limited has been supplying wholesale auto parts for Honda, Toyota, Nissan and Suzuki to other auto companies for the past 10 years.	Home - Efficient Auto Company	2026-07-20 04:04:35.498929	8766321144	efficientautocoltd@cwjamaica.com
197	431	108	40	Electroloc Hardware & Glass Exquisite Home Decor	business	From cement and steel to nails and screws, we are your one-stop-shop for all construction material. To top it all off and add that finishing touch to your space, Electroloc Hardware and Glass Exquisite Home Decor has you covered. We sell everything for your bathroom, kitchen and every space in between. Granite countertops, tiles, lighting, lamps, cushions, and much more are in-store.	www.electrolochardwareandhomedecorja.com	2026-07-20 04:04:35.687059	8769722842	electrolochardware@hotmail.com
266	432	101	109	Flagstaff Bakery	business	If you love bread and delicious baked goodies, come to Flagstaff Bakery. Known as the best in the West, we specialise in the making of Hard Dough bread, duck and twist, superior quality breads, buns, and biscuits.	\N	2026-07-20 04:04:36.421078	8769714694	errolyoung17@yahoo.com
161	433	103	4	Evabless Graphics & More	business	Registered Graphic Design bus	https://evablessgraphics.setmore.com/?utm_source=ig&utm_medium=social&utm_content=link_in_bio&utm_id=97760_v0_s00_e0_tv3	2026-07-20 04:04:35.449588	8768123688	evablessgraphicsmore@gmail.com
259	434	107	102	Excitement Bridal Floral & Gifts	business	We are fully committed to helping brides achieve their wedding dreams. At Excitement Bridal, we provide brides with a truly memorable experience, which starts with a member of our courteous and knowledgeable staff as they help guide brides through the selection process.	\N	2026-07-20 04:04:36.31651	8769181372	excitementbridal@hotmail.com
268	435	101	111	Far Out Fish Hut	business	Far Out Fish Hut has fantastic fishes. Far Out Fish Hut specializes in fried and steamed fishes. Side orders include bammy and breadfruit which are two local Jamaican foods. Far Out Fish Hut establishment is very simple but the service is pretty good and the food is great.	\N	2026-07-20 04:04:36.443202	8769547155	faroutfishutltd@gmail.com
203	436	102	46	Flourish Landscaping	business	Landscape Contractors & Designers	\N	2026-07-20 04:04:35.740326	8764510265	\N
303	437	129	148	Heart Foundation Jamaica	charity	HFJ seeks to minimize the incidence of death from heart disease in Jamaica through education and raising funds for assisting the intensive care unit and cardiac surgery.	http://www.heartfoundation.org.jm	2026-07-20 04:04:36.732699	8769266492	fundmgr@heartfoundationja.org
175	438	102	18	Gags Skincare & Beauty Supplies	business	Skincare and Beauty supplies	Gags Skincare & Beauty Supplies (@gags_skincare_and_beauty)	2026-07-20 04:04:35.538249	8764436554	\N
254	439	106	97	Gary's Fencing & Hardware Supplies	business	Fences, Posts & Fittings	\N	2026-07-20 04:04:36.252016	8769559364	\N
207	440	104	50	General Satellite Network Co Ltd	business	We provide premium channels and, our packages match every budget. With our customisable solutions, our customers can mix and match.	\N	2026-07-20 04:04:35.7735	8769026412	gensat.net@gmail.com
166	441	105	9	G & E Roofing & Constr Co Ltd	business	G & E Roofing and Construction Company Ltd. were founded by Godfrey Campbell. Mr. Campbell is certified as a Construction Technician by the London Institute, holds a Diploma in Architecture from the University of Technology, Jamaica and a Certificate in Construction Engineering from City and Guilds. G & E Roofing and Construction Co. Ltd., under the stewardship of Mr. Campbell have been dedicated to providing sound technical and professional service to Jamaicans across the country for 14 years. G & E Roofing & Construction Co Ltd supplies and installs quality roofing materials. We build from foundation to roof and we also do guttering and ceiling. We offer stone coated metal tiles, Decra metal tiles, Corona shakes, T4 sheeting among others. Free estimates are available islandwide on roofing.	www.geroofingjamaica.com/	2026-07-20 04:04:35.481423	8767490045	\N
306	442	130	150	Girls Brigade	charity	GB empowers girls and young men with skills, Christian qualities and values, to succeed in tomorrow's world.	\N	2026-07-20 04:04:36.752406	8769266427	girlsbrigadeja@yahoo.com
195	443	101	38	Golden Loaf Baking Co Ltd	business	Golden Loaf is more than just a bakery—it's a part of Jamaican culture. For many Jamaicans, Golden Loaf bread is a staple in their daily lives, and the bakery holds a special place in their hearts. Overall, Golden Loaf Bakery is a beloved institution in Jamaica, providing delicious baked goods and a sense of community to those who visit.	www.tiktok.com/@goldenloafbakeryltd? _t=8jgjcRV9X0w	2026-07-20 04:04:35.672013	8769742635	glb@cwjamaica.com
194	444	108	37	Glen & Son's Used Auto Parts Limited	business	Auto parts and repairs for Honda vehicles	\N	2026-07-20 04:04:35.664625	8769749200	glenandsons@yahoo.com
244	445	105	87	Global Refrigeration & Auto A/C Supply	business	Dependenable A/C Supply bus that knows what they're doing	\N	2026-07-20 04:04:36.12968	8767036775	\N
258	446	101	101	Guangos Jerk	business	In 2017 the people of Savanna-La-Mar, Westmoreland warmly welcomed Guangos Jerk. Quickly transitioning from a quick-service jerk spot we've become an authentic Jamaican jerk, fine-dining experience. We execute delectable local dishes as well as jerk chicken and pork.	Instagram	2026-07-20 04:04:36.302077	8768835111	guangosjerk@gmail.com
242	447	106	85	Hamilton's Book Store	business	Hamilton's Bookstore has realised that the economic landscape in our island is changing and we want to ensure that we have adjusted to continue to meet and exceed the needs of customers. We do this by offering services that they have asked for like visa applications for the USA, Canada and the Europe (England as well). Our customers are our priority and we aim to please them by offering extended opening hours when necessary. We have also been working closely with our teachers to design and create and print visual and teaching aids like charts and maps. We print school projects, including SBAs for High School students.	\N	2026-07-20 04:04:36.1079	8769933792	\N
261	448	101	104	Hammond's Kitchen	business	At Hammond's Kitchen, we pride ourselves on delivering oven-fresh products that are crafted with care and attention to detail. Our commitment to quality ensures that every slice, bite, and crumb is filled with goodness.	hammondskitchenja.com/	2026-07-20 04:04:36.341232	8769553399	hammondsconsolidated@gmail.com
294	449	101	139	Hanover Bakery & Restaurant	business	Best bakery and restaurant in Hanover.	\N	2026-07-20 04:04:36.632341	8769562290	\N
289	450	107	134	Harmony Hall Ltd	business	Harmony Hall Ltd was acquired in 1980. Harmony Hall Ltd offers a quiet and romantic haven from which to escape the real world. Harmony Hall Ltd enjoys a fabulous year for guests in the cottages in Jamaica. Harmony Hall Ltd is a major facelift, repainting the roof, the exterior walls and the fretwork, replacing much of the interior woodwork and renovating all the galleries.	\N	2026-07-20 04:04:36.597375	8769754222	\N
170	451	106	115	One Stop Computers Ltd	business	One Stop Computers Ltd supplies: Computers, laptops, digital cameras, flash drives, battery backup, fax machines, processors, hard drives, memory motherboards, ATX cases, wireless routers, printers, desks and chairs and multimedia projectors.	\N	2026-07-20 04:04:35.504437	8769711508	has@cwjamaica.com
205	452	101	48	Smith & Stewart Distributors Ltd	business	Years ago, the frozen novelty category consisted of a few select treats, such as single flavour ice pops, ice cream sandwiches comprised of vanilla ice cream surrounded by chocolate wafers, and vanilla ice cream on a stick covered with a chocolate-flavoured coating. Now we have a wide variety of ice creams and frozen desserts	\N	2026-07-20 04:04:35.755438	8764340684	headoffice@crazyjimja.com
201	453	102	44	Shangri-La Flowers	business	Shangri-La Flowers is a professional retailer and distributor of flowers, floral decor and other floral services.	www.shangrilaflowersjamaica.com/	2026-07-20 04:04:35.722502	8769743498	hello@shangrilaflowersjamaica.com
223	454	101	66	High Street Bakery	business	Family owned bakery	\N	2026-07-20 04:04:35.920691	8769652721	\N
173	455	102	16	Peppermint Roots Natural Jamaica	business	Natural life and herbal products.	Peppermint Roots Naturals. 338 Queen st E Brampton | Facebook	2026-07-20 04:04:35.524347	8763017040	Hindssk@hotmail.com
179	456	106	22	Howies Grocery Wholesale, Retail and Haberdashery	business	Best grocery and wholesale store	\N	2026-07-20 04:04:35.562187	8768271334	\N
279	457	108	123	iFixPC	business	Computers-Service & Repairs	\N	2026-07-20 04:04:36.520073	8763796779	\N
210	458	121	53	Island Farm Supplies Ltd	business	Island Farm Supplies had just relocated to their new premises. With over 20 years of experience, Island Farm Supplies is the largest one stop warehouse for all your home, farm and garden supplies in Clarendon Jamaica. We offer consultation on baby chicks, Fertilizers and Agricultural Chemicals. Deliveries are available on conditions apply.	\N	2026-07-20 04:04:35.806264	8769021908	ifslimited@yahoo.com
309	459	117	153	Abilities Foundation	charity	A registered voluntary organization committed to providing quality vocational education to persons with disabilities	\N	2026-07-20 04:04:36.77935	8769695720	info@abilitiesfoundation.org
271	460	106	114	Di Foto Shoppe	business	We provide passport/visa pictures, glamour shots, studio portraits, foto greeting cards, photo calendars, standard prints, large format prints, photo restorations, photo ID, scanning and laminating.	\N	2026-07-20 04:04:36.460986	8769524527	info@difotoshoppe.com
186	461	116	29	Insight Studios	business	Founded in 2009, Insight Studios is a Jamaican design agency offering creative and effective branding solutions through the use of graphic design, web development and motion graphics. We pride ourselves on our creativity, professionalism and attention to detail and will work with you to plan and execute an efficient and affordable marketing campaign.	https://insightstudiosjm.com/	2026-07-20 04:04:35.606551	8764998846	info@insightstudiosjm.com
302	462	126	147	Lasco Chin Foundation	charity	Guided by our sustainable socio-economic intervention (SSI) model that seeks to address the sustainable development goals (SDGs) and vision 2030, we focus on:\nThe SSI Schooling Support Programme which targets and supports at-risk youths to succeed in school.\nThe SSI Entrepreneurship Programme which supports at-risk youths to succeed in bus, including in agriculture.\nThe Corporate Social Responsibility (CSR) programme addresses the needs of vulnerable groups, including at-risk youth, while recognizing and celebrating exceptional contributions in law enforcement, healthcare, education, and environment protection.	https://lascofoundation.org/en/	2026-07-20 04:04:36.724256	8762768950	info@lascochinfoundation.org
181	463	114	24	Polygenics Consulting	business	Polygenics Consulting takes pride in offering DNA testing in Jamaica, and the wider Caribbean. Our partner labs produce the highest accuracy of results, and have the highest accreditation in relational DNA Testing. With our international partners, we can facilitate DNA testing no matter where in the world you are	Polygenics Consulting	2026-07-20 04:04:35.574822	8763130577	info@polygenicsconsulting.com
190	464	101	33	Irie Eatz Restaurant	business	Restaurant with authentic Jamaican Cuisine	https://www.instagram.com/irieeatzja?igsh=aTdhNTJiaTRldjA%3D	2026-07-20 04:04:35.634049	8768615455	\N
202	465	115	45	Island Eatz	business	Food-selling bus in Clarendon	Island Eatz (@islandeatz_ja) | TikTok	2026-07-20 04:04:35.732597	8763483959	Island.eatz@yahoo.com
280	466	110	124	iWheelz Xpress Ltd	business	iWheelz Xpress Ltd advocate the four best reasons to buy a used car are: minimizing depreciation, reducing insurance costs, reducing registration fees and keeping your peace of mind. Why wait? Come to iWheelz Xpress where we will help you choose the best quality car to fit your budget.	\N	2026-07-20 04:04:36.526497	8769964602	iwheelzXpress@gmail.com
159	467	101	2	JavNick Restaurant	business	Food restaurant in Portmore in the Portmore Town Plaza	\N	2026-07-20 04:04:35.435579	8768538555	\N
304	468	129	149	Jamaica Cancer Society	charity	A non-profit organization with the mandate to “fight and defeat cancer in all its forms”	http://www.jamaicacancersociety.org/	2026-07-20 04:04:36.738974	8769274265	jcsinfo3@cwjamaica.com
262	469	102	105	Jewel Box	business	At Jewel Box, we sell a wide variety of finely crafted jewellery at an affordable price. We also stock appliances, electronics, and a suite of fragrances for a wide cross-section of people. We sell a wide range of batteries for car keys and watches and so much more.	\N	2026-07-20 04:04:36.357408	8769181453	jewel124box@gmail.com
208	470	106	51	Jewellery Legend	business	Jewellery retail store that sells chains, charms, rings etc. from different brands such as Bulova, Casio etc.	\N	2026-07-20 04:04:35.784908	8769023706	\N
278	471	101	122	Jus Rite Foods	business	Food just right for your appetite, coming to you Jamaican style.	\N	2026-07-20 04:04:36.514389	8764941118	\N
189	472	115	32	Just Cool Grocery, Green Grocery and Variety Store	business	Provide homemade Jamaican meals and traditional baked desserts to locals and travellers along the North Coast Highway	\N	2026-07-20 04:04:35.628185	8763752709	\N
299	473	122	144	Children First	charity	A non-governmental agency that caters to the needs of children through the provision of education	http://www.childrenfirst.org.jm/html/	2026-07-20 04:04:36.695288	8769840367	kidz@cwjamaica.com
237	474	104	80	Kweb Media Tech	business	Computers-Service & Repairs	\N	2026-07-20 04:04:36.059724	8764776606	\N
253	475	105	96	Little Ones Boutique	business	Family Owned bus for over 12 years!!	www.facebook.com/LittleOnesJA	2026-07-20 04:04:36.238077	8769559533	littleones121@gmail.com
276	476	101	120	Lobster Bowl Restaurant	business	For the best Lobster, Shrimp, Fish, Steak and Chicken in Jamaica come to The Lobster Bowl. 45 years of satisfaction right on the waterfront of the famous Rio Bueno Bay.	\N	2026-07-20 04:04:36.503272	8769540048	\N
300	477	123	145	MACC Organization	charity	Environmental Conservation Organization	https://www.facebook.com/maccorganization/	2026-07-20 04:04:36.70526	8768715379	maccagents@gmail.com
212	478	110	55	Mercal Electrical Parts & Accessories	business	Mercal Electrical Parts & Accessories is the ideal tool depot and service centre. We stock new and used tools and accessories, such as portable cables, transformers, drills and routers.	\N	2026-07-20 04:04:35.824868	8769620221	mercal@cwjamaica.com
243	479	109	86	Millennium Paving Stones Ltd	business	Millennium Paving Stones Limited is Jamaica's largest paving stone manufacturer. We began operations in 2000, manufacturing stepping stones, grasscrete, and curb wall and distributing complementary products like sealers, cleaners, and polymeric sand. Our paving stones are manufactured using aggregates from the St Thomas River. We do not use marl or limestone to manufacture our products. Our colours go through our stones. As a result, our stones are more durable and long-lasting. They are available in various shapes, colours, and blends.	\N	2026-07-20 04:04:36.119015	8767033151	milpave@yahoo.com
231	480	106	74	Morrison's Variety Store	business	We are a haberdashery and supermarket , who caters to the community of Santa Cruz. We are located in the middle of Town of Santa Cruz, with friendly staff and excellent service waiting you.	\N	2026-07-20 04:04:35.998617	8769663598	morrison'svarietystore@yahoo.com
198	481	102	41	Nasirah Limited	business	Nasirah’s Spa Ltd opened its door in March 2013 and has since been the pioneer of luxurious and decadent spa services. We are conveniently located at Shop 18 Eight Rivers Town Center, Dacosta Drive Ocho Rios, St. Ann. Visit the Best Spa in Ocho Rios where you will have hassle free and ample parking. We are a short walk from the cruise ship pier and Knutsford Express and just 45 minutes from Kingston. Nasirah’s has created a new standard in the wellness industry that was conceptualised from a passion for beauty and relaxation. This was motivated by our goal to provide an oasis that offers a soothing ambiance that simply casts your stress and worries away.	nasirahspa.com	2026-07-20 04:04:35.695709	8769748956	nasirahltd@gmail.com
211	482	108	54	Vulcanizing Partners	business	Vulcanizing Partners is committed to quick, dependable service at competitive prices, with pickup and delivery available to ensure customer convenience and satisfaction.	\N	2026-07-20 04:04:35.815582	8763584297	neltonwatson070@gmail.com
183	483	116	26	Neufville Management and Communications Limited	business	NMCL is an integrated marketing communications organization that provides a wide range of communication services for clients. We are also the Executive Producer for Revtalk, an episodic television series, which has a multifaceted vision to include: mentorship to women, youth, children supporting the development and establishment of good moral values leading to better communities and therefore a better country.	Marketing & Communications | Neufville Management & Communications Limited	2026-07-20 04:04:35.587713	8765070565	\N
178	484	114	21	Nurses & More Limited	business	We provide Medical Tools, Diagnostic Sets, Nurses Supplies, Nurses Uniforms, Shoes, Clogs, Scrubs and Accessories for all medical professionals.	Home - Nurses & More Limited	2026-07-20 04:04:35.555144	8769225015	\N
307	485	130	151	Operation Restoration	charity	Operation Restoration provides Christian education and counseling for children and adults, particularly those engaged in or falling into criminal activity.	http://www.operation-restoration.org	2026-07-20 04:04:36.759648	8769674245	orcs94trenchtown@gmail.com
176	486	112	19	The Clothing Finery	business	Women's Apparel	https://www.instagram.com/theclothingfinery/followers/mutualOnly	2026-07-20 04:04:35.544046	8768492046	orders@theclothingfinery.com
235	487	104	78	Ela Systems Ltd	business	Ela Systems Ltd. offers security services, such as CCTV systems, electronic access control systems, intruder alarm systems and others. If you need to feel safe and secure, our equipment will assist in meeting your security needs.	\N	2026-07-20 04:04:36.041943	8767153180	osusu@cwjamaica.com
248	488	120	91	Outdoors Vybz Jamaica	business	We specialize in camping,hiking, and offroad adventures in the hills and on the river of St Thomas Jamaica.	https://www.instagram.com/outdoorsvybz/	2026-07-20 04:04:36.174113	8762693139	outdoorvybzja25@gmail.com
281	489	110	125	Parts To Go	business	We offer a huge in-stock inventory that meets the needs of anyone looking for Toyota, Honda, Nissan, Mitsubishi, Mazda or Suzuki parts.	\N	2026-07-20 04:04:36.532607	8766175829	partstogofalmouth@yahoo.com
260	490	101	103	P & M Supreme	business	P& M Supreme is located on the West End of beautiful Negril. While not sharing the Cliffs, P&M Supreme enjoys a panoramic view of the Caribbean sea. We have created the Jamaican idea of a homely setting where visitors can enjoy our delicious seafood dishes as well as our mouth watering vegetarian dishes done Jamaican style. Our ever popular Fried Chicken is to die for.	\N	2026-07-20 04:04:36.328922	8769579808	paulcartynegril@gmail.com
234	491	102	77	Petal's Variety Ltd	business	Petals Variety Ltd wholesales Supermarket Items, Body, Beauty and Hair Supplies, Sweets, Snacks, Personal Care, Harbedashery and much more.	\N	2026-07-20 04:04:36.032357	8769939071	\N
291	492	106	136	Poolworld & Fishing Supplies	business	Poolworld & Fishing Supplies is a one stop shop that sells the finest salt water tackle and swimming pool supplies in Tower Isle, St Mary. We stock a wide variety of fishing gear for all anglers, hooks, lines, sinkers, floats, rods, reels, lures, nets and gaffs, just to name a few.	\N	2026-07-20 04:04:36.611506	8762820755	poolworldjamaica@gmail.com
167	493	108	10	Portmore LPG Supplies Ltd	business	Portmore LPG Supplies Ltd supplies and installs Jamaican cooking gas for domestic use. Our company was established to provide the people of Jamaica with top-quality petroleum products. We offer high-quality cylinders, gas refill services, and gas fittings to dealers at competitive rates. Portmore LPG Supplies Ltd is a distributor of PETCOM Cooking Gas	www.portmorelpgsupplies.com/	2026-07-20 04:04:35.487339	8768089943	portmorelpgsupplies@gmail.com
272	494	110	116	Power Plus Electrical & Plbg & Hdw	business	Power Plus Electrical Plumbing & Hardware specializes in providing comprehensive solutions for commercial, residential, and industrial clients. Our offerings include sales, plumbing services, as well as installation and maintenance of electrical equipment and plumbing supplies.	\N	2026-07-20 04:04:36.477239	8769795601	powerplushardware@gmail.com
236	495	104	79	R A P Communications Ltd	business	Cellular Access Service Providers	\N	2026-07-20 04:04:36.049989	8767155943	\N
182	496	106	25	Reality Card Centre Company Limited	business	We are a Promotional Novelty , Trophies & Awards , Signs & Banners Printing Company.	https://realitycardcentre.com/	2026-07-20 04:04:35.580628	8766798721	realitycardcentre@gmail.com
221	497	101	64	Rerrie's Pastries & Cafe	business	Rerrie's Pastries & Cafe is a family-owned bus that specialises in wholesome desserts and beverages. Over the years, we've maintained our standing by providing superior customer satisfaction and quality goods, consistently.	\N	2026-07-20 04:04:35.903939	8769623560	rearrie@gmail.com
245	498	108	88	Ricky's Wireless & More	business	For all your devices fixes and more	\N	2026-07-20 04:04:36.140971	8765094040	\N
288	499	107	133	Running Man Products Ltd	business	Prints & Paints Ltd provides Bags, Duffle Bags, Back Packs, School Bags, Waist Pouches and Draw String Bags. Prints & Paints Ltd also provides special discount for Schools, Churches and Special Events.	\N	2026-07-20 04:04:36.591105	8766307283	\N
193	500	120	36	St Ann Development Co Ltd	business	St. Ann Development Company Limited (SADCo) is a subsidiary of the Urban Development Corporation (UDC), with registered office at Ocean Village Shopping Centre, Main Street, Ocho Rios, St. Ann. The mandate of SADCo is to manage the assets owned by UDC in St. Ann, inclusive of Dunn's River Falls and Park, the Green Grotto Caves and Attractions, Ocho Rios Bay Beach, and Turtle River Park.	www.udcja.com/	2026-07-20 04:04:35.65713	8769742612	sadco@udcja.com
168	501	108	11	Crichton Automotive Ltd	business	Crichton Automotive Ltd is one of Jamaica's most reputable pre-owned vehicle dealerships focusing on vehicle and service quality. Our reputation has become a symbol of quality.	www.crichtonauto.com	2026-07-20 04:04:35.493651	8767490916	sales@crichtonauto.com
219	502	104	62	Digital Systems & Supplies Ltd	business	Digital Systems & Supplies provides solutions and services to improve the productivity and bus results of our customers in information and communication technology and Document Centre Products and Services. Large Inventory Repair Service Excellent Customer Service Competitive Prices empowerment of our employees. We behave responsible as a good corporate citizen.	www.digisysjm.com	2026-07-20 04:04:35.889121	8769866063	sales@digisysjm.com
233	503	108	127	Penny's For Fabrics	business	For over 30 years, we have been supplying the best products at the most viable rates so that our community can benefit in their professional endeavours across various fields. Penny's For Fabrics provides dress and uniform fabric, ready-made garments, suiting, sports fabric, drapery and upholstery, and haberdashery.	\N	2026-07-20 04:04:36.020872	8767243958	Sales@heffessales.com
199	504	105	42	Regency Blinds Ltd	business	The depth of our product range, coupled with our years of experience enable us to offer unmatched service in the satisfaction of our customers’ needs, at competitive prices. Because we manufacture and distribute locally made products, Regency Blinds is able to provide greater quality and order control, shorter lead times, firmer timelines, and on-spot personal service — all without the hassle of you finding foreign exchange, or the risk of damaged or botched orders.	https://www.regency-blinds.com/	2026-07-20 04:04:35.703935	8763684540	sales@regency-blinds.com
218	505	110	61	Wheels & Wheels Auto Imports Ltd	business	Wheels & Wheels Auto Imports Ltd was established in 1999 to provide Jamaicans with a wide selection of quality vehicles. We offer vehicles at the most affordable prices. Our years of experience afford us the advantage when it comes to providing our customers with used cars that are worth the risk of buying.	www.wheelsandwheelsauto.com	2026-07-20 04:04:35.88281	8769040168	sales@wheelsandwheelsauto.com
310	506	117	154	Save The Children Jamaica	charity	STCJ is a voluntary organization which provides early childhood education through the operation of basic schools in the corporate area.	\N	2026-07-20 04:04:36.787821	8769293723	\N
293	507	110	138	Seal Deal Auto Spares & Accessories	business	Seal Deal Auto Spares & Accessories offers genuine and non genuine parts for Toyota, Nissan and Mitsubishi. Seal Deal Auto Spares & Accessories has a wide variety of Bike Parts, Car & Bus Tyres, Batteries (Not Limited to Tropical), Auto body Clips, Lubricants, Front end parts and GT Tyres.	\N	2026-07-20 04:04:36.624944	8769565148	\N
172	508	102	15	Shades of Africa	business	The one stop fashion and boutique store.	https://www.instagram.com/shadesofafrica/	2026-07-20 04:04:35.517593	8767977591	shadesja2003@yahoo.com
265	509	105	108	Simply Unique Household & More	business	Everything you need for a special new home	\N	2026-07-20 04:04:36.406718	8769711023	Simplyuniquehml@yahoo.com
292	510	101	137	Sky Beach Bar & Seafood Grill	business	Sky Beach Bar & Seafood Grill, nestled in Hopewell, Hanover, is a stone throw away from the highway, offering both convenience and a serene escape. Here, guests can savour authentic Jamaican cuisine in a tranquil and inviting ambiance.	\N	2026-07-20 04:04:36.61868	8769565006	skybeach24@gmail.com
213	511	106	56	Smartbox TSSR LTD	business	At Smartbox TSSR Ltd, you are covered with innovative, revolutionary, and smart technology. We provide a wide range of the latest technology consumer electronics and are committed to delivering impeccable customer service.	\N	2026-07-20 04:04:35.834044	8769624335	smartboxmandeville@gmail.com
298	512	106	143	Snave School & Office Supplies	business	For your back to school needs.	\N	2026-07-20 04:04:36.661183	8769563636	snavesupplies@yahoo.com
295	513	101	140	Spritz of Hanover	business	When you eat with us you feel the spirit that lives within Hanover.	\N	2026-07-20 04:04:36.639333	8766094329	\N
196	514	101	39	Harding's St. Ann #1 Caterers	business	Our chefs and team are well experienced in planning and preparing traditional Jamaican cuisine, which is deeply influenced by their culinary methods and skills.	\N	2026-07-20 04:04:35.67882	8769176431	st.anncaterers@yahoo.com
188	515	117	31	Stationery World and Book Center Limited	business	We sell Stationery, office furniture, computer supplies, Textbooks and much more	https://swbcja.com/	2026-07-20 04:04:35.621841	8766189722	\N
228	516	120	71	St Elizabeth Safaris Ltd	business	Tourist Attractions & Amusement Places	\N	2026-07-20 04:04:35.971464	8769652374	stelizabethsafariltd@gmail.com
215	517	106	58	S & N Auto Sales & Japanese Used Parts	business	We provide our clients with Genuine Used Parts straight from Japan. We supply Auto Parts for Toyota, Honda, Nissan, Mitsubishi, Subaru, and Suzuki as well as Lubricants.	\N	2026-07-20 04:04:35.852683	8769643164	stevenashauto@gmail.com
185	518	116	28	Supmasol	business	Established in 2017, Supmasol Limited is your premier full-suite digital and marketing agency. With a robust portfolio of services including bus intelligence, data analytics, bus consultation, digital marketing, graphic design, market research, and web development, we tailor our expertise to meet diverse industry needs. Our proven track record includes partnerships with esteemed clients such as Target Euro SRL, Purity Bakery, Digiview Security Limited, and Jamaica Bauxite Mining Limited, both locally and internationally. At Supmasol, we’re dedicated to driving success and innovation in every project.	https://supmasol.com/	2026-07-20 04:04:35.600535	8764648891	\N
174	519	113	17	TAP Printery & Decor	business	Item customization	TAP Printery & Decor (@tapp.decor) • Instagram photos and videos	2026-07-20 04:04:35.531758	8763260310	tapp.decor@gmail.com
297	520	107	142	Taylor's Artmedia Awards	business	We sell trophies and awards.	\N	2026-07-20 04:04:36.653702	8764132315	\N
256	521	107	99	Events Tents & Party Rental	business	Tents 'N' Events provides tables, chairs and tents for parties, trade shows, conventions, conferences and events.	\N	2026-07-20 04:04:36.277118	8768465717	tents4events@yahoo.com
314	522	128	158	The Committee for the Upliftment of the Mentally Ill (CUMI)	charity	To reach out and advocate for the homeless and other mentally ill persons of Montego Bay (St. James) and within the limits of resources available, attempt to improve their level of physical and mental health as well as their basic quality of life.	https://cumimobay.org/about-cumi-montego-bay-jamaica/	2026-07-20 04:04:36.821051	8769528737	\N
246	523	101	89	Wavez Sports Bar & Chill	business	We provide great customer service and a chill dining experience.	\N	2026-07-20 04:04:36.151055	8764335432	theultimatewavezja@gmail.com
220	524	112	63	Thomas Jewellery Store	business	Cosmetics & Perfumes-Retail	\N	2026-07-20 04:04:35.896083	8769643453	\N
177	525	112	20	Tiva's Boutique	business	The boutique for all your stylish needs.	https://linktr.ee/tivas?utm_source=ig&utm_medium=social&utm_content=link_in_bio	2026-07-20 04:04:35.54967	8768799877	tivasboutique@gmail.com
311	526	122	155	United Way of Jamaica	charity	The United Way of Jamaica brings together contributors, providers and users of social services, and social planners, in an effort to assist in meeting the social and material needs of less fortunate and disadvantaged Jamaicans.  Projects are funded to support programmes in the areas such as Health and Education	http://govolunteer.com.jm	2026-07-20 04:04:36.796442	8769229424	uwj35@hotmail.com
275	527	104	119	Ventura Photo & Video Service	business	When Ventura entered into the field of Wedding Videography it brought with it years of photographic experience. It also started as the best equipped studio in the bus.	\N	2026-07-20 04:04:36.497482	8765630920	venturaphotoja@gmail.com
274	528	108	118	Victor's Locks & Bicycles	business	Offers products such as Road Bikes, Mountain Bikes, Gravel Bikes and BMX Bikes	\N	2026-07-20 04:04:36.490642	8768459307	\N
315	529	126	159	Westmoreland Aid and Vital Empowernent (WAVE)	charity	To meet with different people in different locations to collect and donate to those who are still dealing with the aftermath of Hurricane Melissa.	\N	2026-07-20 04:04:36.830514	8763835374	\N
164	530	106	7	Wild Rides and Party Rentals	business	Wild Rides & Party Rentals are Jamaica's premier party company and also one of the largest. Our qualified staff handles up to (4) events per day with speed, efficiency and reliability when you really need that extra special touch of fun and excitement.	https://old.wildridesja.com/index.html	2026-07-20 04:04:35.468122	8767042408	\N
286	531	117	131	WritersDomain	business	For all your writing and marketing needs	\N	2026-07-20 04:04:36.572733	8765020183	writersdomain722@gmail.com
308	532	122	152	Boys Town Vocational Training Centre	charity	Youth development in education and training, sports and recreation, counseling and humanitarian assistance	\N	2026-07-20 04:04:36.768771	8769481598	yvonnebeck2@yahoo.com
\.


--
-- Data for Name: ratings_reviews; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ratings_reviews (review_id, organisation_id, user_id, rating, review_text, created_at, is_hidden) FROM stdin;
1	229	9	4	I like this	2026-07-20 18:41:52.264068	f
\.


--
-- Data for Name: review_flags; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.review_flags (flag_id, review_id, flagged_by_user_id, reason, created_at) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.roles (role_id, role_name) FROM stdin;
1	general_user
2	business_user
3	charity_user
4	admin
\.


--
-- Data for Name: saved_organisations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.saved_organisations (saved_id, user_id, organisation_id, saved_at) FROM stdin;
1	16	309	2026-07-20 16:46:55.885758
2	11	309	2026-07-20 18:29:46.64146
3	9	229	2026-07-20 18:42:02.688569
\.


--
-- Data for Name: user_availability; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_availability (availability_id, user_id, available_date, start_time, end_time) FROM stdin;
\.


--
-- Data for Name: user_factors; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_factors (user_id, factors, trained_at) FROM stdin;
9	[0.0]	2026-07-24 01:16:57.18198
11	[4.0]	2026-07-24 01:16:57.18198
16	[4.0]	2026-07-24 01:16:57.18198
\.


--
-- Data for Name: user_preferences; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_preferences (preference_id, user_id, category_id, preference_weight) FROM stdin;
21	374	103	1
22	374	113	1
23	375	108	1
24	375	128	1
\.


--
-- Data for Name: user_skills; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_skills (user_skill_id, user_id, skill_name) FROM stdin;
1	182	General Volunteering
2	184	General Volunteering
3	186	General Volunteering
4	188	General Volunteering
5	190	General Volunteering
6	192	General Volunteering
7	194	General Volunteering
8	196	General Volunteering
9	198	General Volunteering
10	200	General Volunteering
11	202	General Volunteering
12	366	Cooking
13	374	Graphic Design
14	375	Mentoring
15	375	First Aid
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (user_id, role_id, first_name, last_name, email, password_hash, created_at, location_id, last_login_at, display_name) FROM stdin;
398	2	Business	Owner	billionhairextensionsja@gmail.com	Billionhairextensions227!	2026-07-25 23:32:22.573078	70	\N	Billionhair Extensions
399	2	Business	Owner	bluepeakdigitallimited184@civilinfohub.test	Bluepeakdigitallimited184!	2026-07-25 23:32:22.573078	27	\N	Blue Peak Digital Limited
400	2	Business	Owner	bnmeats270@civilinfohub.test	Bnmeats270!	2026-07-25 23:32:22.573078	113	\N	B & N Meats
401	2	Business	Owner	bobssupercentre@gmail.com	Bobssupercentre232!	2026-07-25 23:32:22.573078	75	\N	Bob's Supercentre
407	2	Business	Owner	cableprodataservsltd165@civilinfohub.test	Cableprodataservsltd165!	2026-07-25 23:32:22.573078	8	\N	Cablepro Data Servs Ltd
408	2	Business	Owner	calabashitalrestaurant192@civilinfohub.test	Calabashitalrestaurant192!	2026-07-25 23:32:22.573078	35	\N	Calabash Ital Restaurant
409	2	Business	Owner	caribbeancreditrepairassociationccra187@civilinfohub.test	Caribbeancreditrepairassociationccra187!	2026-07-25 23:32:22.573078	30	\N	Caribbean Credit Repair Association (CCRA)
410	2	Business	Owner	cbsochorios@hotmail.com	Computerbussuppliescbs200!	2026-07-25 23:32:22.573078	43	\N	Computer bus Supplies (CBS)
411	2	Business	Owner	chantalbentartistry@gmail.com	Chantalsbeautyartistry160!	2026-07-25 23:32:22.573078	3	\N	Chantal's Beauty Artistry
412	2	Business	Owner	chickenhut285@civilinfohub.test	Chickenhut285!	2026-07-25 23:32:22.573078	130	\N	Chicken Hut
413	2	Business	Owner	chickenmore250@civilinfohub.test	Chickenmore250!	2026-07-25 23:32:22.573078	93	\N	Chicken & More
414	2	Business	Owner	chinsradiosales@cwjamaica.com	Chinsradiosalesserviceltd273!	2026-07-25 23:32:22.573078	117	\N	Chin's Radio Sales & Service Ltd
465	2	Business	Owner	island.eatz@yahoo.com	Islandeatz202!	2026-07-25 23:32:22.573078	45	2026-07-26 05:35:54.872063	Island Eatz
415	2	Business	Owner	claresoniae296@civilinfohub.test	Claresoniae296!	2026-07-25 23:32:22.573078	141	\N	Clare Sonia E
402	3	Charity	Owner	boysbrigade@hotmail.com	Boysbrigade305!	2026-07-25 23:32:22.573078	150	\N	Boys Brigade
416	2	Business	Owner	clarkesvarietystore255@civilinfohub.test	Clarkesvarietystore255!	2026-07-25 23:32:22.573078	98	\N	Clarke's Variety Store
417	2	Business	Owner	classicsupershop741@gmail.com	Classicsupershopwholesaleoutlet251!	2026-07-25 23:32:22.573078	94	\N	Classic Super Shop & Wholesale Outlet
418	2	Business	Owner	colhasapplianceservices284@civilinfohub.test	Colhasapplianceservices284!	2026-07-25 23:32:22.573078	129	\N	Colhas Appliance Services
419	2	Business	Owner	computazbeyondltd257@civilinfohub.test	Computazbeyondltd257!	2026-07-25 23:32:22.573078	100	\N	Computaz & Beyond Ltd
420	2	Business	Owner	coronationbakery@hotmail.com	Coronationbakery241!	2026-07-25 23:32:22.573078	84	\N	Coronation Bakery
421	2	Business	Owner	creatifdotsolutions@yahoo.com	Creatifdotsolutions163!	2026-07-25 23:32:22.573078	6	\N	Creatif Dot Solutions
422	2	Business	Owner	cssmoothiebarkitchen239@civilinfohub.test	Cssmoothiebarkitchen239!	2026-07-25 23:32:22.573078	82	\N	C & S Smoothie Bar & Kitchen
423	2	Business	Owner	customerservice@cascoltd.com	Centralagriculturalsuppliescoltdcascoltd216!	2026-07-25 23:32:22.573078	59	\N	Central Agricultural Supplies Co Ltd (Casco Ltd)
424	2	Business	Owner	dangelautospares@gmail.com	Dangelautosparesaccessoriesltd209!	2026-07-25 23:32:22.573078	52	\N	Dangel Auto Spares & Accessories Ltd
425	2	Business	Owner	dayorest@yahoo.com	Dayoplantationrestaurantbar269!	2026-07-25 23:32:22.573078	112	\N	Day-O Plantation Restaurant & Bar
426	2	Business	Owner	deluxefurnishingstore240@civilinfohub.test	Deluxefurnishingstore240!	2026-07-25 23:32:22.573078	83	\N	Deluxe Furnishing Store
427	2	Business	Owner	donnasatfalmouth@gmail.com	Donnascaribbeanrestaurant282!	2026-07-25 23:32:22.573078	126	\N	Donna's Caribbean Restaurant
518	2	Business	Owner	supmasol185@civilinfohub.test	Supmasol185!	2026-07-25 23:32:22.573078	28	\N	Supmasol
403	3	Charity	Owner	breds313@civilinfohub.test	Breds313!	2026-07-25 23:32:22.573078	157	\N	BREDS
437	3	Charity	Owner	fundmgr@heartfoundationja.org	Heartfoundationjamaica303!	2026-07-25 23:32:22.573078	148	\N	Heart Foundation Jamaica
442	3	Charity	Owner	girlsbrigadeja@yahoo.com	Girlsbrigade306!	2026-07-25 23:32:22.573078	150	\N	Girls Brigade
459	3	Charity	Owner	info@abilitiesfoundation.org	Abilitiesfoundation309!	2026-07-25 23:32:22.573078	153	\N	Abilities Foundation
462	3	Charity	Owner	info@lascochinfoundation.org	Lascochinfoundation302!	2026-07-25 23:32:22.573078	147	\N	Lasco Chin Foundation
468	3	Charity	Owner	jcsinfo3@cwjamaica.com	Jamaicacancersociety304!	2026-07-25 23:32:22.573078	149	\N	Jamaica Cancer Society
473	3	Charity	Owner	kidz@cwjamaica.com	Childrenfirst299!	2026-07-25 23:32:22.573078	144	\N	Children First
477	3	Charity	Owner	maccagents@gmail.com	Maccorganization300!	2026-07-25 23:32:22.573078	145	\N	MACC Organization
485	3	Charity	Owner	orcs94trenchtown@gmail.com	Operationrestoration307!	2026-07-25 23:32:22.573078	151	\N	Operation Restoration
506	3	Charity	Owner	savethechildrenjamaica310@civilinfohub.test	Savethechildrenjamaica310!	2026-07-25 23:32:22.573078	154	\N	Save The Children Jamaica
522	3	Charity	Owner	thecommitteefortheupliftmentofthementallyillcumi314@civilinfohub.test	Thecommitteefortheupliftmentofthementallyillcumi314!	2026-07-25 23:32:22.573078	158	\N	The Committee for the Upliftment of the Mentally Ill (CUMI)
529	3	Charity	Owner	westmorelandaidandvitalempowernentwave315@civilinfohub.test	Westmorelandaidandvitalempowernentwave315!	2026-07-25 23:32:22.573078	159	\N	Westmoreland Aid and Vital Empowernent (WAVE)
2	1	gen10	General User	gen10@civilinfohub.test	pass10	2026-07-19 07:59:38.844185	\N	\N	gen10 General User
3	1	gen11	General User	gen11@civilinfohub.test	pass11	2026-07-19 07:59:38.846716	\N	\N	gen11 General User
4	1	gen12	General User	gen12@civilinfohub.test	pass12	2026-07-19 07:59:38.848449	\N	\N	gen12 General User
5	1	gen13	General User	gen13@civilinfohub.test	pass13	2026-07-19 07:59:38.850038	\N	\N	gen13 General User
6	1	gen14	General User	gen14@civilinfohub.test	pass14	2026-07-19 07:59:38.851601	\N	\N	gen14 General User
7	1	gen15	General User	gen15@civilinfohub.test	pass15	2026-07-19 07:59:38.853167	\N	\N	gen15 General User
8	1	gen16	General User	gen16@civilinfohub.test	pass16	2026-07-19 07:59:38.85477	\N	\N	gen16 General User
9	1	gen17	General User	gen17@civilinfohub.test	pass17	2026-07-19 07:59:38.856443	\N	\N	gen17 General User
10	1	gen18	General User	gen18@civilinfohub.test	pass18	2026-07-19 07:59:38.857989	\N	\N	gen18 General User
11	1	gen19	General User	gen19@civilinfohub.test	pass19	2026-07-19 07:59:38.859431	\N	\N	gen19 General User
428	2	Business	Owner	downtownpaylesswholesale@yahoo.com	Downtownpayless247!	2026-07-25 23:32:22.573078	90	\N	Downtown Payless
12	1	gen20	General User	gen20@civilinfohub.test	pass20	2026-07-19 07:59:38.860821	\N	\N	gen20 General User
13	1	gen21	General User	gen21@civilinfohub.test	pass21	2026-07-19 07:59:38.86219	\N	\N	gen21 General User
14	1	gen22	General User	gen22@civilinfohub.test	pass22	2026-07-19 07:59:38.863578	\N	\N	gen22 General User
15	1	gen23	General User	gen23@civilinfohub.test	pass23	2026-07-19 07:59:38.864938	\N	\N	gen23 General User
16	1	gen24	General User	gen24@civilinfohub.test	pass24	2026-07-19 07:59:38.866303	\N	\N	gen24 General User
17	1	gen25	General User	gen25@civilinfohub.test	pass25	2026-07-19 07:59:38.86774	\N	\N	gen25 General User
18	1	gen26	General User	gen26@civilinfohub.test	pass26	2026-07-19 07:59:38.869136	\N	\N	gen26 General User
19	1	gen27	General User	gen27@civilinfohub.test	pass27	2026-07-19 07:59:38.870496	\N	\N	gen27 General User
20	1	gen28	General User	gen28@civilinfohub.test	pass28	2026-07-19 07:59:38.871876	\N	\N	gen28 General User
21	1	gen29	General User	gen29@civilinfohub.test	pass29	2026-07-19 07:59:38.873219	\N	\N	gen29 General User
22	1	gen30	General User	gen30@civilinfohub.test	pass30	2026-07-19 07:59:38.874599	\N	\N	gen30 General User
429	2	Business	Owner	dreamweddingja290@civilinfohub.test	Dreamweddingja290!	2026-07-25 23:32:22.573078	135	\N	Dream Wedding Ja
430	2	Business	Owner	efficientautocoltd@cwjamaica.com	Efficientautocompanyltd169!	2026-07-25 23:32:22.573078	12	\N	Efficient Auto Company Ltd
431	2	Business	Owner	electrolochardware@hotmail.com	Electrolochardwareglassexquisitehomedecor197!	2026-07-25 23:32:22.573078	40	\N	Electroloc Hardware & Glass Exquisite Home Decor
432	2	Business	Owner	errolyoung17@yahoo.com	Flagstaffbakery266!	2026-07-25 23:32:22.573078	109	\N	Flagstaff Bakery
433	2	Business	Owner	evablessgraphicsmore@gmail.com	Evablessgraphicsmore161!	2026-07-25 23:32:22.573078	4	\N	Evabless Graphics & More
434	2	Business	Owner	excitementbridal@hotmail.com	Excitementbridalfloralgifts259!	2026-07-25 23:32:22.573078	102	\N	Excitement Bridal Floral & Gifts
435	2	Business	Owner	faroutfishutltd@gmail.com	Faroutfishhut268!	2026-07-25 23:32:22.573078	111	\N	Far Out Fish Hut
436	2	Business	Owner	flourishlandscaping203@civilinfohub.test	Flourishlandscaping203!	2026-07-25 23:32:22.573078	46	\N	Flourish Landscaping
438	2	Business	Owner	gagsskincarebeautysupplies175@civilinfohub.test	Gagsskincarebeautysupplies175!	2026-07-25 23:32:22.573078	18	\N	Gags Skincare & Beauty Supplies
439	2	Business	Owner	garysfencinghardwaresupplies254@civilinfohub.test	Garysfencinghardwaresupplies254!	2026-07-25 23:32:22.573078	97	\N	Gary's Fencing & Hardware Supplies
440	2	Business	Owner	gensat.net@gmail.com	Generalsatellitenetworkcoltd207!	2026-07-25 23:32:22.573078	50	\N	General Satellite Network Co Ltd
441	2	Business	Owner	geroofingconstrcoltd166@civilinfohub.test	Geroofingconstrcoltd166!	2026-07-25 23:32:22.573078	9	\N	G & E Roofing & Constr Co Ltd
443	2	Business	Owner	glb@cwjamaica.com	Goldenloafbakingcoltd195!	2026-07-25 23:32:22.573078	38	\N	Golden Loaf Baking Co Ltd
444	2	Business	Owner	glenandsons@yahoo.com	Glensonsusedautopartslimited194!	2026-07-25 23:32:22.573078	37	\N	Glen & Son's Used Auto Parts Limited
451	2	Business	Owner	has@cwjamaica.com	Onestopcomputersltd170!	2026-07-25 23:32:22.573078	115	\N	One Stop Computers Ltd
452	2	Business	Owner	headoffice@crazyjimja.com	Smithstewartdistributorsltd205!	2026-07-25 23:32:22.573078	48	\N	Smith & Stewart Distributors Ltd
453	2	Business	Owner	hello@shangrilaflowersjamaica.com	Shangrilaflowers201!	2026-07-25 23:32:22.573078	44	\N	Shangri-La Flowers
454	2	Business	Owner	highstreetbakery223@civilinfohub.test	Highstreetbakery223!	2026-07-25 23:32:22.573078	66	\N	High Street Bakery
455	2	Business	Owner	hindssk@hotmail.com	Peppermintrootsnaturaljamaica173!	2026-07-25 23:32:22.573078	16	\N	Peppermint Roots Natural Jamaica
456	2	Business	Owner	howiesgrocerywholesaleretailandhaberdashery179@civilinfohub.test	Howiesgrocerywholesaleretailandhaberdashery179!	2026-07-25 23:32:22.573078	22	\N	Howies Grocery Wholesale, Retail and Haberdashery
458	2	Business	Owner	ifslimited@yahoo.com	Islandfarmsuppliesltd210!	2026-07-25 23:32:22.573078	53	\N	Island Farm Supplies Ltd
460	2	Business	Owner	info@difotoshoppe.com	Difotoshoppe271!	2026-07-25 23:32:22.573078	114	\N	Di Foto Shoppe
461	2	Business	Owner	info@insightstudiosjm.com	Insightstudios186!	2026-07-25 23:32:22.573078	29	\N	Insight Studios
463	2	Business	Owner	info@polygenicsconsulting.com	Polygenicsconsulting181!	2026-07-25 23:32:22.573078	24	\N	Polygenics Consulting
464	2	Business	Owner	irieeatzrestaurant190@civilinfohub.test	Irieeatzrestaurant190!	2026-07-25 23:32:22.573078	33	\N	Irie Eatz Restaurant
466	2	Business	Owner	iwheelzxpress@gmail.com	Iwheelzxpressltd280!	2026-07-25 23:32:22.573078	124	\N	iWheelz Xpress Ltd
467	2	Business	Owner	javnickrestaurant159@civilinfohub.test	Javnickrestaurant159!	2026-07-25 23:32:22.573078	2	\N	JavNick Restaurant
469	2	Business	Owner	jewel124box@gmail.com	Jewelbox262!	2026-07-25 23:32:22.573078	105	\N	Jewel Box
470	2	Business	Owner	jewellerylegend208@civilinfohub.test	Jewellerylegend208!	2026-07-25 23:32:22.573078	51	\N	Jewellery Legend
471	2	Business	Owner	jusritefoods278@civilinfohub.test	Jusritefoods278!	2026-07-25 23:32:22.573078	122	\N	Jus Rite Foods
472	2	Business	Owner	justcoolgrocerygreengroceryandvarietystore189@civilinfohub.test	Justcoolgrocerygreengroceryandvarietystore189!	2026-07-25 23:32:22.573078	32	\N	Just Cool Grocery, Green Grocery and Variety Store
474	2	Business	Owner	kwebmediatech237@civilinfohub.test	Kwebmediatech237!	2026-07-25 23:32:22.573078	80	\N	Kweb Media Tech
475	2	Business	Owner	littleones121@gmail.com	Littleonesboutique253!	2026-07-25 23:32:22.573078	96	\N	Little Ones Boutique
476	2	Business	Owner	lobsterbowlrestaurant276@civilinfohub.test	Lobsterbowlrestaurant276!	2026-07-25 23:32:22.573078	120	\N	Lobster Bowl Restaurant
478	2	Business	Owner	mercal@cwjamaica.com	Mercalelectricalpartsaccessories212!	2026-07-25 23:32:22.573078	55	\N	Mercal Electrical Parts & Accessories
479	2	Business	Owner	milpave@yahoo.com	Millenniumpavingstonesltd243!	2026-07-25 23:32:22.573078	86	\N	Millennium Paving Stones Ltd
480	2	Business	Owner	morrison'svarietystore@yahoo.com	Morrisonsvarietystore231!	2026-07-25 23:32:22.573078	74	\N	Morrison's Variety Store
481	2	Business	Owner	nasirahltd@gmail.com	Nasirahlimited198!	2026-07-25 23:32:22.573078	41	\N	Nasirah Limited
482	2	Business	Owner	neltonwatson070@gmail.com	Vulcanizingpartners211!	2026-07-25 23:32:22.573078	54	\N	Vulcanizing Partners
483	2	Business	Owner	neufvillemanagementandcommunicationslimited183@civilinfohub.test	Neufvillemanagementandcommunicationslimited183!	2026-07-25 23:32:22.573078	26	\N	Neufville Management and Communications Limited
484	2	Business	Owner	nursesmorelimited178@civilinfohub.test	Nursesmorelimited178!	2026-07-25 23:32:22.573078	21	\N	Nurses & More Limited
486	2	Business	Owner	orders@theclothingfinery.com	Theclothingfinery176!	2026-07-25 23:32:22.573078	19	\N	The Clothing Finery
487	2	Business	Owner	osusu@cwjamaica.com	Elasystemsltd235!	2026-07-25 23:32:22.573078	78	\N	Ela Systems Ltd
488	2	Business	Owner	outdoorvybzja25@gmail.com	Outdoorsvybzjamaica248!	2026-07-25 23:32:22.573078	91	\N	Outdoors Vybz Jamaica
489	2	Business	Owner	partstogofalmouth@yahoo.com	Partstogo281!	2026-07-25 23:32:22.573078	125	\N	Parts To Go
496	2	Business	Owner	realitycardcentre@gmail.com	Realitycardcentrecompanylimited182!	2026-07-25 23:32:22.573078	25	\N	Reality Card Centre Company Limited
497	2	Business	Owner	rearrie@gmail.com	Rerriespastriescafe221!	2026-07-25 23:32:22.573078	64	\N	Rerrie's Pastries & Cafe
498	2	Business	Owner	rickyswirelessmore245@civilinfohub.test	Rickyswirelessmore245!	2026-07-25 23:32:22.573078	88	\N	Ricky's Wireless & More
499	2	Business	Owner	runningmanproductsltd288@civilinfohub.test	Runningmanproductsltd288!	2026-07-25 23:32:22.573078	133	\N	Running Man Products Ltd
500	2	Business	Owner	sadco@udcja.com	Stanndevelopmentcoltd193!	2026-07-25 23:32:22.573078	36	\N	St Ann Development Co Ltd
501	2	Business	Owner	sales@crichtonauto.com	Crichtonautomotiveltd168!	2026-07-25 23:32:22.573078	11	\N	Crichton Automotive Ltd
502	2	Business	Owner	sales@digisysjm.com	Digitalsystemssuppliesltd219!	2026-07-25 23:32:22.573078	62	\N	Digital Systems & Supplies Ltd
503	2	Business	Owner	sales@heffessales.com	Pennysforfabrics233!	2026-07-25 23:32:22.573078	127	\N	Penny's For Fabrics
504	2	Business	Owner	sales@regency-blinds.com	Regencyblindsltd199!	2026-07-25 23:32:22.573078	42	\N	Regency Blinds Ltd
505	2	Business	Owner	sales@wheelsandwheelsauto.com	Wheelswheelsautoimportsltd218!	2026-07-25 23:32:22.573078	61	\N	Wheels & Wheels Auto Imports Ltd
507	2	Business	Owner	sealdealautosparesaccessories293@civilinfohub.test	Sealdealautosparesaccessories293!	2026-07-25 23:32:22.573078	138	\N	Seal Deal Auto Spares & Accessories
508	2	Business	Owner	shadesja2003@yahoo.com	Shadesofafrica172!	2026-07-25 23:32:22.573078	15	\N	Shades of Africa
509	2	Business	Owner	simplyuniquehml@yahoo.com	Simplyuniquehouseholdmore265!	2026-07-25 23:32:22.573078	108	\N	Simply Unique Household & More
510	2	Business	Owner	skybeach24@gmail.com	Skybeachbarseafoodgrill292!	2026-07-25 23:32:22.573078	137	\N	Sky Beach Bar & Seafood Grill
511	2	Business	Owner	smartboxmandeville@gmail.com	Smartboxtssrltd213!	2026-07-25 23:32:22.573078	56	\N	Smartbox TSSR LTD
512	2	Business	Owner	snavesupplies@yahoo.com	Snaveschoolofficesupplies298!	2026-07-25 23:32:22.573078	143	\N	Snave School & Office Supplies
513	2	Business	Owner	spritzofhanover295@civilinfohub.test	Spritzofhanover295!	2026-07-25 23:32:22.573078	140	\N	Spritz of Hanover
514	2	Business	Owner	st.anncaterers@yahoo.com	Hardingsstann1caterers196!	2026-07-25 23:32:22.573078	39	\N	Harding's St. Ann #1 Caterers
515	2	Business	Owner	stationeryworldandbookcenterlimited188@civilinfohub.test	Stationeryworldandbookcenterlimited188!	2026-07-25 23:32:22.573078	31	\N	Stationery World and Book Center Limited
516	2	Business	Owner	stelizabethsafariltd@gmail.com	Stelizabethsafarisltd228!	2026-07-25 23:32:22.573078	71	\N	St Elizabeth Safaris Ltd
517	2	Business	Owner	stevenashauto@gmail.com	Snautosalesjapaneseusedparts215!	2026-07-25 23:32:22.573078	58	\N	S & N Auto Sales & Japanese Used Parts
519	2	Business	Owner	tapp.decor@gmail.com	Tapprinterydecor174!	2026-07-25 23:32:22.573078	17	\N	TAP Printery & Decor
520	2	Business	Owner	taylorsartmediaawards297@civilinfohub.test	Taylorsartmediaawards297!	2026-07-25 23:32:22.573078	142	\N	Taylor's Artmedia Awards
521	2	Business	Owner	tents4events@yahoo.com	Eventstentspartyrental256!	2026-07-25 23:32:22.573078	99	\N	Events Tents & Party Rental
523	2	Business	Owner	theultimatewavezja@gmail.com	Wavezsportsbarchill246!	2026-07-25 23:32:22.573078	89	\N	Wavez Sports Bar & Chill
524	2	Business	Owner	thomasjewellerystore220@civilinfohub.test	Thomasjewellerystore220!	2026-07-25 23:32:22.573078	63	\N	Thomas Jewellery Store
525	2	Business	Owner	tivasboutique@gmail.com	Tivasboutique177!	2026-07-25 23:32:22.573078	20	\N	Tiva's Boutique
527	2	Business	Owner	venturaphotoja@gmail.com	Venturaphotovideoservice275!	2026-07-25 23:32:22.573078	119	\N	Ventura Photo & Video Service
528	2	Business	Owner	victorslocksbicycles274@civilinfohub.test	Victorslocksbicycles274!	2026-07-25 23:32:22.573078	118	\N	Victor's Locks & Bicycles
530	2	Business	Owner	wildridesandpartyrentals164@civilinfohub.test	Wildridesandpartyrentals164!	2026-07-25 23:32:22.573078	7	\N	Wild Rides and Party Rentals
531	2	Business	Owner	writersdomain722@gmail.com	Writersdomain286!	2026-07-25 23:32:22.573078	131	\N	WritersDomain
366	1	Michael	Mann	mman@test.com	mrmann	2026-07-24 02:18:06.253083	\N	\N	Michael Mann
182	1	gen10	General User	gen10.general_user@civilinfohub.test	pass10	2026-07-20 04:04:35.340553	\N	\N	gen10 General User
183	1	gen11	General User	gen11.general_user@civilinfohub.test	pass11	2026-07-20 04:04:35.349615	\N	\N	gen11 General User
184	1	gen12	General User	gen12.general_user@civilinfohub.test	pass12	2026-07-20 04:04:35.351056	\N	\N	gen12 General User
185	1	gen13	General User	gen13.general_user@civilinfohub.test	pass13	2026-07-20 04:04:35.353686	\N	\N	gen13 General User
186	1	gen14	General User	gen14.general_user@civilinfohub.test	pass14	2026-07-20 04:04:35.354985	\N	\N	gen14 General User
187	1	gen15	General User	gen15.general_user@civilinfohub.test	pass15	2026-07-20 04:04:35.3576	\N	\N	gen15 General User
188	1	gen16	General User	gen16.general_user@civilinfohub.test	pass16	2026-07-20 04:04:35.359009	\N	\N	gen16 General User
189	1	gen17	General User	gen17.general_user@civilinfohub.test	pass17	2026-07-20 04:04:35.361689	\N	\N	gen17 General User
190	1	gen18	General User	gen18.general_user@civilinfohub.test	pass18	2026-07-20 04:04:35.363057	\N	\N	gen18 General User
191	1	gen19	General User	gen19.general_user@civilinfohub.test	pass19	2026-07-20 04:04:35.365721	\N	\N	gen19 General User
192	1	gen20	General User	gen20.general_user@civilinfohub.test	pass20	2026-07-20 04:04:35.367032	\N	\N	gen20 General User
193	1	gen21	General User	gen21.general_user@civilinfohub.test	pass21	2026-07-20 04:04:35.369546	\N	\N	gen21 General User
194	1	gen22	General User	gen22.general_user@civilinfohub.test	pass22	2026-07-20 04:04:35.37088	\N	\N	gen22 General User
195	1	gen23	General User	gen23.general_user@civilinfohub.test	pass23	2026-07-20 04:04:35.373478	\N	\N	gen23 General User
196	1	gen24	General User	gen24.general_user@civilinfohub.test	pass24	2026-07-20 04:04:35.374715	\N	\N	gen24 General User
197	1	gen25	General User	gen25.general_user@civilinfohub.test	pass25	2026-07-20 04:04:35.377208	\N	\N	gen25 General User
198	1	gen26	General User	gen26.general_user@civilinfohub.test	pass26	2026-07-20 04:04:35.378538	\N	\N	gen26 General User
199	1	gen27	General User	gen27.general_user@civilinfohub.test	pass27	2026-07-20 04:04:35.381012	\N	\N	gen27 General User
200	1	gen28	General User	gen28.general_user@civilinfohub.test	pass28	2026-07-20 04:04:35.382286	\N	\N	gen28 General User
201	1	gen29	General User	gen29.general_user@civilinfohub.test	pass29	2026-07-20 04:04:35.384858	\N	\N	gen29 General User
202	1	gen30	General User	gen30.general_user@civilinfohub.test	pass30	2026-07-20 04:04:35.386184	\N	\N	gen30 General User
374	1	John	Singh	jsingh@test.com	jsingh	2026-07-24 02:48:46.035082	\N	2026-07-26 04:05:59.919302	John Singh
362	1	Jeff 	John	JJohn@test.com	scrypt:32768:8:1$6pd0wIWk1tRUdb1C$e2973e6479c98a629f7295bdf1c221d414a21a7884f6ea1b95963b42f93ce340a0d546888a198fba7719e4796f51fd6ac54aca7561098824ca0558f35ceced8e	2026-07-20 18:51:11.133029	\N	\N	Jeff  John
375	1	Mike	Samuel	msamuel@test.com	msamsuel	2026-07-24 21:25:46.933191	\N	\N	Mike Samuel
376	2	Business	Owner	absolutedistributors@gmail.com	Absolutedistributors206!	2026-07-25 23:32:22.573078	49	\N	Absolute Distributors
377	2	Business	Owner	admin@insolutionsjm.com	Inventorysolutionslimited171!	2026-07-25 23:32:22.573078	14	\N	Inventory Solutions Limited
378	2	Business	Owner	affordablebooksbbay@yahoo.com	Affordablebooksthings238!	2026-07-25 23:32:22.573078	81	\N	Affordable Books & Things
379	2	Business	Owner	airtechrefrigeration@yahoo.com	Airtechrefrigerationltd264!	2026-07-25 23:32:22.573078	107	\N	Airtech Refrigeration Ltd
380	2	Business	Owner	andjosdata2004@gmail.com	Andjosdataprocessing225!	2026-07-25 23:32:22.573078	68	\N	Andjos Data Processing
381	2	Business	Owner	andrereid1111@gmail.com	Hypnotizedfashion249!	2026-07-25 23:32:22.573078	92	\N	Hypnotized Fashion
383	2	Business	Owner	anpanda12@gmail.com	Anpandaltd162!	2026-07-25 23:32:22.573078	5	\N	Anpanda Ltd
384	2	Business	Owner	artntings229@civilinfohub.test	Artntings229!	2026-07-25 23:32:22.573078	72	\N	Art 'N' Tings
385	2	Business	Owner	astratechnologyltd224@civilinfohub.test	Astratechnologyltd224!	2026-07-25 23:32:22.573078	67	\N	Astra Technology Ltd
386	2	Business	Owner	atneilbrahamcompany@gmail.com	Atneiljbrahamassociatescoltd230!	2026-07-25 23:32:22.573078	73	\N	Atneil J. Braham & Associates Co. Ltd
387	2	Business	Owner	authurbarrettsonsltd252@civilinfohub.test	Authurbarrettsonsltd252!	2026-07-25 23:32:22.573078	95	\N	Authur Barrett & Sons Ltd
389	2	Business	Owner	barienterprisesautoparts226@civilinfohub.test	Barienterprisesautoparts226!	2026-07-25 23:32:22.573078	69	\N	Bari Enterprises & Auto Parts
390	2	Business	Owner	bayspa191@civilinfohub.test	Bayspa191!	2026-07-25 23:32:22.573078	34	\N	Bay Spa
391	2	Business	Owner	bbandbja@yahoo.com	Betterbathroomsbeyond214!	2026-07-25 23:32:22.573078	57	\N	Better Bathrooms & Beyond
392	2	Business	Owner	bcblocks@yahoo.com	Bcblocksbuildingsupplies204!	2026-07-25 23:32:22.573078	47	\N	BC Blocks & Building Supplies
393	2	Business	Owner	bestdec@hotmail.com	Thenewbestdecoratorsltd217!	2026-07-25 23:32:22.573078	60	\N	The New Best Decorators Ltd
394	2	Business	Owner	bestforlessawnings@yahoo.com	Esbestforlessaluminumandcanvasawning267!	2026-07-25 23:32:22.573078	110	\N	E & S Best For Less Aluminum and Canvas Awning
395	2	Business	Owner	betcoltd@gmail.com	Bedwardsenterprisetradingcoltd283!	2026-07-25 23:32:22.573078	128	\N	Bedward's Enterprise Trading Co Ltd
396	2	Business	Owner	betterdealwindows222@civilinfohub.test	Betterdealwindows222!	2026-07-25 23:32:22.573078	65	\N	Better Deal Windows
397	2	Business	Owner	betterpricehardware277@civilinfohub.test	Betterpricehardware277!	2026-07-25 23:32:22.573078	121	\N	Better Price Hardware
382	3	Charity	Owner	angelsofloveja@gmail.com	Angelsoflove312!	2026-07-25 23:32:22.573078	156	\N	Angels of Love
388	3	Charity	Owner	backontherack301@civilinfohub.test	Backontherack301!	2026-07-25 23:32:22.573078	146	\N	Back on the Rack
404	2	Business	Owner	breebotanicals180@civilinfohub.test	Breebotanicals180!	2026-07-25 23:32:22.573078	23	\N	Bree Botanicals
405	2	Business	Owner	broadwayhouse287@civilinfohub.test	Broadwayhouse287!	2026-07-25 23:32:22.573078	132	\N	Broadway House
406	2	Business	Owner	bryansjewelleryleatheraffair263@civilinfohub.test	Bryansjewelleryleatheraffair263!	2026-07-25 23:32:22.573078	106	\N	Bryan's Jewellery & Leather Affair
445	2	Business	Owner	globalrefrigerationautoacsupply244@civilinfohub.test	Globalrefrigerationautoacsupply244!	2026-07-25 23:32:22.573078	87	\N	Global Refrigeration & Auto A/C Supply
446	2	Business	Owner	guangosjerk@gmail.com	Guangosjerk258!	2026-07-25 23:32:22.573078	101	\N	Guangos Jerk
447	2	Business	Owner	hamiltonsbookstore242@civilinfohub.test	Hamiltonsbookstore242!	2026-07-25 23:32:22.573078	85	\N	Hamilton's Book Store
448	2	Business	Owner	hammondsconsolidated@gmail.com	Hammondskitchen261!	2026-07-25 23:32:22.573078	104	\N	Hammond's Kitchen
449	2	Business	Owner	hanoverbakeryrestaurant294@civilinfohub.test	Hanoverbakeryrestaurant294!	2026-07-25 23:32:22.573078	139	\N	Hanover Bakery & Restaurant
450	2	Business	Owner	harmonyhallltd289@civilinfohub.test	Harmonyhallltd289!	2026-07-25 23:32:22.573078	134	\N	Harmony Hall Ltd
457	2	Business	Owner	ifixpc279@civilinfohub.test	Ifixpc279!	2026-07-25 23:32:22.573078	123	\N	iFixPC
490	2	Business	Owner	paulcartynegril@gmail.com	Pmsupreme260!	2026-07-25 23:32:22.573078	103	\N	P & M Supreme
491	2	Business	Owner	petalsvarietyltd234@civilinfohub.test	Petalsvarietyltd234!	2026-07-25 23:32:22.573078	77	\N	Petal's Variety Ltd
492	2	Business	Owner	poolworldjamaica@gmail.com	Poolworldfishingsupplies291!	2026-07-25 23:32:22.573078	136	\N	Poolworld & Fishing Supplies
493	2	Business	Owner	portmorelpgsupplies@gmail.com	Portmorelpgsuppliesltd167!	2026-07-25 23:32:22.573078	10	\N	Portmore LPG Supplies Ltd
494	2	Business	Owner	powerplushardware@gmail.com	Powerpluselectricalplbghdw272!	2026-07-25 23:32:22.573078	116	\N	Power Plus Electrical & Plbg & Hdw
495	2	Business	Owner	rapcommunicationsltd236@civilinfohub.test	Rapcommunicationsltd236!	2026-07-25 23:32:22.573078	79	\N	R A P Communications Ltd
526	3	Charity	Owner	uwj35@hotmail.com	Unitedwayofjamaica311!	2026-07-25 23:32:22.573078	155	\N	United Way of Jamaica
532	3	Charity	Owner	yvonnebeck2@yahoo.com	Boystownvocationaltrainingcentre308!	2026-07-25 23:32:22.573078	152	\N	Boys Town Vocational Training Centre
\.


--
-- Data for Name: volunteer_allocations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.volunteer_allocations (allocation_id, volunteer_need_id, user_id, matching_score, allocation_status, allocated_at) FROM stdin;
\.


--
-- Data for Name: volunteer_needs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.volunteer_needs (volunteer_need_id, organisation_id, title, description, urgency_level, status, created_at, needed_date, start_time, end_time, volunteers_needed) FROM stdin;
\.


--
-- Data for Name: volunteer_required_skills; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.volunteer_required_skills (required_skill_id, volunteer_need_id, skill_name) FROM stdin;
\.


--
-- Data for Name: volunteer_signups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.volunteer_signups (signup_id, volunteer_need_id, user_id, status, signed_up_at) FROM stdin;
\.


--
-- Name: categories_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.categories_category_id_seq', 130, true);


--
-- Name: conversations_conversation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.conversations_conversation_id_seq', 1, false);


--
-- Name: engagement_logs_engagement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.engagement_logs_engagement_id_seq', 15, true);


--
-- Name: locations_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.locations_location_id_seq', 159, true);


--
-- Name: messages_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.messages_message_id_seq', 1, false);


--
-- Name: monthly_business_reports_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.monthly_business_reports_report_id_seq', 15, true);


--
-- Name: organisation_categories_organisation_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.organisation_categories_organisation_category_id_seq', 309, true);


--
-- Name: organisation_images_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.organisation_images_image_id_seq', 1, false);


--
-- Name: organisations_organisation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.organisations_organisation_id_seq', 315, true);


--
-- Name: ratings_reviews_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ratings_reviews_review_id_seq', 1, true);


--
-- Name: review_flags_flag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.review_flags_flag_id_seq', 1, false);


--
-- Name: roles_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.roles_role_id_seq', 4, true);


--
-- Name: saved_organisations_saved_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.saved_organisations_saved_id_seq', 3, true);


--
-- Name: user_availability_availability_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_availability_availability_id_seq', 1, false);


--
-- Name: user_preferences_preference_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_preferences_preference_id_seq', 24, true);


--
-- Name: user_skills_user_skill_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_skills_user_skill_id_seq', 15, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_user_id_seq', 532, true);


--
-- Name: volunteer_allocations_allocation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.volunteer_allocations_allocation_id_seq', 1, false);


--
-- Name: volunteer_needs_volunteer_need_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.volunteer_needs_volunteer_need_id_seq', 1, false);


--
-- Name: volunteer_required_skills_required_skill_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.volunteer_required_skills_required_skill_id_seq', 1, false);


--
-- Name: volunteer_signups_signup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.volunteer_signups_signup_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_id);


--
-- Name: conversations conversations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_pkey PRIMARY KEY (conversation_id);


--
-- Name: engagement_logs engagement_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.engagement_logs
    ADD CONSTRAINT engagement_logs_pkey PRIMARY KEY (engagement_id);


--
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (location_id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (message_id);


--
-- Name: monthly_business_reports monthly_business_reports_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monthly_business_reports
    ADD CONSTRAINT monthly_business_reports_pkey PRIMARY KEY (report_id);


--
-- Name: organisation_categories organisation_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisation_categories
    ADD CONSTRAINT organisation_categories_pkey PRIMARY KEY (organisation_category_id);


--
-- Name: organisation_factors organisation_factors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisation_factors
    ADD CONSTRAINT organisation_factors_pkey PRIMARY KEY (organisation_id);


--
-- Name: organisation_images organisation_images_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisation_images
    ADD CONSTRAINT organisation_images_pkey PRIMARY KEY (image_id);


--
-- Name: organisations organisations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisations
    ADD CONSTRAINT organisations_pkey PRIMARY KEY (organisation_id);


--
-- Name: ratings_reviews ratings_reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ratings_reviews
    ADD CONSTRAINT ratings_reviews_pkey PRIMARY KEY (review_id);


--
-- Name: review_flags review_flags_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.review_flags
    ADD CONSTRAINT review_flags_pkey PRIMARY KEY (flag_id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role_id);


--
-- Name: roles roles_role_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_role_name_key UNIQUE (role_name);


--
-- Name: saved_organisations saved_organisations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saved_organisations
    ADD CONSTRAINT saved_organisations_pkey PRIMARY KEY (saved_id);


--
-- Name: monthly_business_reports unique_monthly_report; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monthly_business_reports
    ADD CONSTRAINT unique_monthly_report UNIQUE (organisation_id, report_month, report_year);


--
-- Name: organisation_categories unique_organisation_category; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisation_categories
    ADD CONSTRAINT unique_organisation_category UNIQUE (organisation_id, category_id);


--
-- Name: user_availability user_availability_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_availability
    ADD CONSTRAINT user_availability_pkey PRIMARY KEY (availability_id);


--
-- Name: user_factors user_factors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_factors
    ADD CONSTRAINT user_factors_pkey PRIMARY KEY (user_id);


--
-- Name: user_preferences user_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_pkey PRIMARY KEY (preference_id);


--
-- Name: user_skills user_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_skills
    ADD CONSTRAINT user_skills_pkey PRIMARY KEY (user_skill_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: volunteer_allocations volunteer_allocations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.volunteer_allocations
    ADD CONSTRAINT volunteer_allocations_pkey PRIMARY KEY (allocation_id);


--
-- Name: volunteer_needs volunteer_needs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.volunteer_needs
    ADD CONSTRAINT volunteer_needs_pkey PRIMARY KEY (volunteer_need_id);


--
-- Name: volunteer_required_skills volunteer_required_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.volunteer_required_skills
    ADD CONSTRAINT volunteer_required_skills_pkey PRIMARY KEY (required_skill_id);


--
-- Name: volunteer_signups volunteer_signups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.volunteer_signups
    ADD CONSTRAINT volunteer_signups_pkey PRIMARY KEY (signup_id);


--
-- Name: unique_monthly_report_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX unique_monthly_report_idx ON public.monthly_business_reports USING btree (organisation_id, report_month, report_year);


--
-- Name: messages trg_log_message_engagement; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_log_message_engagement AFTER INSERT ON public.messages FOR EACH ROW EXECUTE FUNCTION public.log_message_engagement();


--
-- Name: ratings_reviews trg_log_rating_engagement; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_log_rating_engagement AFTER INSERT ON public.ratings_reviews FOR EACH ROW EXECUTE FUNCTION public.log_rating_engagement();


--
-- Name: saved_organisations trg_log_save_engagement; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_log_save_engagement AFTER INSERT ON public.saved_organisations FOR EACH ROW EXECUTE FUNCTION public.log_save_engagement();


--
-- Name: conversations conversations_organisation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id);


--
-- Name: conversations conversations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: engagement_logs engagement_logs_organisation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.engagement_logs
    ADD CONSTRAINT engagement_logs_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id);


--
-- Name: engagement_logs engagement_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.engagement_logs
    ADD CONSTRAINT engagement_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: organisation_categories fk_org_category_category; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisation_categories
    ADD CONSTRAINT fk_org_category_category FOREIGN KEY (category_id) REFERENCES public.categories(category_id) ON DELETE CASCADE;


--
-- Name: organisation_categories fk_org_category_organisation; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisation_categories
    ADD CONSTRAINT fk_org_category_organisation FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id) ON DELETE CASCADE;


--
-- Name: users fk_users_location; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_users_location FOREIGN KEY (location_id) REFERENCES public.locations(location_id) ON DELETE SET NULL;


--
-- Name: messages messages_conversation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_conversation_id_fkey FOREIGN KEY (conversation_id) REFERENCES public.conversations(conversation_id);


--
-- Name: messages messages_sender_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_sender_user_id_fkey FOREIGN KEY (sender_user_id) REFERENCES public.users(user_id);


--
-- Name: monthly_business_reports monthly_business_reports_organisation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.monthly_business_reports
    ADD CONSTRAINT monthly_business_reports_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id);


--
-- Name: organisation_factors organisation_factors_organisation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisation_factors
    ADD CONSTRAINT organisation_factors_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id);


--
-- Name: organisation_images organisation_images_organisation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisation_images
    ADD CONSTRAINT organisation_images_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id);


--
-- Name: organisations organisations_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisations
    ADD CONSTRAINT organisations_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(category_id);


--
-- Name: organisations organisations_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisations
    ADD CONSTRAINT organisations_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.locations(location_id);


--
-- Name: organisations organisations_owner_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisations
    ADD CONSTRAINT organisations_owner_user_id_fkey FOREIGN KEY (owner_user_id) REFERENCES public.users(user_id);


--
-- Name: ratings_reviews ratings_reviews_organisation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ratings_reviews
    ADD CONSTRAINT ratings_reviews_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id);


--
-- Name: ratings_reviews ratings_reviews_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ratings_reviews
    ADD CONSTRAINT ratings_reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: review_flags review_flags_flagged_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.review_flags
    ADD CONSTRAINT review_flags_flagged_by_user_id_fkey FOREIGN KEY (flagged_by_user_id) REFERENCES public.users(user_id);


--
-- Name: review_flags review_flags_review_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.review_flags
    ADD CONSTRAINT review_flags_review_id_fkey FOREIGN KEY (review_id) REFERENCES public.ratings_reviews(review_id);


--
-- Name: saved_organisations saved_organisations_organisation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saved_organisations
    ADD CONSTRAINT saved_organisations_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id);


--
-- Name: saved_organisations saved_organisations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saved_organisations
    ADD CONSTRAINT saved_organisations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_availability user_availability_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_availability
    ADD CONSTRAINT user_availability_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_factors user_factors_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_factors
    ADD CONSTRAINT user_factors_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_preferences user_preferences_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(category_id);


--
-- Name: user_preferences user_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_skills user_skills_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_skills
    ADD CONSTRAINT user_skills_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(role_id);


--
-- Name: volunteer_allocations volunteer_allocations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.volunteer_allocations
    ADD CONSTRAINT volunteer_allocations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: volunteer_allocations volunteer_allocations_volunteer_need_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.volunteer_allocations
    ADD CONSTRAINT volunteer_allocations_volunteer_need_id_fkey FOREIGN KEY (volunteer_need_id) REFERENCES public.volunteer_needs(volunteer_need_id);


--
-- Name: volunteer_needs volunteer_needs_organisation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.volunteer_needs
    ADD CONSTRAINT volunteer_needs_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES public.organisations(organisation_id);


--
-- Name: volunteer_required_skills volunteer_required_skills_volunteer_need_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.volunteer_required_skills
    ADD CONSTRAINT volunteer_required_skills_volunteer_need_id_fkey FOREIGN KEY (volunteer_need_id) REFERENCES public.volunteer_needs(volunteer_need_id);


--
-- Name: volunteer_signups volunteer_signups_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.volunteer_signups
    ADD CONSTRAINT volunteer_signups_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: volunteer_signups volunteer_signups_volunteer_need_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.volunteer_signups
    ADD CONSTRAINT volunteer_signups_volunteer_need_id_fkey FOREIGN KEY (volunteer_need_id) REFERENCES public.volunteer_needs(volunteer_need_id);


--
-- PostgreSQL database dump complete
--

\unrestrict BdZoxhMgwjdZYKRPbVwwDvmBTPHkCRJkcERikXw0gZAnKdIUVgfjzaX6jsj4Mho

