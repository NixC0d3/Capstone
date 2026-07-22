from flask import Blueprint, jsonify, request
from app.models import RatingReview
from app.services.recommendation_service import recommend_with_svd

#-------------------------------------------------------------------------------------------------------------------------------------------
#########################ADDED MORE LIBRARIES AND IMPORTS#############################
#-------------------------------------------------------------------------------------------------------------------------------------------

from app.services.recommendation_service import (
    get_recommendations,
    get_recommendations_with_explanations,
    train_svd_model_from_spreadsheet,
    load_ratings_from_spreadsheet,
    recommend_with_svd,          
    fallback_recommendations    
)
from app.models import Organisation, UserFactor, RatingReview
from app.extensions import db
import pandas as pd

#-------------------------------------------------------------------------------------------------------------------------------------------
######################### RECOMMENDATION MODEL ENDPOINT #############################
#-------------------------------------------------------------------------------------------------------------------------------------------

@recommendation_bp.route('/train', methods=['POST'])
def train_model():

    #Trains the model using results from the training data spreadsheet

    try:
        # Call the training function from the recommendation service
        # This function loads the spreadsheet, builds the matrix, applies SVD, and stores factors
        result = train_svd_model_from_spreadsheet()
        
        # Return the result as JSON with 200 OK status
        return jsonify(result), 200
    except Exception as e:

        #error handing if training model fails
        
        return jsonify({"message": f"Training failed: {str(e)}"}), 500

#-------------------------------------------------------------------------------------------------------------------------------------------
######################### RECOMMENDATION MODEL ENDPOINT #############################
#-------------------------------------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------------------------------------------------
######################### USER RECOMMENDATIONS ENDPOINT #############################
#-------------------------------------------------------------------------------------------------------------------------------------------

@recommendation_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_recommendations(user_id):

    #Gets a user's recommendations

    # top_n: Number of recommendations to return (default: 10)
    top_n = request.args.get('top_n', 10, type=int)
    
    # include_explanations is if we plan to include explanations with the recommendations, like explaining to the general user to some level 
    # why its being recommended to them

    include_explanations = request.args.get('include_explanations', 'false').lower() == 'true'
    
    try:
        # Check if explanations are requested
        if include_explanations:
            # Calls the function that returns recommendations with explanations
            result = get_recommendations_with_explanations(user_id, top_n)
        else:
            # Calls the basic recommendation function which returns the small business IDs and predicted scores
            result = get_recommendations(user_id, top_n)
        
        # Return the result as JSON with 200 OK status
        return jsonify(result), 200
    except Exception as e:
        # error handling
        return jsonify({
            "message": f"Error generating recommendations: {str(e)}",
            "recommendations": []
        }), 500

#-------------------------------------------------------------------------------------------------------------------------------------------
######################### USER RECOMMENDATIONS ENDPOINT #############################
#-------------------------------------------------------------------------------------------------------------------------------------------

@recommendation_bp.route('/status', methods=['GET'])
def get_model_status():

    #checks to see if the model is ready before making recommendation requests
    #could also be used to show the status on the admin dashboard

    # UserFactor records are created when training the model
    user_factor_count = UserFactor.query.count()
    
    # Counts how many small business factor records exist (also created during training)

    item_factor_count = UserFactor.query.count()  # Should match small business factor count
    
    # Determine if the model has been trained (at least one user factor needs to exists)
    model_trained = user_factor_count > 0
    
    # Return the status as JSON
    return jsonify({
        "model_trained": model_trained,
        "users_with_factors": user_factor_count,
        "items_with_factors": item_factor_count,

        "message": "Model is ready." if model_trained else "Model not trained yet. Please run /api/recommendations/train first."
    }), 200

#-------------------------------------------------------------------------------------------------------------------------------------------
######################### USER RECOMMENDATIONS ENDPOINT #############################
#-------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------
######################### GET RECOMMENDATIONS (RANKED) ENDPOINT #############################
#-------------------------------------------------------------------------------------------------------------------------------------------

@recommendation_bp.route('/user/<int:user_id>/ranked', methods=['GET'])
def get_user_recommendations_ranked(user_id):

    #Gets recommendations based on that user's ranking and match percentages

    top_n = request.args.get('top_n', 10, type=int)
    
    try:
        # Imports the ranking function from the service
        from app.services.recommendation_service import get_recommendations_ranked
        
        # Gets the ranked recommendations
        result = get_recommendations_ranked(user_id, top_n)
        
        # Return the result as JSON
        return jsonify(result), 200
    except Exception as e:
        # Handle any errors that occur
        return jsonify({
            "message": f"Error generating ranked recommendations: {str(e)}",
            "recommendations": []
        }), 500

#-------------------------------------------------------------------------------------------------------------------------------------------
######################### GET RECOMMENDATIONS (RANKED) ENDPOINT #############################
#-------------------------------------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------------------------------------------------
######################### GET RECOMMENDATIONS (POPULAR) ENDPOINT #############################
#-------------------------------------------------------------------------------------------------------------------------------------------

@recommendation_bp.route('/user/<int:user_id>/trending', methods=['GET'])
def get_trending_recommendations(user_id):

    ## Get recommendations based on popularity
    ## Mainly for first time users

    top_n = request.args.get('top_n', 10, type=int)
    
    try:
        from app.services.recommendation_service import get_trending_recommendations
        
        result = get_trending_recommendations(user_id, top_n)
        
        return jsonify(result), 200
    except Exception as e:
        # Handle any errors
        return jsonify({
            "message": f"Error generating trending recommendations: {str(e)}",
            "recommendations": []
        }), 500

#-------------------------------------------------------------------------------------------------------------------------------------------
######################### GET RECOMMENDATIONS (POPULAR) ENDPOINT #############################
#-------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------
######################### WAS HERE BEFORE #############################
#-------------------------------------------------------------------------------------------------------------------------------------------

@recommendation_bp.route("/<int:user_id>", methods=["GET"])
def get_recommendations(user_id):
    top_n = int(request.args.get("top_n", 5))

    ratings = [
        {
            "user_id": review.user_id,
            "organisation_id": review.organisation_id,
            "rating": review.rating
        }
        for review in RatingReview.query.filter_by(is_hidden=False).all()
    ]

    result = recommend_with_svd(ratings, selected_user_id=user_id, top_n=top_n)
    return jsonify(result)
