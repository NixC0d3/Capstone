"""
CivilInfoHub Recommendation Service
===================================

This version is for the database design where these two model classes exist:

    UserFactor
    OrganisationFactor

Those tables store the trained SVD vectors after training.

Main idea
---------
1. Gather user-organisation interaction data.
2. Convert it into a user-organisation matrix.
3. Train TruncatedSVD.
4. Store learned user vectors in user_factors.
5. Store learned organisation vectors in organisation_factors.
6. Use dot product scores to recommend organisations.

The system is still HYBRID:
    - user preference/category matching helps new users
    - popularity helps fallback recommendations
    - SVD factor scores help personalised recommendations after training

Recommended spreadsheet location
--------------------------------
Put the training spreadsheet here:

    BACKEND/app/data/Training Data - Recommendations.xlsx

The spreadsheet is optional. The better final system should train mainly from
the database tables as users rate, save, view, and message organisations.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sqlalchemy import bindparam, text

from app.extensions import db
from app.models import (
    User,
    Organisation,
    UserPreference,
    RatingReview,
    SavedOrganisation,
    EngagementLog,
    UserFactor,
    OrganisationFactor,
)


# ----------------------------------------------------------------------
# Spreadsheet settings
# ----------------------------------------------------------------------

TRAINING_FILE_NAME = "Training Data - Recommendations.xlsx"


def find_training_file():
    """
    Find the Excel training spreadsheet.

    Recommended location:
        BACKEND/app/data/Training Data - Recommendations.xlsx

    The function also checks a few backup locations so the project still works
    if the file is temporarily placed somewhere else.
    """
    current_file = Path(__file__).resolve()

    services_folder = current_file.parent
    app_folder = current_file.parent.parent
    backend_folder = current_file.parent.parent.parent

    possible_paths = [
        app_folder / "data" / TRAINING_FILE_NAME,       # recommended location
        backend_folder / "data" / TRAINING_FILE_NAME,   # BACKEND/data
        services_folder / TRAINING_FILE_NAME,           # BACKEND/app/services
        app_folder / TRAINING_FILE_NAME,                # BACKEND/app
        backend_folder / TRAINING_FILE_NAME,            # BACKEND
        Path.cwd() / TRAINING_FILE_NAME,                # folder where Flask was run
    ]

    for path in possible_paths:
        if path.exists():
            return path

    return None


# ----------------------------------------------------------------------
# Interaction weights
# ----------------------------------------------------------------------

def get_weight_from_pattern(pattern):
    """
    Convert the spreadsheet interaction pattern into a numeric weight.

    Pattern guide:
        0 = no interaction
        1 = viewed only
        2 = viewed + one action
        3 = viewed + two actions
        4 = viewed + rating + review + save

    Stronger interaction = higher weight.
    """
    pattern = int(pattern)

    if pattern >= 4:
        return 7.0
    if pattern == 3:
        return 5.0
    if pattern == 2:
        return 3.0
    if pattern == 1:
        return 1.0

    return 0.0


def get_match_level(score):
    """
    Convert a final 0-1 recommendation score into a user-friendly label.
    """
    if score >= 0.80:
        return "Excellent Match"
    if score >= 0.60:
        return "Good Match"
    if score >= 0.40:
        return "Moderate Match"
    if score >= 0.20:
        return "Basic Match"

    return "Potential Match"


# ----------------------------------------------------------------------
# Spreadsheet data
# ----------------------------------------------------------------------

def load_ratings_from_spreadsheet(user_id_offset=0, organisation_id_offset=0):
    """
    Load training interactions from the Excel matrix.

    Important:
    The matrix sheet appears to use:
        row 0 = category/category-code labels
        row 1 = actual organisation IDs
        row 2 onward = user interaction rows

    This is why header=None is used.

    user_id_offset:
        Use 0 if the spreadsheet already has real user IDs.
        Use 30000 if the spreadsheet has training users 1, 2, 3...
        but your real seeded user IDs begin around 30001.

    organisation_id_offset:
        Use 0 if spreadsheet organisation IDs match the database.
        Use -999 if the spreadsheet organisation IDs are 1000, 1001, 1002...
        but your database organisation IDs are 1, 2, 3...
    """
    training_path = find_training_file()

    if not training_path:
        print("Training spreadsheet not found.")
        return []

    try:
        raw_matrix = pd.read_excel(
            training_path,
            sheet_name="Matrix",
            header=None,
        )
    except Exception as error:
        print(f"Error reading training spreadsheet: {error}")
        return []

    if raw_matrix.shape[0] < 3 or raw_matrix.shape[1] < 2:
        return []

    organisation_ids = raw_matrix.iloc[1, 1:].tolist()
    records = []

    for row_index in range(2, len(raw_matrix)):
        raw_user_id = raw_matrix.iloc[row_index, 0]

        if pd.isna(raw_user_id):
            continue

        try:
            user_id = int(raw_user_id) + int(user_id_offset)
        except ValueError:
            continue

        for column_offset, raw_organisation_id in enumerate(organisation_ids, start=1):
            if pd.isna(raw_organisation_id):
                continue

            pattern = raw_matrix.iloc[row_index, column_offset]

            if pd.isna(pattern):
                continue

            try:
                organisation_id = int(raw_organisation_id) + int(organisation_id_offset)
                pattern = int(pattern)
            except ValueError:
                continue

            weight = get_weight_from_pattern(pattern)

            if weight <= 0:
                continue

            records.append({
                "user_id": user_id,
                "organisation_id": organisation_id,
                "interaction_score": weight,
                "interaction_pattern": pattern,
                "source": "spreadsheet",
            })

    return records


def spreadsheet_preview(user_id_offset=0, organisation_id_offset=0, sample_size=10):
    """
    Return a small preview of spreadsheet records for testing.

    The preview helps confirm whether the spreadsheet IDs are being converted
    into the same IDs used by your database.
    """
    records = load_ratings_from_spreadsheet(
        user_id_offset=user_id_offset,
        organisation_id_offset=organisation_id_offset,
    )

    return {
        "spreadsheet_found": find_training_file() is not None,
        "user_id_offset": int(user_id_offset),
        "organisation_id_offset": int(organisation_id_offset),
        "records_found": len(records),
        "sample": records[:sample_size],
    }


# ----------------------------------------------------------------------
# Database interaction data
# ----------------------------------------------------------------------

def build_interaction_dataframe_from_db():
    """
    Build training data from actual application database tables.

    Output:
        DataFrame with user_id, organisation_id, interaction_score.

    Sources:
        ratings_reviews       -> explicit ratings
        saved_organisations   -> implicit positive interest
        engagement_logs       -> views, messages, saves, reviews, signups

    If the same user interacts with the same organisation many times,
    the strongest score is kept.
    """
    records = []

    # 1. Explicit ratings from reviews.
    reviews = RatingReview.query.filter_by(is_hidden=False).all()

    for review in reviews:
        records.append({
            "user_id": review.user_id,
            "organisation_id": review.organisation_id,
            "interaction_score": float(review.rating),
            "source": "rating_review",
        })

    # 2. Saved organisations.
    saved_items = SavedOrganisation.query.all()

    for saved in saved_items:
        records.append({
            "user_id": saved.user_id,
            "organisation_id": saved.organisation_id,
            "interaction_score": 4.0,
            "source": "saved_organisation",
        })

    # 3. Engagement logs.
    engagement_weights = {
        "view": 1.0,
        "profile_view": 1.0,
        "save": 4.0,
        "saved": 4.0,
        "message": 4.0,
        "rating": 5.0,
        "review": 5.0,
        "volunteer_signup": 5.0,
    }

    engagement_logs = EngagementLog.query.filter(
        EngagementLog.user_id.isnot(None)
    ).all()

    for log in engagement_logs:
        score = engagement_weights.get(log.engagement_type, 1.0)

        records.append({
            "user_id": log.user_id,
            "organisation_id": log.organisation_id,
            "interaction_score": score,
            "source": "engagement_log",
        })

    if not records:
        return pd.DataFrame(
            columns=["user_id", "organisation_id", "interaction_score"]
        )

    df = pd.DataFrame(records)

    # Keep strongest signal per user-organisation pair.
    df = (
        df
        .groupby(["user_id", "organisation_id"], as_index=False)["interaction_score"]
        .max()
    )

    return df


def build_interaction_dataframe_from_spreadsheet(
    user_id_offset=0,
    organisation_id_offset=0,
):
    """
    Build a DataFrame from the spreadsheet training data.
    """
    records = load_ratings_from_spreadsheet(
        user_id_offset=user_id_offset,
        organisation_id_offset=organisation_id_offset,
    )

    if not records:
        return pd.DataFrame(
            columns=["user_id", "organisation_id", "interaction_score"]
        )

    df = pd.DataFrame(records)

    df = (
        df
        .groupby(["user_id", "organisation_id"], as_index=False)["interaction_score"]
        .max()
    )

    return df[["user_id", "organisation_id", "interaction_score"]]


def filter_existing_users_and_organisations(matrix):
    """
    Remove user IDs or organisation IDs that do not exist in the database.

    This prevents foreign key errors when saving UserFactor and
    OrganisationFactor rows.
    """
    user_ids = [int(value) for value in matrix.index.tolist()]
    organisation_ids = [int(value) for value in matrix.columns.tolist()]

    existing_user_ids = {
        int(row[0])
        for row in db.session.query(User.user_id)
        .filter(User.user_id.in_(user_ids))
        .all()
    }

    existing_organisation_ids = {
        int(row[0])
        for row in db.session.query(Organisation.organisation_id)
        .filter(Organisation.organisation_id.in_(organisation_ids))
        .all()
    }

    if not existing_user_ids or not existing_organisation_ids:
        return matrix.iloc[0:0, 0:0]

    matrix = matrix.loc[
        [user_id for user_id in matrix.index if int(user_id) in existing_user_ids],
        [org_id for org_id in matrix.columns if int(org_id) in existing_organisation_ids],
    ]

    return matrix


# ----------------------------------------------------------------------
# SVD training and factor storage
# ----------------------------------------------------------------------

def train_svd_model(
    source="database",
    max_components=10,
    user_id_offset=0,
    organisation_id_offset=0,
):
    """
    Train SVD and store the learned vectors in the database.

    source options:
        "database"    -> train from real app data
        "spreadsheet" -> train from BACKEND/app/data spreadsheet

    user_id_offset and organisation_id_offset are only used for spreadsheet
    training. They help convert spreadsheet IDs into the real database IDs.

    Stores:
        UserFactor.factors
        OrganisationFactor.factors
    """
    if source == "spreadsheet":
        interactions_df = build_interaction_dataframe_from_spreadsheet(
            user_id_offset=user_id_offset,
            organisation_id_offset=organisation_id_offset,
        )
    else:
        interactions_df = build_interaction_dataframe_from_db()

    if interactions_df.empty:
        return {
            "message": "No interaction data found for training.",
            "trained": False,
            "source": source,
            "user_id_offset": int(user_id_offset),
            "organisation_id_offset": int(organisation_id_offset),
        }

    matrix = interactions_df.pivot_table(
        index="user_id",
        columns="organisation_id",
        values="interaction_score",
        fill_value=0,
    )

    # Remove IDs that do not exist in the real database.
    matrix = filter_existing_users_and_organisations(matrix)

    if matrix.empty:
        return {
            "message": (
                "The interaction matrix has no matching real users or organisations. "
                "Check your spreadsheet IDs or use user_id_offset if needed."
            ),
            "trained": False,
            "source": source,
        }

    number_of_users, number_of_orgs = matrix.shape
    n_components = min(max_components, number_of_users - 1, number_of_orgs - 1)

    if n_components < 1:
        return {
            "message": "Not enough users or organisations to train SVD.",
            "trained": False,
            "source": source,
            "users_in_matrix": int(number_of_users),
            "organisations_in_matrix": int(number_of_orgs),
        }

    model = TruncatedSVD(n_components=n_components, random_state=42)

    # user_features shape:
    #     number of users x number of components
    user_features = model.fit_transform(matrix)

    # organisation_features shape:
    #     number of organisations x number of components
    organisation_features = model.components_.T

    # Save user vectors.
    users_saved = 0

    for user_id, vector in zip(matrix.index, user_features):
        user_id = int(user_id)
        factor_values = [float(value) for value in vector.tolist()]

        user_factor = UserFactor.query.get(user_id)

        if user_factor:
            user_factor.factors = factor_values
        else:
            user_factor = UserFactor(
                user_id=user_id,
                factors=factor_values,
            )

        db.session.add(user_factor)
        users_saved += 1

    # Save organisation vectors.
    organisations_saved = 0

    for organisation_id, vector in zip(matrix.columns, organisation_features):
        organisation_id = int(organisation_id)
        factor_values = [float(value) for value in vector.tolist()]

        organisation_factor = OrganisationFactor.query.get(organisation_id)

        if organisation_factor:
            organisation_factor.factors = factor_values
        else:
            organisation_factor = OrganisationFactor(
                organisation_id=organisation_id,
                factors=factor_values,
            )

        db.session.add(organisation_factor)
        organisations_saved += 1

    db.session.commit()

    return {
        "message": "SVD model trained and factor vectors stored.",
        "trained": True,
        "source": source,
        "user_id_offset": int(user_id_offset),
        "organisation_id_offset": int(organisation_id_offset),
        "components": int(n_components),
        "users_in_matrix": int(number_of_users),
        "organisations_in_matrix": int(number_of_orgs),
        "non_zero_interactions": int((matrix > 0).sum().sum()),
        "users_saved": int(users_saved),
        "organisations_saved": int(organisations_saved),
        "explained_variance": float(model.explained_variance_ratio_.sum()),
    }


def train_svd_model_from_database(max_components=10):
    """
    Convenience wrapper for training from real database interactions.
    """
    return train_svd_model(
        source="database",
        max_components=max_components,
        user_id_offset=0,
    )


def train_svd_model_from_spreadsheet(
    max_components=10,
    user_id_offset=0,
    organisation_id_offset=0,
):
    """
    Convenience wrapper for training from the Excel spreadsheet.
    """
    return train_svd_model(
        source="spreadsheet",
        max_components=max_components,
        user_id_offset=user_id_offset,
        organisation_id_offset=organisation_id_offset,
    )


# ----------------------------------------------------------------------
# Recommendation helper scores
# ----------------------------------------------------------------------

def get_user_interacted_org_ids(user_id):
    """
    Return organisations the user already interacted with.

    These are excluded from recommendations.
    """
    interacted_ids = set()

    reviewed = RatingReview.query.filter_by(user_id=user_id).all()
    for review in reviewed:
        interacted_ids.add(review.organisation_id)

    saved = SavedOrganisation.query.filter_by(user_id=user_id).all()
    for saved in saved:
        interacted_ids.add(saved.organisation_id)

    logs = EngagementLog.query.filter_by(user_id=user_id).all()
    for log in logs:
        interacted_ids.add(log.organisation_id)

    return interacted_ids


def get_factor_scores(user_id):
    """
    Generate SVD scores using stored UserFactor and OrganisationFactor vectors.

    This is the main benefit of creating UserFactor and OrganisationFactor:
    recommendations can use stored trained vectors instead of retraining every
    time a user opens the page.
    """
    user_factor = UserFactor.query.get(user_id)

    if not user_factor:
        return {}

    user_vector = np.array(user_factor.factors, dtype=float)

    organisation_factors = OrganisationFactor.query.all()

    if not organisation_factors:
        return {}

    raw_scores = {}

    for organisation_factor in organisation_factors:
        organisation_id = organisation_factor.organisation_id
        organisation_vector = np.array(organisation_factor.factors, dtype=float)

        # Dot product measures how closely the user vector matches the
        # organisation vector.
        raw_score = float(np.dot(user_vector, organisation_vector))
        raw_scores[organisation_id] = raw_score

    if not raw_scores:
        return {}

    # Normalise raw dot-product scores to 0-1.
    min_score = min(raw_scores.values())
    max_score = max(raw_scores.values())

    if max_score == min_score:
        return {
            org_id: 0.5
            for org_id in raw_scores
        }

    return {
        org_id: (score - min_score) / (max_score - min_score)
        for org_id, score in raw_scores.items()
    }


def get_preference_scores(user_id):
    """
    Score organisations based on user selected category preferences.

    This helps new users, especially before they have enough interactions for
    SVD to work.
    """
    preferences = UserPreference.query.filter_by(user_id=user_id).all()
    category_ids = [preference.category_id for preference in preferences]

    if not category_ids:
        return {}

    scores = {}

    # organisation_categories is used as a linking table.
    statement = text("""
        SELECT organisation_id
        FROM organisation_categories
        WHERE category_id IN :category_ids
    """).bindparams(bindparam("category_ids", expanding=True))

    rows = db.session.execute(
        statement,
        {"category_ids": category_ids}
    ).fetchall()

    for row in rows:
        organisation_id = row[0]
        scores[organisation_id] = scores.get(organisation_id, 0) + 1

    # Also match organisations that store the category directly.
    organisations = Organisation.query.filter(
        Organisation.category_id.in_(category_ids)
    ).all()

    for organisation in organisations:
        scores[organisation.organisation_id] = scores.get(
            organisation.organisation_id,
            0
        ) + 1

    if not scores:
        return {}

    max_score = max(scores.values())

    return {
        organisation_id: score / max_score
        for organisation_id, score in scores.items()
    }


def get_popularity_scores():
    """
    Score organisations based on general popularity.

    Uses:
        average rating
        review count
        saved count
        engagement count

    These values are normalised and combined.
    """
    organisations = Organisation.query.all()

    if not organisations:
        return {}

    organisation_ids = [org.organisation_id for org in organisations]
    scores = {organisation_id: 0.0 for organisation_id in organisation_ids}

    rating_rows = (
        db.session.query(
            RatingReview.organisation_id,
            db.func.avg(RatingReview.rating),
            db.func.count(RatingReview.review_id),
        )
        .filter(RatingReview.is_hidden == False)  # noqa: E712
        .group_by(RatingReview.organisation_id)
        .all()
    )

    average_rating = {}
    review_count = {}

    for organisation_id, avg_rating, count_reviews in rating_rows:
        average_rating[organisation_id] = float(avg_rating or 0)
        review_count[organisation_id] = int(count_reviews or 0)

    save_rows = (
        db.session.query(
            SavedOrganisation.organisation_id,
            db.func.count(SavedOrganisation.saved_id),
        )
        .group_by(SavedOrganisation.organisation_id)
        .all()
    )

    save_count = {
        organisation_id: int(count_saves or 0)
        for organisation_id, count_saves in save_rows
    }

    engagement_rows = (
        db.session.query(
            EngagementLog.organisation_id,
            db.func.count(EngagementLog.engagement_id),
        )
        .group_by(EngagementLog.organisation_id)
        .all()
    )

    engagement_count = {
        organisation_id: int(count_engagements or 0)
        for organisation_id, count_engagements in engagement_rows
    }

    max_reviews = max(review_count.values(), default=1)
    max_saves = max(save_count.values(), default=1)
    max_engagements = max(engagement_count.values(), default=1)

    for organisation_id in organisation_ids:
        rating_score = average_rating.get(organisation_id, 0) / 5
        review_score = (
            review_count.get(organisation_id, 0) / max_reviews
            if max_reviews
            else 0
        )
        save_score = (
            save_count.get(organisation_id, 0) / max_saves
            if max_saves
            else 0
        )
        engagement_score = (
            engagement_count.get(organisation_id, 0) / max_engagements
            if max_engagements
            else 0
        )

        scores[organisation_id] = (
            0.50 * rating_score
            + 0.20 * review_score
            + 0.20 * save_score
            + 0.10 * engagement_score
        )

    return scores


# ----------------------------------------------------------------------
# Final recommendation output
# ----------------------------------------------------------------------

def organisation_to_dict(
    organisation,
    final_score,
    factor_score=0,
    preference_score=0,
    popularity_score=0,
):
    """
    Convert one Organisation model into a JSON response for Vue.
    """
    category_name = "General"
    parish = "Not provided"

    if organisation.category:
        category_name = organisation.category.category_name

    if organisation.location:
        parish = organisation.location.parish

    reasons = []

    if factor_score > 0:
        reasons.append("similar users interacted with this organisation")

    if preference_score > 0:
        reasons.append("matches your selected interests")

    if popularity_score > 0.30:
        reasons.append("is popular or highly engaged")

    if not reasons:
        reasons.append("is a general recommendation")

    return {
        "organisation_id": organisation.organisation_id,
        "organisation_name": organisation.organisation_name,
        "name": organisation.organisation_name,
        "organisation_type": organisation.organisation_type,
        "category": category_name,
        "location": parish,
        "email": organisation.email,
        "phone": organisation.phone,
        "website_url": organisation.website_url,
        "predicted_score": round(float(final_score), 4),
        "match_level": get_match_level(final_score),
        "score_parts": {
            "factor_score": round(float(factor_score), 4),
            "preference_score": round(float(preference_score), 4),
            "popularity_score": round(float(popularity_score), 4),
        },
        "explanation": "Recommended because it " + ", ".join(reasons) + ".",
    }


def get_recommendations(user_id, top_n=10):
    """
    Return hybrid recommendations for a user.

    If factor scores exist:
        50% factor score
        30% preference score
        20% popularity score

    If the user has no factor vector yet:
        70% preference score
        30% popularity score

    This means the system still works for users who have not been included in
    model training yet.
    """
    user = User.query.get(user_id)

    if not user:
        return {
            "message": f"User {user_id} not found.",
            "model_used": "none",
            "recommendations": [],
        }

    factor_scores = get_factor_scores(user_id)
    preference_scores = get_preference_scores(user_id)
    popularity_scores = get_popularity_scores()

    if factor_scores:
        weights = {
            "factor": 0.50,
            "preference": 0.30,
            "popularity": 0.20,
        }
        model_used = "stored_svd_factors_plus_preferences_and_popularity"
    else:
        weights = {
            "factor": 0.00,
            "preference": 0.70,
            "popularity": 0.30,
        }
        model_used = "preferences_and_popularity_fallback"

    candidate_ids = set()
    candidate_ids.update(factor_scores.keys())
    candidate_ids.update(preference_scores.keys())
    candidate_ids.update(popularity_scores.keys())

    already_interacted = get_user_interacted_org_ids(user_id)

    scored_items = []

    for organisation_id in candidate_ids:
        organisation = Organisation.query.get(organisation_id)

        if not organisation:
            continue

        # Do not recommend an organisation to its owner.
        if organisation.owner_user_id == user_id:
            continue

        # Do not recommend an organisation the user already interacted with.
        if organisation_id in already_interacted:
            continue

        factor_score = factor_scores.get(organisation_id, 0)
        preference_score = preference_scores.get(organisation_id, 0)
        popularity_score = popularity_scores.get(organisation_id, 0)

        final_score = (
            weights["factor"] * factor_score
            + weights["preference"] * preference_score
            + weights["popularity"] * popularity_score
        )

        scored_items.append({
            "organisation": organisation,
            "final_score": final_score,
            "factor_score": factor_score,
            "preference_score": preference_score,
            "popularity_score": popularity_score,
        })

    scored_items.sort(
        key=lambda item: item["final_score"],
        reverse=True,
    )

    recommendations = [
        organisation_to_dict(
            organisation=item["organisation"],
            final_score=item["final_score"],
            factor_score=item["factor_score"],
            preference_score=item["preference_score"],
            popularity_score=item["popularity_score"],
        )
        for item in scored_items[:top_n]
    ]

    return {
        "message": "Recommendations generated.",
        "model_used": model_used,
        "recommendations": recommendations,
    }


def get_recommendations_with_explanations(user_id, top_n=10):
    """
    Compatibility wrapper for existing route code.
    """
    return get_recommendations(user_id, top_n)


# ----------------------------------------------------------------------
# Standalone helper for Jupyter/notebook demonstration
# ----------------------------------------------------------------------

def recommend_with_svd(ratings, selected_user_id, top_n=5):
    """
    Simple notebook-style SVD recommender.

    This function does not use Flask, SQLAlchemy, or the database.
    It is useful for explaining the ML idea in a Jupyter Notebook.

    ratings example:
        [
            {"user_id": 1, "organisation_id": 1000, "rating": 5},
            {"user_id": 1, "organisation_id": 1002, "rating": 3},
            {"user_id": 2, "organisation_id": 1000, "rating": 4},
        ]
    """
    if not ratings:
        return {
            "message": "No ratings found.",
            "recommendations": [],
        }

    ratings_df = pd.DataFrame(ratings)

    matrix = ratings_df.pivot_table(
        index="user_id",
        columns="organisation_id",
        values="rating",
        fill_value=0,
    )

    if selected_user_id not in matrix.index:
        return {
            "message": "This user has no rating history.",
            "recommendations": [],
        }

    number_of_users, number_of_orgs = matrix.shape
    n_components = min(2, number_of_users - 1, number_of_orgs - 1)

    if n_components < 1:
        return {
            "message": "Not enough data to train SVD.",
            "recommendations": [],
        }

    model = TruncatedSVD(n_components=n_components, random_state=42)
    user_features = model.fit_transform(matrix)
    organisation_features = model.components_

    predicted_values = user_features @ organisation_features

    predicted_matrix = pd.DataFrame(
        predicted_values,
        index=matrix.index,
        columns=matrix.columns,
    )

    user_predictions = predicted_matrix.loc[selected_user_id]
    already_rated = matrix.loc[selected_user_id]
    already_rated = already_rated[already_rated > 0].index

    user_predictions = user_predictions.drop(already_rated)
    top_predictions = user_predictions.sort_values(ascending=False).head(top_n)

    return {
        "message": "Recommendations generated successfully.",
        "recommendations": [
            {
                "organisation_id": int(organisation_id),
                "predicted_score": float(score),
            }
            for organisation_id, score in top_predictions.items()
        ],
    }
