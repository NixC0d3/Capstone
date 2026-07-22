#-------------------------------------------------------------------------------------
#################ADDED LIBRARIES HERE#################
#-------------------------------------------------------------------------------------
import pandas as pd  ##data manipulation + excel
import numpy as np   ## dot product calculations
from sklearn.decomposition import TruncatedSVD  #needed for rec algo as it decomposes matrix
from app.models import RatingReview, UserFactor, OrganisationFactor, User, Organisation #imported these database models based on what I think each field does in model.py
from app.extensions import db #database connection??
import os
#-------------------------------------------------------------------------------------
#################ENDS HERE#############################################
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
################TRAINING DATA SPREADSHEET HERE########################
#-------------------------------------------------------------------------------------

# Path to training data spreadsheet
DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #gets project root dir

#I used the training data as a spreadsheet but it may be better to add it to the database
#Not fully sure how that works so I just left it as a spreadsheet
TRAINING_DATA_PATH = os.path.join(DATA_DIR, 'Training Data - Recommendations.xlsx') 

#-------------------------------------------------------------------------------------
################# WEIGHTS FOR THE BASED ON THE TRAINING DATA #############################################
#-------------------------------------------------------------------------------------

def get_interaction_weight(row):

    #-----------------------------------------------------------------------------------------------------------------------------------
    # Interaction weight is also in the info section of the spreadsheet
    # 1 = view only (weight 1.0)
    # 2 = view + (rate, review or save) (3.0)
    # 3 = view + (2 of 3) (5.0)
    # 4 = view + (all 3)
    # I know sir said to give ppl the option to change their weight but this has to wor
    #-----------------------------------------------------------------------------------------------------------------------------------
    
    # Check the cells that aren't 0
    # I should have 0 in each row but just in case
    has_rate = row.get('rating', 0) > 0
    has_review = row.get('review', 0) > 0
    has_save = row.get('save', 0) > 0
    has_view = row.get('view', 0) > 0  

    # This counts how many of the three actions (rate, review, save) were performed
    action_count = sum([has_rate, has_review, has_save])
    
    # Determine weight based on level
    if not has_view:
        return 0.0
    elif action_count == 0: #user viewed page
        return 1.0
    elif action_count == 1: # user viewed page + another action
        return 3.0
    elif action_count == 2: # user viewed page + 2 actions
        return 5.0
    elif action_count == 3: # all actions performed
        return 7.0
    else:
        return 1.0

####This is probably better considering the number is on the spreadsheet
#### But above is how I see it would be done from the actual application

def get_weight_from_pattern(pattern):
    #where pattern is the matrix from the spreadsheet
    if pattern >= 4:
        return 7.0  # View + All Three Actions
    elif pattern == 3:
        return 5.0  # View + Two Actions
    elif pattern == 2:
        return 3.0  # View + One Action
    elif pattern == 1:
        return 1.0  # View Only
    else:
        return 1.0  # Default fallback

#-----------------------------------------------------------------------------------------------------------------------------------
########## LOADS RATINGS FROM THE TRAINING DATA #############################
#-----------------------------------------------------------------------------------------------------------------------------------

#Implements step 1 of the pseudocode

def load_ratings_from_spreadsheet():

    try:

        # read the matrix from the spreadsheet
        # header=0/column are the small business IDs and index_col=0/rows are the training user IDs.
        df = pd.read_excel(TRAINING_DATA_PATH, sheet_name='Matrix', header=0, index_col=0)

    except Exception as e:

        #error checking that returns an empty list.
        print(f"Error reading training spreadsheet: {e}")
        return []
    
    # stores rating records
    ratings = []
    
    # Iterate over each user ID in the df.index (1, 2, 3....)
    for user_id in df.index:
        # Iterate over each small business number, df.columns, for this user.
        for org_id in df.columns:
            # Get the value at the intersection of user and small business.
            # This is the interaction pattern (1, 2, 3, or 4) or 0 (user has never interacted with the application)
            rating_val = df.loc[user_id, org_id]
            
            # Only process values > 0

            if rating_val > 0:
                # Genuinely just assuming that the seed.py's offset for general users is 30000 as a placeholder
                # Maps the training data to actual users in the database.
                actual_user_id = int(user_id) + 30000
                
                actual_org_id = int(org_id)
                
                # pattern is from the function --> get_weight_from_pattern(pattern)
                pattern = int(rating_val)
                
                # Does it again could just call back the get_weight_from_pattern(pattern) function instead
                if pattern >= 4:
                    weight = 7.0   # View + All Three Actions
                elif pattern == 3:
                    weight = 5.0   # View + Two Actions
                elif pattern == 2:
                    weight = 3.0   # View + One Action
                elif pattern == 1:
                    weight = 1.0   # View Only
                else:
                    weight = 1.0   
                
                # Appends the rating record as a dictionary.
                ratings.append({
                    "user_id": actual_user_id,
                    "organisation_id": actual_org_id,
                    "rating": weight,  # Use the hierarchical weight as the "rating"
                    "interaction_pattern": pattern,  # Store the original pattern for reference
                    "weight": weight
                })
    
    # Returns the list of all rating records with weights.
    return ratings

