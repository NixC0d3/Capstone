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


# ---------------------------------------------------------
# Helper function: get the currently logged-in user
# ---------------------------------------------------------
def get_current_user():
    """Return the logged-in user object, or None if nobody is logged in."""
    user_id = session.get("user_id")

    if not user_id:
        return None

    return User.query.get(user_id)


# ---------------------------------------------------------
# Helper decorator: protect pages that require login
# ---------------------------------------------------------
def login_required(route_function):
    """Prevent users from accessing certain routes unless they are logged in."""
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in first.")
            return redirect(url_for("page_bp.login"))

        return route_function(*args, **kwargs)

    return wrapper


# ---------------------------------------------------------
# Helper function: get all categories for one organisation
# ---------------------------------------------------------
def get_categories_for_organisation(organisation_id):
    """
    Get all category names linked to one organisation.

    This uses organisation_categories because one organisation can now
    belong to more than one category.
    """
    result = db.session.execute(
        text("""
            SELECT c.category_name
            FROM organisation_categories oc
            JOIN categories c
                ON oc.category_id = c.category_id
            WHERE oc.organisation_id = :organisation_id
            ORDER BY c.category_name;
        """),
        {"organisation_id": organisation_id}
    ).fetchall()

    return [row[0] for row in result]


# ---------------------------------------------------------
# Home page
# ---------------------------------------------------------
@page_bp.route("/")
def home():
    return redirect(url_for("page_bp.explore"))


# ---------------------------------------------------------
# Explore organisations + filtering
# ---------------------------------------------------------
@page_bp.route("/explore")
def explore():
    """
    Shows all organisations and allows filtering by:
    - search text
    - organisation type
    - category

    It also passes saved_ids to the template so a logged-in user can see
    whether each organisation is already saved.
    """
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
        organisation_ids_result = db.session.execute(
            text("""
                SELECT organisation_id
                FROM organisation_categories
                WHERE category_id = :category_id
            """),
            {"category_id": int(category_id)}
        ).fetchall()

        organisation_ids = [row[0] for row in organisation_ids_result]

        if organisation_ids:
            query = query.filter(Organisation.organisation_id.in_(organisation_ids))
        else:
            query = query.filter(False)

    organisations = query.order_by(Organisation.organisation_name.asc()).all()
    categories = Category.query.order_by(Category.category_name.asc()).all()

    # Get saved organisation IDs for the logged-in user.
    # This allows the Explore grid to show Save or Remove from Saved.
    saved_ids = []

    if session.get("user_id"):
        saved_records = SavedOrganisation.query.filter_by(
            user_id=session.get("user_id")
        ).all()

        saved_ids = [record.organisation_id for record in saved_records]

    return render_template(
        "explore.html",
        organisations=organisations,
        categories=categories,
        search=search,
        organisation_type=organisation_type,
        category_id=category_id,
        saved_ids=saved_ids
    )


# ---------------------------------------------------------
# Register
# ---------------------------------------------------------
@page_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Registration page with three account types:
    - general_user
    - business_user
    - charity_user
    """
    if request.method == "POST":
        account_type = request.form.get("account_type")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not account_type or not email or not password or not confirm_password:
            flash("Please fill out all required fields.")
            return redirect(url_for("page_bp.register"))

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("page_bp.register"))

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

            name_parts = owner_name.split()

            if len(name_parts) == 1:
                first_name = name_parts[0]
                last_name = "Owner"
            else:
                first_name = name_parts[0]
                last_name = " ".join(name_parts[1:])

            user = User(
                role_id=role.role_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=generate_password_hash(password)
            )

            db.session.add(user)
            db.session.flush()

            location = Location(
                parish=parish,
                town=city_town,
                address=street_address
            )

            db.session.add(location)
            db.session.flush()

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

            for selected_category_id in selected_categories:
                db.session.execute(
                    text("""
                        INSERT INTO organisation_categories (organisation_id, category_id)
                        VALUES (:organisation_id, :category_id)
                        ON CONFLICT (organisation_id, category_id) DO NOTHING;
                    """),
                    {
                        "organisation_id": organisation.organisation_id,
                        "category_id": int(selected_category_id)
                    }
                )

            db.session.commit()

            flash("Account and organisation profile created. Please log in.")
            return redirect(url_for("page_bp.login"))

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


# ---------------------------------------------------------
# Login
# ---------------------------------------------------------
@page_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Logs users into the basic Flask layout.

    This supports:
    - normal email login
    - imported demo usernames such as gen10, bus1000, char2000
    - hashed passwords for newly registered users
    - plain demo passwords for imported Excel users
    """
    if request.method == "POST":
        login_value = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        user = User.query.filter(
            db.func.lower(User.email) == login_value
        ).first()

        if not user and "@" not in login_value:
            user = User.query.filter(
                User.email.ilike(f"{login_value}.%@civilinfohub.test")
            ).first()

        if not user:
            flash("Invalid email or password.")
            return redirect(url_for("page_bp.login"))

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


