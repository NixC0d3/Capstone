def fallback_recommendations(organisations, top_n=5):
    # Simple fallback used when a user has little or no rating history.
    return organisations[:top_n]

def recommend_with_svd(ratings, selected_user_id, top_n=5):
    """
    Machine-learning recommendation service.

    Expected ratings format:
    [
        {"user_id": 1, "organisation_id": 2, "rating": 5},
        {"user_id": 1, "organisation_id": 3, "rating": 4},
        ...
    ]

    This function uses pandas and scikit-learn if installed.
    If they are not installed yet, it returns an explanation instead of crashing.
    """

    try:
        import pandas as pd
        from sklearn.decomposition import TruncatedSVD
    except ImportError:
        return {
            "message": "Install pandas and scikit-learn to enable TruncatedSVD recommendations.",
            "recommendations": []
        }

    if not ratings:
        return {
            "message": "No ratings found. Use fallback recommendations.",
            "recommendations": []
        }

    ratings_df = pd.DataFrame(ratings)

    user_org_matrix = ratings_df.pivot_table(
        index="user_id",
        columns="organisation_id",
        values="rating",
        fill_value=0
    )

    if selected_user_id not in user_org_matrix.index:
        return {
            "message": "This user has no rating history. Use fallback recommendations.",
            "recommendations": []
        }

    number_of_users, number_of_orgs = user_org_matrix.shape
    n_components = min(2, number_of_users - 1, number_of_orgs - 1)

    if n_components < 1:
        return {
            "message": "Not enough ratings to train recommendation model.",
            "recommendations": []
        }

    model = TruncatedSVD(n_components=n_components, random_state=42)
    user_features = model.fit_transform(user_org_matrix)
    organisation_features = model.components_

    predicted_values = user_features @ organisation_features
    predicted_matrix = pd.DataFrame(
        predicted_values,
        index=user_org_matrix.index,
        columns=user_org_matrix.columns
    )

    user_predictions = predicted_matrix.loc[selected_user_id]
    already_rated = user_org_matrix.loc[selected_user_id]
    already_rated = already_rated[already_rated > 0].index

    user_predictions = user_predictions.drop(already_rated)
    top_predictions = user_predictions.sort_values(ascending=False).head(top_n)

    return {
        "message": "Recommendations generated successfully.",
        "recommendations": [
            {
                "organisation_id": int(org_id),
                "predicted_score": float(score)
            }
            for org_id, score in top_predictions.items()
        ]
    }