#-----------------------------------------------------------------------------------------------------------------------------------------
################# LOADS RATINGS FROM THE TRAINING DATA USING PATTERNS #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

def load_ratings_with_patterns():
    try:
        df = pd.read_excel(TRAINING_DATA_PATH, sheet_name='Matrix', header=0, index_col=0)
    except Exception as e:
        print(f"Error reading training spreadsheet: {e}")
        return pd.DataFrame()
    
    # Creates a list detailing the pattern info
    records = []
    for user_id in df.index:
        for org_id in df.columns:
            val = df.loc[user_id, org_id]
            if val > 0:
                records.append({
                    'user_id': int(user_id) + 30000,  # maps to user_id
                    'organisation_id': int(org_id),    # small business id #
                    'pattern': int(val),               # Original pattern (1-4) with 0 showing no interaction
                    'weight': get_weight_from_pattern(int(val))  
                })
    
    return pd.DataFrame(records)

#-----------------------------------------------------------------------------------------------------------------------------------------
################# LOADS RATINGS FROM THE TRAINING DATA USING PATTERNS #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------
################# FALLBACK #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

def fallback_recommendations(organisations, top_n=5):
    # Returns the first N small businesses but it would be better for it to return the most popular small businesses but that would need another
    # functionality the more I think about it
    # But for this it could also be the case of just using the training data to recommend them small businesses
    return organisations[:top_n]

#-----------------------------------------------------------------------------------------------------------------------------------------
################# FALLBACK #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

def train_svd_model_from_spreadsheet(n_components=20):

    #Steps 1-4 from the pseudocode

    # Step 1: Retrieve all ratings from the spreadsheet with weights.
    ratings = load_ratings_from_spreadsheet()
    
    if not ratings:
        return {"message": "No ratings found in spreadsheet. Check the file path."}
    
    # Converts the list of rating dictionaries to a pandas DataFrame.
    df = pd.DataFrame(ratings)
    
    # Step 2: Convert the ratings data into a matrix.
    # This is mainly if we're interwebbing the training and testing data

    matrix = df.pivot_table(
        index='user_id', 
        columns='organisation_id', 
        values='weight',  
        fill_value=0
    )
    
    # Determine the number of components for SVD.
    # We can't have more components than (users - 1) or (small businesses - 1).
    n_comp = min(n_components, matrix.shape[0] - 1, matrix.shape[1] - 1)
    
    # If we can't extract at least one component, there's not enough data.
    if n_comp < 1:
        return {"message": "Not enough data to train SVD."}
    
    # Step 4: Apply matrix factorisation using TruncatedSVD.
    model = TruncatedSVD(n_components=n_comp, random_state=42)
    
    # shape of user_features: (general users, n_components)
    user_features = model.fit_transform(matrix)
    
    # Transpose to get shape: (small businesses, n_components)
    item_features = model.components_.T
    
    # Store user factors in the database.
    user_count = 0
    for user_id, vec in zip(matrix.index, user_features):
        # Check if user factors already exist in the database.
        uf = UserFactor.query.get(user_id)
        if uf:
            # Update existing factors.
            uf.factors = vec.tolist()
        else:
            # Create new user factors.
            uf = UserFactor(user_id=user_id, factors=vec.tolist())
        # Stage the factor for saving.
        db.session.add(uf)
        user_count += 1
    
    # Store item factors in the database.
    item_count = 0
    for org_id, vec in zip(matrix.columns, item_features):
        # Check if organisation factors already exist.
        of = OrganisationFactor.query.get(org_id)
        if of:
            # Update existing factors.
            of.factors = vec.tolist()
        else:
            # Create new organisation factors.
            of = OrganisationFactor(organisation_id=org_id, factors=vec.tolist())
        # Stage the factor for saving.
        db.session.add(of)
        item_count += 1
    
    # Commit all staged to the database.
    db.session.commit()
    
    # Return success message
    return {
        "message": "SVD model trained with hierarchical interaction weights and factors stored.",
        "components": n_comp,
        "users_trained": user_count,
        "items_trained": item_count,
        "explained_variance": float(model.explained_variance_ratio_.sum())
    }