# ---------------------------------------------------------
# Logout
# ---------------------------------------------------------
@page_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("page_bp.login"))


# ---------------------------------------------------------
# Organisation details
# ---------------------------------------------------------
@page_bp.route("/organisations/<int:organisation_id>")
def organisation_details(organisation_id):
    """
    Shows the details of one organisation.
    Also shows rating summary, existing reviews, category names, and save button.
    """
    organisation = Organisation.query.get_or_404(organisation_id)

    reviews = (
        RatingReview.query
        .filter_by(organisation_id=organisation_id, is_hidden=False)
        .order_by(RatingReview.created_at.desc())
        .all()
    )

    total_reviews = len(reviews)

    if total_reviews > 0:
        average_rating = sum(review.rating for review in reviews) / total_reviews
    else:
        average_rating = 0

    current_user = get_current_user()
    already_saved = False

    if current_user:
        saved_record = SavedOrganisation.query.filter_by(
            user_id=current_user.user_id,
            organisation_id=organisation_id
        ).first()

        already_saved = saved_record is not None

    category_names = get_categories_for_organisation(organisation_id)

    return render_template(
        "organisation_details.html",
        organisation=organisation,
        reviews=reviews,
        total_reviews=total_reviews,
        average_rating=average_rating,
        already_saved=already_saved,
        category_names=category_names
    )


# ---------------------------------------------------------
# Add or update rating/review
# ---------------------------------------------------------
@page_bp.route("/organisations/<int:organisation_id>/review", methods=["POST"])
@login_required
def add_review(organisation_id):
    """
    Allows a logged-in user to rate and review an organisation.

    If the user already reviewed the organisation, the old review is updated
    instead of creating a duplicate review.
    """
    user_id = session.get("user_id")

    rating = request.form.get("rating")
    review_text = request.form.get("review_text", "").strip()

    if not rating:
        flash("Please select a rating.")
        return redirect(url_for("page_bp.organisation_details", organisation_id=organisation_id))

    rating = int(rating)

    if rating < 1 or rating > 5:
        flash("Rating must be between 1 and 5.")
        return redirect(url_for("page_bp.organisation_details", organisation_id=organisation_id))

    existing_review = RatingReview.query.filter_by(
        user_id=user_id,
        organisation_id=organisation_id
    ).first()

    if existing_review:
        existing_review.rating = rating
        existing_review.review_text = review_text
    else:
        review = RatingReview(
            user_id=user_id,
            organisation_id=organisation_id,
            rating=rating,
            review_text=review_text
        )

        db.session.add(review)

    db.session.commit()

    flash("Review saved successfully.")
    return redirect(url_for("page_bp.organisation_details", organisation_id=organisation_id))


# ---------------------------------------------------------
# Save organisation
# ---------------------------------------------------------
@page_bp.route("/organisations/<int:organisation_id>/save", methods=["POST"])
@login_required
def save_organisation(organisation_id):
    """Save/bookmark an organisation for the logged-in user."""
    user_id = session.get("user_id")

    existing_save = SavedOrganisation.query.filter_by(
        user_id=user_id,
        organisation_id=organisation_id
    ).first()

    if existing_save:
        flash("This organisation is already saved.")
    else:
        saved = SavedOrganisation(
            user_id=user_id,
            organisation_id=organisation_id
        )

        db.session.add(saved)
        db.session.commit()

        flash("Organisation saved.")

    return redirect(request.referrer or url_for("page_bp.organisation_details", organisation_id=organisation_id))


# ---------------------------------------------------------
# Remove saved organisation
# ---------------------------------------------------------
@page_bp.route("/organisations/<int:organisation_id>/unsave", methods=["POST"])
@login_required
def unsave_organisation(organisation_id):
    """Remove an organisation from the logged-in user's saved list."""
    user_id = session.get("user_id")

    saved = SavedOrganisation.query.filter_by(
        user_id=user_id,
        organisation_id=organisation_id
    ).first()

    if saved:
        db.session.delete(saved)
        db.session.commit()
        flash("Organisation removed from saved list.")
    else:
        flash("This organisation was not in your saved list.")

    return redirect(request.referrer or url_for("page_bp.organisation_details", organisation_id=organisation_id))


# ---------------------------------------------------------
# View saved organisations
# ---------------------------------------------------------
@page_bp.route("/saved")
@login_required
def saved_organisations():
    """Shows all organisations saved by the logged-in user."""
    user_id = session.get("user_id")

    saved_records = (
        db.session.query(SavedOrganisation, Organisation)
        .join(Organisation, SavedOrganisation.organisation_id == Organisation.organisation_id)
        .filter(SavedOrganisation.user_id == user_id)
        .order_by(SavedOrganisation.saved_at.desc())
        .all()
    )

    return render_template("saved.html", saved_records=saved_records)
