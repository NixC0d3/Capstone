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
    RatingReview,
    SavedOrganisation
)

page_bp = Blueprint("page_bp", __name__)


# ---------------------------------------------------------
# Helper function: get the currently logged-in user
# ---------------------------------------------------------
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return None

    return User.query.get(user_id)


# ---------------------------------------------------------
# Helper decorator: protect pages that require login
# ---------------------------------------------------------
def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in first.")
            return redirect(url_for("page_bp.login"))

        return route_function(*args, **kwargs)

    return wrapper


# ---------------------------------------------------------
# Home page
# ---------------------------------------------------------
@page_bp.route("/")
def home():
    return redirect(url_for("page_bp.explore"))


# ---------------------------------------------------------
# Register
# ---------------------------------------------------------
@page_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        role_name = request.form.get("role_name")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Basic validation
        if not role_name or not first_name or not last_name or not email or not password:
            flash("All fields are required.")
            return redirect(url_for("page_bp.register"))

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("An account with this email already exists.")
            return redirect(url_for("page_bp.register"))

        # Find selected role
        role = Role.query.filter_by(role_name=role_name).first()

        if not role:
            flash("Invalid role selected.")
            return redirect(url_for("page_bp.register"))

        # Store hashed password, not plain text
        user = User(
            role_id=role.role_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for("page_bp.login"))

    roles = Role.query.all()
    return render_template("register.html", roles=roles)


# ---------------------------------------------------------
# Login
# ---------------------------------------------------------
@page_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Invalid email or password.")
            return redirect(url_for("page_bp.login"))

        # Some old imported users may have plain text passwords.
        # This allows both hashed passwords and simple demo passwords.
        password_is_correct = False

        if user.password_hash:
            try:
                password_is_correct = check_password_hash(user.password_hash, password)
            except ValueError:
                password_is_correct = user.password_hash == password

        if not password_is_correct:
            flash("Invalid email or password.")
            return redirect(url_for("page_bp.login"))

        # Store user ID in session after successful login
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
# Explore organisations with filtering
# ---------------------------------------------------------
@page_bp.route("/explore")
def explore():
    search = request.args.get("search", "").strip()
    organisation_type = request.args.get("organisation_type", "").strip()
    category_id = request.args.get("category_id", "").strip()

    query = Organisation.query

    # Filter by business or charity
    if organisation_type:
        query = query.filter(Organisation.organisation_type == organisation_type)

    # Search by organisation name or description
    if search:
        query = query.filter(
            Organisation.organisation_name.ilike(f"%{search}%")
            | Organisation.description.ilike(f"%{search}%")
        )

    # Filter by category using organisation_categories table
    if category_id:
        query = query.join(
            text(
                "organisation_categories ON organisations.organisation_id = organisation_categories.organisation_id"
            )
        ).filter(
            text("organisation_categories.category_id = :category_id")
        ).params(category_id=category_id)

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


# ---------------------------------------------------------
# View one organisation
# ---------------------------------------------------------
@page_bp.route("/organisations/<int:organisation_id>")
def organisation_details(organisation_id):
    organisation = Organisation.query.get_or_404(organisation_id)

    reviews = RatingReview.query.filter_by(
        organisation_id=organisation_id,
        is_hidden=False
    ).order_by(RatingReview.created_at.desc()).all()

    # Calculate average rating
    total_reviews = len(reviews)

    if total_reviews > 0:
        average_rating = sum(review.rating for review in reviews) / total_reviews
    else:
        average_rating = 0

    current_user = get_current_user()

    already_saved = False

    if current_user:
        saved = SavedOrganisation.query.filter_by(
            user_id=current_user.user_id,
            organisation_id=organisation_id
        ).first()

        already_saved = saved is not None

    return render_template(
        "organisation_details.html",
        organisation=organisation,
        reviews=reviews,
        average_rating=average_rating,
        total_reviews=total_reviews,
        already_saved=already_saved
    )


# ---------------------------------------------------------
# Add rating/review
# ---------------------------------------------------------
@page_bp.route("/organisations/<int:organisation_id>/review", methods=["POST"])
@login_required
def add_review(organisation_id):
    user_id = session.get("user_id")
    rating = request.form.get("rating")
    review_text = request.form.get("review_text")

    if not rating:
        flash("Rating is required.")
        return redirect(url_for("page_bp.organisation_details", organisation_id=organisation_id))

    rating = int(rating)

    if rating < 1 or rating > 5:
        flash("Rating must be between 1 and 5.")
        return redirect(url_for("page_bp.organisation_details", organisation_id=organisation_id))

    # Check if this user already reviewed this organisation
    existing_review = RatingReview.query.filter_by(
        user_id=user_id,
        organisation_id=organisation_id
    ).first()

    if existing_review:
        # Update existing review instead of creating a duplicate
        existing_review.rating = rating
        existing_review.review_text = review_text
    else:
        review = RatingReview(
            organisation_id=organisation_id,
            user_id=user_id,
            rating=rating,
            review_text=review_text
        )

        db.session.add(review)

    db.session.commit()

    flash("Review saved successfully.")
    return redirect(url_for("page_bp.organisation_details", organisation_id=organisation_id))


# ---------------------------------------------------------
# Save/bookmark organisation
# ---------------------------------------------------------
@page_bp.route("/organisations/<int:organisation_id>/save", methods=["POST"])
@login_required
def save_organisation(organisation_id):
    user_id = session.get("user_id")

    existing_save = SavedOrganisation.query.filter_by(
        user_id=user_id,
        organisation_id=organisation_id
    ).first()

    if existing_save:
        flash("Organisation is already saved.")
    else:
        saved = SavedOrganisation(
            user_id=user_id,
            organisation_id=organisation_id
        )

        db.session.add(saved)
        db.session.commit()

        flash("Organisation saved.")

    return redirect(url_for("page_bp.organisation_details", organisation_id=organisation_id))


# ---------------------------------------------------------
# Remove saved organisation
# ---------------------------------------------------------
@page_bp.route("/organisations/<int:organisation_id>/unsave", methods=["POST"])
@login_required
def unsave_organisation(organisation_id):
    user_id = session.get("user_id")

    saved = SavedOrganisation.query.filter_by(
        user_id=user_id,
        organisation_id=organisation_id
    ).first()

    if saved:
        db.session.delete(saved)
        db.session.commit()
        flash("Organisation removed from saved list.")

    return redirect(url_for("page_bp.organisation_details", organisation_id=organisation_id))


# ---------------------------------------------------------
# View saved organisations
# ---------------------------------------------------------
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
