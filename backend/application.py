from controllers.accomodationsManager import AccomodationsManager
from flask import Flask, abort, request, jsonify, Response
from dotenv import load_dotenv
from markupsafe import escape
from controllers.activityManager import ActivityManager

load_dotenv()
application = Flask(__name__)

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
    return result , 200

@application.route('/accomodations/<accomodation_id>' , methods = ['DELETE'])
def deleteAccomodationById (accomodation_id):
    accomodationId = escape(accomodation_id)
    user = {
        "type" : "admin"
    }
    result = AccomodationsManager.deleteAccomodation(accomodationId , user)
    print(f"delete result : {result}")
    return "" , 200

@application.route('/accomodations/<accomodation_id>' , methods = ['GET'])
def getAccomodationById (accomodation_id):
    accomodationId = escape(accomodation_id)
    result = AccomodationsManager.getAccomodationsFromId(accomodationId)
    return result , 200

@application.route('/accomodations' , methods = ['GET'])
def getAccomodations():
    args = request.args
    city = args.get("city")
    guests = args.get("guests")
    start_date = args.get("start_date")
    end_date = args.get("end_date")
    result = AccomodationsManager.getFilteredAccomodation(start_date  , end_date  , city , guests)
    return result , 200
    
if __name__ == "__main__":
    application.run(threaded=True , debug=True , use_reloader=False)