from controllers.reviewManager import ReviewManager
#from flask import Flask, abort, request, jsonify, Response
#from flask_cors import CORS, cross_origin
#from dotenv import load_dotenv
#import os
#import datetime
#from datetime import timedelta , datetime
#import logging
#from markupsafe import escape

@application.route('/reviews/<review_id>' , methods = ['GET'])
def getReviewByID(review_id):
    reviewID = escape(review_id)
    result = ReviewManager.getReviewFromID(reviewID)
    return result , 200
    

@application.route('/reviews/<review_id>' , methods = ['DELETE'])
def deleteReviewByID(reviewID):
    reviewID = escape(reviewID)
    user = {
        "type" : "admin"
    }
    result = ReviewManager.deleteReview(reviewID , user)
    print(f"delete result : {result}")
    return "" , 200