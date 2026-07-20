from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models import (
    User,
    Role,
    Organisation,
    Category,
    Location,
    RatingReview,
    SavedOrganisation
)

# Create the Blueprint before using @page_bp.route
page_bp = Blueprint("page_bp", __name__)

@page_bp.route("/")
def home():
    return redirect(url_for("page_bp.explore"))


@page_bp.route("/explore")
def explore():
    search = request.args.get("search", "").strip()
    organisation_type = request.args.get("organisation_type", "").strip()
    category_id = request.args.get("category_id", "").strip()

    query = Organisation.query

    # Filter by organisation type: business or charity
    if organisation_type:
        query = query.filter(Organisation.organisation_type == organisation_type)

    # Search by organisation name or description
    if search:
        query = query.filter(
            Organisation.organisation_name.ilike(f"%{search}%")
            | Organisation.description.ilike(f"%{search}%")
        )

    # Filter by category using the organisation_categories linking table
    if category_id:
        query = query.filter(
            Organisation.organisation_id.in_(
                db.session.execute(
                    text("""
                        SELECT organisation_id
                        FROM organisation_categories
                        WHERE category_id = :category_id
                    """),
                    {"category_id": category_id}
                ).scalars()
            )
        )

    organisations = query.order_by(Organisation.organisation_name.asc()).all()
    categories = Category.query.order_by(Category.category_name.asc()).all()

    return render_template(
        "explore.html",
        organisations=organisations,
        categories=categories,
        search=search,
        organisation_type=organisation_type,
        category_id=category_id
    )

@page_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        account_type = request.form.get("account_type")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Basic validation
        if not account_type or not email or not password or not confirm_password:
            flash("Please fill out all required fields.")
            return redirect(url_for("page_bp.register"))

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("page_bp.register"))

        # Check if email is already used
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("An account with this email already exists.")
            return redirect(url_for("page_bp.register"))

        role = Role.query.filter_by(role_name=account_type).first()

        if not role:
            flash("Invalid account type selected.")
            return redirect(url_for("page_bp.register"))

        # -----------------------------
        # General user registration
        # -----------------------------
        if account_type == "general_user":
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")

            if not first_name or not last_name:
                flash("Please enter your first and last name.")
                return redirect(url_for("page_bp.register"))

            user = User(
                role_id=role.role_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=generate_password_hash(password)
            )

            db.session.add(user)
            db.session.commit()

            flash("General user account created. Please log in.")
            return redirect(url_for("page_bp.login"))

        # -----------------------------
        # Business / charity registration
        # -----------------------------
        if account_type in ["business_user", "charity_user"]:
            owner_name = request.form.get("owner_name")
            organisation_name = request.form.get("organisation_name")
            phone = request.form.get("phone")
            street_address = request.form.get("street_address")
            city_town = request.form.get("city_town")
            parish = request.form.get("parish")
            description = request.form.get("description")
            website_url = request.form.get("website_url")
            selected_categories = request.form.getlist("category_ids")

            if not owner_name or not organisation_name:
                flash("Owner name and organisation name are required.")
                return redirect(url_for("page_bp.register"))

            if not selected_categories:
                flash("Please select at least one category.")
                return redirect(url_for("page_bp.register"))

            # Split owner name into first and last name
            name_parts = owner_name.split()

            if len(name_parts) == 1:
                first_name = name_parts[0]
                last_name = "Owner"
            else:
                first_name = name_parts[0]
                last_name = " ".join(name_parts[1:])

            # Create the user account first
            user = User(
                role_id=role.role_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=generate_password_hash(password)
            )

            db.session.add(user)
            db.session.flush()

            # Create location record
            location = Location(
                parish=parish,
                town=city_town,
                address=street_address
            )

            db.session.add(location)
            db.session.flush()

            # First selected category becomes the main category
            main_category_id = int(selected_categories[0])

            organisation_type = "business"

            if account_type == "charity_user":
                organisation_type = "charity"

            organisation = Organisation(
                owner_user_id=user.user_id,
                category_id=main_category_id,
                location_id=location.location_id,
                organisation_name=organisation_name,
                organisation_type=organisation_type,
                description=description,
                phone=phone,
                email=email,
                website_url=website_url
            )

            db.session.add(organisation)
            db.session.flush()

            # Link organisation to all selected categories
            for category_id in selected_categories:
                db.session.execute(
                    text("""
                        INSERT INTO organisation_categories (organisation_id, category_id)
                        VALUES (:organisation_id, :category_id)
                        ON CONFLICT (organisation_id, category_id) DO NOTHING;
                    """),
                    {
                        "organisation_id": organisation.organisation_id,
                        "category_id": int(category_id)
                    }
                )

            db.session.commit()

            flash("Account and organisation profile created. Please log in.")
            return redirect(url_for("page_bp.login"))

    # Get categories for the register page
    business_categories = Category.query.filter(
        Category.category_type.in_(["business", "both"])
    ).order_by(Category.category_name.asc()).all()

    charity_categories = Category.query.filter(
        Category.category_type.in_(["charity", "both"])
    ).order_by(Category.category_name.asc()).all()

    return render_template(
        "register.html",
        business_categories=business_categories,
        charity_categories=charity_categories
    )

@page_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_value = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        # First try normal email login
        user = User.query.filter(
            db.func.lower(User.email) == login_value
        ).first()

        # If the user typed only a username like gen10, bus1000, or char2000,
        # try to find the demo email created by the import script.
        if not user and "@" not in login_value:
            user = User.query.filter(
                User.email.ilike(f"{login_value}.%@civilinfohub.test")
            ).first()

        if not user:
            flash("Invalid email or password.")
            return redirect(url_for("page_bp.login"))

        # Imported Excel users may have plain demo passwords.
        # Newly registered users have hashed passwords.
        password_is_correct = False

        if user.password_hash == password:
            password_is_correct = True
        else:
            try:
                password_is_correct = check_password_hash(user.password_hash, password)
            except ValueError:
                password_is_correct = False

        if not password_is_correct:
            flash("Invalid email or password.")
            return redirect(url_for("page_bp.login"))

        session["user_id"] = user.user_id
        session["user_name"] = f"{user.first_name} {user.last_name}"

        flash("Login successful.")
        return redirect(url_for("page_bp.explore"))

    return render_template("login.html")

@page_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("page_bp.login"))


def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in first.")
            return redirect(url_for("page_bp.login"))

        return route_function(*args, **kwargs)

    return wrapper

@page_bp.route("/saved")
@login_required
def saved_organisations():
    user_id = session.get("user_id")

    saved_records = (
        db.session.query(SavedOrganisation, Organisation)
        .join(Organisation, SavedOrganisation.organisation_id == Organisation.organisation_id)
        .filter(SavedOrganisation.user_id == user_id)
        .order_by(SavedOrganisation.saved_at.desc())
        .all()
    )

    return render_template("saved.html", saved_records=saved_records)
