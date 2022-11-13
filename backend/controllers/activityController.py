from controllers.activityManager import ActivityManager
#from flask import Flask, abort, request, jsonify, Response
#from flask_cors import CORS, cross_origin
#from dotenv import load_dotenv
#import os
#import datetime
#from datetime import timedelta , datetime
#import logging
#from markupsafe import escape

@application.route('/activities/<activity_id>' , methods = ['DELETE'])
def deleteActivityByID(activity_id):
    activityID = escape(activity_id)
    user = {
        "type" : "admin"
    }
    result = ActivityManager.deleteAccomodation(activityID , user)
    print(f"delete result : {result}")
    return "" , 200

@application.route('/activities/<activity_id>' , methods = ['GET'])
def getActivityByID(activity_id):
    activityID = escape(activity_id)
    result = ActivityManager.getActivityFromID(activityID)
    return result , 200

@application.route('/activities' , methods = ['GET'])
def getActivities():
    args = request.args
    city = args.get("city")
    guests = args.get("guests")
    start_date = args.get("start_date")
    end_date = args.get("end_date")
    result = ActivityManager.getFilteredActivity(start_date  , end_date  , city , guests)
    print(f"result : {result}")
    result["_id"] = str(result["_id"])
    return result , 200