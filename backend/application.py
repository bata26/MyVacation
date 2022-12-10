from controllers.accomodationsManager import AccomodationsManager
from flask import Flask, abort, request, jsonify, Response
from dotenv import load_dotenv
from markupsafe import escape
from controllers.activityManager import ActivityManager
from controllers.reviewManager import ReviewManager
from controllers.userManager import UserManager
from controllers.adminManager import AdminManager
from controllers.reservationManager import ReservationManager
from flask_cors import CORS, cross_origin
import json
from functools import wraps
import re
import bcrypt
from models.review import Review
import json

user = {
    "_id" : "637ce1a04ed62608566c5fae"
}

load_dotenv()
application = Flask(__name__)
cors = CORS(application , supports_credentials=True, origins=["*" , "http://127.0.0.1:3000"])

def validateObjecID(userObj):
    parsedUserObj = json.loads(userObj)
    print(parsedUserObj)
    userID = parsedUserObj["userID"]
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
@required_token
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
@required_token
def deleteAccomodationById(accomodation_id):
    accomodationId = escape(accomodation_id)
    user = {
        "type" : "admin"
    }
    result = AccomodationsManager.deleteAccomodation(accomodationId , user)
    return "" , 200

@application.route('/accomodations/<accomodation_id>' , methods = ['GET'])
@required_token
def getAccomodationById (accomodation_id):
    accomodationId = escape(accomodation_id)
    result = AccomodationsManager.getAccomodationsFromId(accomodationId)
    print(f"res : {result['_id']}")
    return result , 200

@application.route('/book/accomodation' , methods = ['POST'])
#@required_token
def bookAccomodation ():
    global user
    requestBody = request.json
    accomodation= requestBody["accomodation"]
    startDate = requestBody["startDate"]
    endDate = requestBody["endDate"]
    print(f"accomodation : {accomodation}")
    print(f"startDate : {startDate}")
    print(f"endDate : {endDate}")
    result = ReservationManager.book(accomodation , startDate ,user, "accomodation", endDate)
    return "OK" , 200

@application.route('/book/activity' , methods = ['POST'])
#@required_token
def bookActivity():
    global user
    requestBody = request.json
    activity= requestBody["activity"]
    startDate = requestBody["startDate"]
    print(f"activity : {activity}")
    print(f"startDate : {startDate}")
    result = ReservationManager.book(activity , startDate , user , "activity")
    return "OK" , 200

@application.route('/reservations' , methods = ['GET'])
#@required_token
def getReservationsByUserID():
    global user
    result = ReservationManager.getReservationsByUser(user["_id"])
    return "OK" , 200

@application.route('/reservations/<reservation_id>' , methods = ['DELETE'])
#@required_token
def deleteReservation(reservation_id):
    reservationID = escape(reservation_id)
    global user
    result = ReservationManager.deleteReservationByID()
    return "OK" , 200


@application.route('/accomodations' , methods = ['GET'])
#@required_token
def getAccomodations():
    args = request.args
    city = args.get("city")
    guests = args.get("guestsNumber")
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

@application.route('/reviews' , methods = ['PUT'])
#@required_token
def insertReview():
    global user
    requestBody = request.json
    review = Review(requestBody["userID"],
                    requestBody["destinationID"],
                    requestBody["score"],
                    requestBody["description"])          
    try:
        ReviewManager.insertNewReview(review)
        return "" , 200    
    except Exception as e:
        return str(e) , 200

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


@application.route('/review/check/<destination_id>' , methods = ['GET'])
#@required_token
def getIfCanReview (destination_id):
    destinationID = escape(destination_id)
    print(destinationID)
    global user
    result = {"result" : False}
    if ReviewManager.checkIfCanReview(str(destinationID) , user):
        result = {"result" : True}
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
    id = args.get("id")
    name = args.get("name")
    surname = args.get("surname")
    index = args.get("index")
    direction = args.get("direction")
    print(f"id : {id}")
    print(f"name : {name}")
    print(f"surname : {surname}")
    print(f"lastid : {index}")
    print(f"direction : {direction}")

    user = {
            "type" : "admin"
        }
    result = UserManager.getFilteredUsers(user ,id, name , surname, index, direction)
    return result , 200


@application.route('/admin/announcements' , methods = ['GET'])
#@required_token
def getAnnouncementToBeApproved():
    try:
        args = request.args
        index = args.get("index")
        direction = args.get("direction")
        result = AdminManager.getAnnouncementToApprove(index, direction)
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
    
    application.run(threaded=True , debug=True , use_reloader=True)