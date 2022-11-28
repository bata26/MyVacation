from controllers.accomodationsManager import AccomodationsManager
from flask import Flask, abort, request, jsonify, Response
from dotenv import load_dotenv
from markupsafe import escape
from controllers.activityManager import ActivityManager
from controllers.reviewManager import ReviewManager
from controllers.userManager import UserManager
from controllers.adminManager import AdminManager
from flask_cors import CORS
import json
from functools import wraps
import re
import bcrypt


load_dotenv()
application = Flask(__name__)
CORS(application)

def validateObjecID(userID):
    validationRegex = "^[0-9a-fA-F]{24}$"
    if re.match(validationRegex , userID):
        return True
    return False

def required_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return Response(json.dumps(f"Authorization token not found"), 401)
        
        if(not(validateObjecID(request.headers.get('Authorization')))):
            return Response(json.dumps("userID non valido"), 403)

        return f(*args, **kwargs)

    return decorator


@application.route("/test" , methods = ["GET"])
#@required_token
def testValidation():
    return "OK" , 200

@application.route('/activities/<activity_id>' , methods = ['DELETE'])
#@required_token
def deleteActivityByID(activity_id):
    activityID = escape(activity_id)
    user = {
        "type" : "admin"
    }
    result = ActivityManager.deleteActivity(activityID , user)
    return "" , 200

@application.route('/activities/<activity_id>' , methods = ['GET'])
#@required_token
def getActivityByID(activity_id):
    activityID = escape(activity_id)
    result = ActivityManager.getActivityFromID(activityID)
    return result , 200

@application.route('/activities' , methods = ['GET'])
#@required_token
def getActivities():
    args = request.args
    city = args.get("city")
    guests = args.get("guests")
    start_date = args.get("start_date")
    end_date = args.get("end_date")
    result = ActivityManager.getFilteredActivity(start_date  , end_date  , city , guests)
    return result , 200

@application.route('/accomodations/<accomodation_id>' , methods = ['DELETE'])
#@required_token
def deleteAccomodationById(accomodation_id):
    accomodationId = escape(accomodation_id)
    user = {
        "type" : "admin"
    }
    result = AccomodationsManager.deleteAccomodation(accomodationId , user)
    return "" , 200

@application.route('/accomodations/<accomodation_id>' , methods = ['GET'])
#@required_token
def getAccomodationById (accomodation_id):
    accomodationId = escape(accomodation_id)
    result = AccomodationsManager.getAccomodationsFromId(accomodationId)
    return result , 200

@application.route('/accomodations' , methods = ['GET'])
#@required_token
def getAccomodations():
    args = request.args
    city = args.get("city")
    guests = args.get("guests")
    start_date = args.get("start_date")
    end_date = args.get("end_date")
    result = AccomodationsManager.getFilteredAccomodation(start_date  , end_date  , city , guests)
    return result , 200

@application.route('/insert/accomodation' , methods = ['POST'])
#@required_token
def insertAccomodation():
    accomodation = request.data
    print(f"req : {request}")
    print(f"req : {request.data}")
    print(f"form : {dict(request.form)}")
    print(f"file : {dict(request.files)}")
    
    return "" , 200

@application.route('/reviews/<review_id>' , methods = ['GET'])
#@required_token
def getReviewByID(review_id):
    reviewID = escape(review_id)
    result = ReviewManager.getReviewFromID(reviewID)
    return result , 200
    

@application.route('/reviews/<review_id>' , methods = ['DELETE'])
#@required_token
def deleteReviewByID(reviewID):
    reviewID = escape(reviewID)
    user = {
        "type" : "admin"
    }
    result = ReviewManager.deleteReview(reviewID , user)
    return "" , 200

@application.route('/users/<user_id>' , methods = ['DELETE'])
#@required_token
def deleteUserById (user_id):
    userId = escape(user_id)
    user = {
        "type" : "admin"
    }
    result = UserManager.deleteUser(userId , user)
    return "" , 200

@application.route('/users/<user_id>' , methods = ['GET'])
#@required_token
def getUserById (user_id):
    userId = escape(user_id)
    result = UserManager.getUserFromId(userId)
    return result , 200

@application.route('/login' , methods = ['POST'])
#@required_token
def loginUser ():
    #print(request.)
    username = request.json["username"]
    password = request.json["password"]
    print(f"username : {username}")
    print(f"password : {password}")
    try:
        userID = UserManager.authenicateUser(username , password)
        return userID , 200
    except Exception as e:
        return str(e) , 500

@application.route('/users' , methods = ['GET'])
#@required_token
def getUsers():
    args = request.args
    name = args.get("name")
    surname = args.get("surname")
    print(f"name : {name}")
    print(f"surname : {surname}")
    user = {
            "type" : "admin"
        }
    result = UserManager.getFilteredUsers(user , name , surname)
    return result , 200


@application.route('/admin/announcements' , methods = ['GET'])
#@required_token
def getAnnouncementToBeApproved():
    try:
        result = AdminManager.getAnnouncementToApprove()
        return result , 200
    except Exception as e:
        return e , 500

@application.route('/admin/announcements/<announcementID>' , methods = ['POST'])
#@required_token
def approveAnnouncement(announcementID):
    if(not(validateObjecID(announcementID))): return "Announcement non valido" , 500
    try:
        AdminManager.approveAnnouncement(announcementID)
        return "" , 200
    except Exception as e:
        return e , 500

if __name__ == "__main__":
    application.run(threaded=True , debug=True , use_reloader=False)