#-----------------------------------------------------------------------------------------------------------------------------------------
################# GET USER RATINGS FROM THE DATABASE #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

#Step 7 of the pseudocode

def get_user_ratings_from_db(user_id):

    # Queries the database for all organisations this user has rated.

    rated = RatingReview.query.filter_by(user_id=user_id).with_entities(RatingReview.organisation_id).all()

    return {r.organisation_id for r in rated}

#-----------------------------------------------------------------------------------------------------------------------------------------
################# GET RECOMMENDATIONS #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------

def get_recommendations(user_id, top_n=10):

    #How I see steps 6-9 beimg implemented

    #same error checking as before
    user = User.query.get(user_id)
    if not user:
        return {
            "message": f"User {user_id} not found in the database.",
            "recommendations": []
        }
    
    user_factor = UserFactor.query.get(user_id)
    if not user_factor:
        return {
            "message": "Recommendation model not trained yet. Please run /api/recommendations/train first.",
            "recommendations": []
        }
    
    # Step 6: Select predictions for the current user.
    user_vec = np.array(user_factor.factors)
    
    # Fetch all small business factors from the database (we got the small business factors from the training done with SVD)

    item_factors = OrganisationFactor.query.all()
    if not item_factors:
        return {
            "message": "No organisation factors found. Please train the model.",
            "recommendations": []
        }
    
    # Step 5: Predict missing ratings.
    # For each small business, compute the dot product of small business and user to get the predicated engagement score
    # the higher the dot product the higher the predicted match
    scores = {}
    for of in item_factors:
        org_id = of.organisation_id
        item_vec = np.array(of.factors)
        score = np.dot(user_vec, item_vec)  
        scores[org_id] = score
    
    # Step 7: Remove small businesses already rated.
    rated = get_user_ratings_from_db(user_id)
    for org_id in list(scores.keys()):
        if org_id in rated:
            del scores[org_id]
    
    # Step 8: Rank recommendations.
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Step 9: Return top recommendations.
    recommendations = []
    for org_id, score in sorted_scores[:top_n]:
        org = Organisation.query.get(org_id)
        if org:
            recommendations.append({
                "organisation_id": org_id,
                "name": org.organisation_name,

                "category": org.category.category_name if org.category else "General",

                "location": org.location.parish if org.location else "Jamaica",
                "predicted_score": float(score),
                # Calculate average rating from all user reviews so as to know whats most popular.
                # Could similarly be used for fallback.
                "rating": db.session.query(db.func.avg(RatingReview.rating)).filter(
                    RatingReview.organisation_id == org_id
                ).scalar() or 0,

                # Determine the match level of the user to the small businesses.
                "match_level": get_match_level(score)
            })
        else:
            # Small business may not exist in database 
            # Probably it would be better to just have it not appear tho
            recommendations.append({
                "organisation_id": org_id,
                "name": f"Organisation {org_id}",
                "category": "Unknown",
                "location": "Jamaica",
                "predicted_score": float(score),
                "rating": 0,
                "match_level": "Uncategorised"
            })
    
    # Return the final recommendations.
    return {
        "message": "Recommendations generated.",
        "recommendations": recommendations
    }


def get_match_level(score):
    #converts matching scores for the general user to better understand

    # Normalise score to 0-4 range (hierarchical pattern scale)
    normalised = normalise_score(score)
    
    # Map normalised score to match level description
    if normalised >= 3.0:
        return "Excellent (View + Rate + Review + Save)"
    elif normalised >= 2.0:
        return "Good (View + Two Actions)"
    elif normalised >= 1.5:
        return "Moderate (View + One Action)"
    elif normalised >= 1.0:
        return "Basic (View Only)"
    else:
        return "Potential Match"


def normalise_score(score):

    #Normlaises the raw dot product thats on the 0-4 scale
    normalised = (score + 5) * 0.2
    return min(4.0, max(0.0, normalised))

#-----------------------------------------------------------------------------------------------------------------------------------------
################# GET RECOMMENDATIONS #############################################
#-------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------

############################BELOW WAS THERE BEFORE###########################3

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
