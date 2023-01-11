from controllers.accommodationController import AccommodationController
from controllers.activityController import ActivityController
from controllers.reviewController import ReviewController
from controllers.userController import UserController
from controllers.analyticsController import AnalyticsController
from controllers.reservationController import ReservationController
from controllers.adminController import AdminController
from flask import Flask,request, Response
from dotenv import load_dotenv
from markupsafe import escape
from models.userNode import UserNode
from flask_cors import CORS
import json
from functools import wraps
import re
import json
import dateparser
from worker import startup
from utility.logger import Logger
from datetime import datetime
from datetime import date
from flask import jsonify
load_dotenv()
application = Flask(__name__)
cors = CORS(application, supports_credentials=True, origins=["*", "http://127.0.0.1:3000"])


def validateObjecID(userID):
    validationRegex = "^[0-9a-fA-F]{24}$"
    if re.match(validationRegex, userID):
        return True
    return False


def required_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if "Authorization" not in request.headers:
            return Response(json.dumps(f"Authorization token not found"), 401)
        parsedUserObj = json.loads(request.headers.get("Authorization"))
        userID = parsedUserObj["_id"]
        if not (validateObjecID(userID)):
            return Response(json.dumps("userID non valido"), 403)

        return f(*args, **kwargs, user=parsedUserObj)

    return decorator


@application.route("/test", methods=["GET"])
@required_token
def testValidation(user={}):
    activityID = "325342tfwregregf"
    nodeToDelete = {"type": "activity", "_id": activityID}
    return "", 200


@application.route("/analytics/topcities", methods=["GET"])
def getBestCities():
    try:
        return jsonify(AnalyticsController.getBestCities()) , 200
    except Exception as e:
        return str(e), 500


@application.route("/analytics/topadv", methods=["GET"])
# @required_token
def getBestAdv():
    try:
        return jsonify(AnalyticsController.getTopAdv()) , 200
    except Exception as e:
        return str(e), 500


@application.route("/analytics/advinfo", methods=["POST"])
# @required_token
def getBestAdvInfo(user={}):
    try:
        requestBody = request.json
        accommodationsID = requestBody["accommodationsID"]
        activitiesID = requestBody["activitiesID"]
        result = {}
        result["accommodations"] = AccommodationController.getTopAdvInfo(accommodationsID)
        result["activities"] = ActivityController.getTopAdvInfo(activitiesID)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/analytics/monthReservations", methods=["GET"])
@required_token
def getMonthReservations(user={}):
    try:
        return jsonify(AnalyticsController.getMonthReservations(user)) , 200
    except Exception as e:
        return str(e), 500


@application.route("/analytics/usersForMonth", methods=["GET"])
@required_token
def getUsersForMonth(user={}):
    try:
        return jsonify(AnalyticsController.getUsersForMonth()) , 200
    except Exception as e:
        return str(e), 500


@application.route("/analytics/averageAccommodations", methods=["GET"])
@required_token
def getAccommodationsAverageCost(user={}):
    try:
        return jsonify(AnalyticsController.getAccommodationsAverageCost(user)) , 200
    except Exception as e:
        return str(e), 500


@application.route("/analytics/averageActivities", methods=["GET"])
@required_token
def getActivitiesAverageCost(user={}):
    try:
        return jsonify(AnalyticsController.getActivitiesAverageCost(user)) , 200
    except Exception as e:
        return str(e), 500


@application.route("/analytics/totalReservations", methods=["GET"])
@required_token
def getTotalReservations(user={}):
    try:
        return jsonify(AnalyticsController.getTotalReservations(user)) , 200
    except Exception as e:
        return str(e), 500


@application.route("/analytics/totalAdvertisement", methods=["GET"])
@required_token
def getTotalAdvs(user={}):
    try:
        return jsonify(AnalyticsController.getTotalAdvs(user)) , 200
    except Exception as e:
        return str(e), 500


@application.route("/activities/<activity_id>", methods=["DELETE"])
@required_token
def deleteActivityByID(activity_id, user={}):
    activityID = escape(activity_id)   
    try:
        deleteResult = ActivityController.deleteActivityById(activityID, user)
        if(not(deleteResult)):
            Logger.addNodeToFile("activity", activityID , "DELETE")
            return str(e), 500
    except Exception as e:
        return str(e), 500


@application.route("/activities/<activity_id>", methods=["GET"])
def getActivityByID(activity_id):
    activityID = escape(activity_id)
    try:
        return jsonify(ActivityController.getActivityByID(activityID)) , 200
    except Exception as e:
        return str(e), 500


@application.route("/activities", methods=["GET"])
def getActivities(user={}):
    args = request.args
    city = args.get("city")
    start_date = args.get("startDate")
    index = args.get("index")
    direction = args.get("direction")
    try:
        if start_date != "" and start_date is not None:
            if dateparser.parse(start_date).date() < date.today():
                raise Exception("Impossibile ricercare")

        return jsonify(ActivityController.getActivities(start_date, city, index, direction)), 200
    except Exception as e:
        return str(e), 500


@application.route("/accommodations/<accommodation_id>", methods=["DELETE"])
@required_token
def deleteAccommodationById(accommodation_id, user={}):
    accommodationID = escape(accommodation_id)
    try:
        deleteResult = AccommodationController.deleteAccommodationById(accommodationID, user)
        if(not(deleteResult)):
            Logger.addNodeToFile("accommodation", accommodationID , "DELETE")
            return "Da aggiornare il nodo" , 500    
        return "OK" , 200
    except Exception as e:
        return str(e), 500


@application.route("/edit/accommodation/<accommodationID>", methods=["POST"])
@required_token
def editAccommodationById(accommodationID, user={}):
    formData = dict(request.json)
    formData["location"] = {}
    formData["location"]["city"] = formData["city"]
    formData["location"]["address"] = formData["address"]
    formData["location"]["country"] = formData["country"]
    formData["guests"] = formData["guests"]
    formData["approved"] = False
    try:
        updateResult = AccommodationController.updateAccommodation(accommodationID, formData, user)
        if(not(updateResult)):
            Logger.addNodeToFile("accommodation" , accommodationID , "UPDATE" , formData["name"])
            return "Da aggiornare il nodo" , 500
        return "OK", 200
    except Exception as e:
        return str(e), 500


@application.route("/edit/activity/<activityID>", methods=["POST"])
@required_token
def editActivityById(activityID, user={}):
    formData = dict(request.json)
    formData["location"] = {}
    formData["location"]["city"] = formData["city"]
    formData["location"]["address"] = formData["address"]
    formData["location"]["country"] = formData["country"]
    formData.pop("city")
    formData.pop("address")
    formData.pop("country")
    formData["approved"] = False
    try:
        updateResult = ActivityController.updateActivity(activityID, formData, user)
        if(not(updateResult)):
            Logger.addNodeToFile("activity" , activityID , "UPDATE" , formData["name"])
            return "Da aggiornare il nodo" , 500
        return "OK", 200
    except Exception as e:
        return str(e), 500


@application.route("/accommodations/<accommodation_id>", methods=["GET"])
def getAccommodationById(accommodation_id):
    accommodationID = escape(accommodation_id)
    try:
        return jsonify(AccommodationController.getAccommodationById(accommodationID)) , 200
    except Exception as e:
        return str(e), 500


@application.route("/book/accommodation", methods=["POST"])
@required_token
def bookAccommodation(user={}):
    try:
        if user["role"] != "admin":
            requestBody = dict(request.json)
            ReservationController.bookAccommodation(requestBody , user)
            return "OK" , 200
        else:
            raise Exception("Admin non può prenotare")
    except Exception as e:
        return str(e) , 500


@application.route("/reservation", methods=["PATCH"])
@required_token
def updateReservation(user={}):
    requestBody = dict(request.json)
    try:
        ReservationController.updateReservation(requestBody , user)
        return "OK", 200
    except Exception as e:
        return str(e), 500


@application.route("/user/<user_id>", methods=["PATCH"])
@required_token
def updateUser(user_id, user={}):
    updatedData = dict(request.json)
    updatedData["dateOfBirth"] = dateparser.parse(updatedData["dateOfBirth"])
    try:
        if user["role"] != "admin" and user["_id"] != user_id:
            raise Exception("Impossibile aggiornare")

        UserController.updateUser(updatedData, user_id)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route("/users/isfollowing/<user_id>", methods=["GET"])
@required_token
def checkIfIsFollowing(user_id , user={}):
    try:
        return jsonify(UserController.checkIfIsFollowing(user["_id"] , escape(user_id))) , 200
    except Exception as e:
        return str(e), 500


@application.route("/users/following/<user_id>", methods=["GET"])
@required_token
def getFollowedUsersByUserID(user_id , user={}):
    try:
        return jsonify(UserController.getFollowedUser(escape(user_id))) , 200
    except Exception as e:
        return str(e), 500

@application.route("/users/follow", methods=["POST"])
@required_token
def followUser(user={}):
    if user["role"] != "admin":
        requestBody = dict(request.json)
        try:
            UserController.followUser(requestBody , user)
            return "OK", 200
        except Exception as e:
            return str(e), 500
    else:
        return "Admin non può seguire" , 500

@application.route("/users/liking/<destination_type>/<destination_id>", methods=["GET"])
@required_token
def checkIfUserLikesDestination(destination_type, destination_id , user={}):
    try:
        return UserController.checkIfLike(user["_id"], escape(destination_id), escape(destination_type)) , 200
    except Exception as e:
        return str(e), 500


@application.route("/users/liked/<destination_type>/<user_id>", methods=["GET"])
@required_token
def getLikedAdvsByUserID(destination_type,user_id, user={}):
    try:
        return jsonify(UserController.getLikedAdvs(escape(user_id), escape(destination_type))) , 200
    except Exception as e:
        return str(e), 500


@application.route("/users/liking", methods=["POST"])
@required_token
def likeAdv(user={}):
    if user["role"] != "admin":
        try:
            requestBody = dict(request.json)
            if requestBody["destinationType"] == "accommodation":
                AccommodationController.likeAccommodation(requestBody , user)
            elif requestBody["destinationType"] == "activity":
                ActivityController.likeActivity(requestBody , user)
            return "OK", 200
        except Exception as e:
            return str(e), 500
    else:
        raise Exception("Admin non può mettere like")

@application.route("/commonadvs/<destination_type>/<user_id>", methods=["GET"])
@required_token
def getCommonAdv(destination_type, user_id, user={}):
    destinationType = escape(destination_type)
    try:
        if destinationType == "accommodation":
            return jsonify(AccommodationController.getCommonAccommodation(user, escape(user_id))) , 200
        else:
            return jsonify(ActivityController.getCommonActivity(user, escape(user_id))) , 200
    except Exception as e:
        return str(e), 500


@application.route("/likenumber/<destination_type>/<destination_id>", methods=["GET"])
@required_token
def getTotalLikes(destination_type, destination_id, user={}):
    destinationType = escape(destination_type)
    try:
        if destinationType == "accommodation":
            return jsonify(AccommodationController.getTotalLikes(escape(destination_id))) , 200
        else:
            return jsonify(ActivityController.getTotalLikes(escape(destination_id))) , 200
        
    except Exception as e:
        return str(e), 500


@application.route("/recommendations/user", methods=["GET"])
@required_token
def getRecommendedUsers(user={}):
    try:
        return jsonify(UserController.getRecommendedUsers(user)) , 200
    except Exception as e:
        return str(e), 500


@application.route("/users/unfollow", methods=["POST"])
@required_token
def unfollowUser(user={}):
    if user["role"] != "admin":
        try:
            requestBody = dict(request.json)
            UserController.unfollowUser(requestBody , user)      
            return "OK", 200
        except Exception as e:
            return str(e), 500
    else:
        return "Admin non può smettere di seguire" , 500

@application.route("/users/unliking", methods=["POST"])
@required_token
def dislikeAdv(user={}):
    if user["role"] != "admin":
        try:
            requestBody = dict(request.json)
            
            if requestBody["destinationType"] == "accommodation":
                AccommodationController.dislikeAccommodation(requestBody , user)
            elif requestBody["destinationType"] == "activity":
                ActivityController.dislikeActivity(requestBody , user)
            return "OK", 200
        except Exception as e:
            return str(e), 500
    else:
        raise Exception("Admin non può rimuovere il like")


@application.route("/recommendations/<destination_type>", methods=["GET"])
@required_token
def getRecommendedAdvs(destination_type, user={}):
    try:
        return jsonify(UserController.getRecommendedAdvs(escape(destination_type) , user)), 200
    except Exception as e:
        return str(e), 500


@application.route("/book/activity", methods=["POST"])
@required_token
def bookActivity(user={}):
    try:
        if user["role"] != "admin":
            requestBody = dict(request.json)
            ReservationController.bookActivity(requestBody , user)
            return "OK", 200
            
        else:
            raise Exception("Admin non può prenotare")
    except Exception as e:
                return str(e), 500

@application.route("/reservations/<user_id>", methods=["GET"])
@required_token
def getReservationsByUserID(user_id , user={}):
    try:
        return jsonify(ReservationController.getReservationsByUserID(escape(user_id))) , 200
    except Exception as e:
        return str(e), 500

@application.route("/reservationsHost/<host_id>", methods=["GET"])
@required_token
def getReservationsByHostID(host_id , user={}):
    try:
        return jsonify(ReservationController.getReservationsByHostID(escape(host_id))) , 200
    except Exception as e:
        return str(e), 500

@application.route("/reservations/<reservation_id>", methods=["DELETE"])
@required_token
def deleteReservation(reservation_id, user={}):
    try:
        ReservationController.deleteReservation(escape(reservation_id) , user)
        return "OK", 200
    except Exception as e:
        return str(e), 500


@application.route("/accommodations", methods=["GET"])
def getAccommodations():
    args = request.args
    city = args.get("city")
    guests = args.get("guestsNumber")
    start_date = args.get("startDate")
    end_date = args.get("endDate")
    index = args.get("index")
    direction = args.get("direction")
    
    try:
        if start_date != "" and start_date is not None :
            if dateparser.parse(start_date).date() < date.today():
                raise Exception("Impossibile ricercare")
            if end_date != "" and end_date is not None:
                if dateparser.parse(end_date) < dateparser.parse(start_date):
                    raise Exception("Impossibile ricercare")
        return jsonify(AccommodationController.getFilteredAccommodations(
            start_date, end_date, city, guests, index, direction
        )), 200
    except Exception as e:
        return str(e), 500


@application.route("/insert/accommodation", methods=["POST"])
@required_token
def insertAccommodation(user={}):
    if user["role"] != "admin":
        formData = dict(request.json)
        try:
           return jsonify(AccommodationController.insertAccommodation(formData , user)) , 200
        except Exception as e:
            return str(e), 500
    else:
        return "Admin non può inserire un alloggio" , 500

@application.route("/insert/activity", methods=["POST"])
@required_token
def insertActivity(user={}):
    if user["role"] != "admin":
        formData = dict(request.json)
        try:
            return jsonify(ActivityController.insertActivity(formData , user)) , 200
        except Exception as e:
            return str(e), 500
    else:
        return "Admin non può inserire un'attività" , 500

@application.route("/reviews/<review_id>", methods=["GET"])
# @required_token
def getReviewByID(review_id):
    reviewID = escape(review_id)
    try:
        return jsonify(ReviewController.getReviewByID(reviewID))  ,200
    except Exception as e:
        return str(e), 500


@application.route("/reviewsByDestination/<destination_id>", methods=["GET"])
# @required_token
def getReviewByAd(destination_id):
    destinationID = escape(destination_id)
    try:
        return jsonify(ReviewController.getReviewByDestinationID(destinationID)) , 200
    except Exception as e:
        return str(e), 500


@application.route("/reviews", methods=["PUT"])
@required_token
def insertReview(user={}):
    if user["role"] != "admin":
        try:
            requestBody = dict(request.json)
            destinationType = requestBody["destinationType"]
            if destinationType == "accommodation":
                AccommodationController.insertReview(requestBody , user)
            elif destinationType == "activity":
                ActivityController.insertReview(requestBody , user)
            return "OK", 200
        except Exception as e:
            return str(e), 200
    else:
        raise Exception("Admin non può inserire recensione")

@application.route("/reviews/<destinationType>/<destinationID>/<reviewID>", methods=["DELETE"])
@required_token
def deleteReviewByID(destinationType, destinationID, reviewID, user={}):
    reviewID = escape(reviewID)
    destinationType = escape(destinationType)
    destinationID = escape(destinationID)
    try:
        ReviewController.deleteReview(reviewID, destinationID, destinationType, user)
        return "OK", 200
    except Exception as e:
        return str(e), 500


@application.route("/users/<user_id>", methods=["DELETE"])
@required_token
def deleteUserById(user_id, user={}):
    try:
        if(AdminController.deleteUser(escape(user_id), user)):
            return "OK", 200
        else:
            Logger.addNodeToFile("user" , escape(user_id) , "DELETE")
            return "Impossibile creare nodo" , 500
    except Exception as e:
        return str(e), 500


@application.route("/users/<user_id>", methods=["GET"])
@required_token
def getUserByID(user_id, user={}):
    userID = escape(user_id)
    try:
        return UserController.getUserByID(userID) , 200
    except Exception as e:
        return str(e), 500


@application.route("/review/check/<destination_id>", methods=["GET"])
@required_token
def getIfCanReview(destination_id, user={}):
    destinationID = escape(destination_id)
    args = request.args
    try:
        result = ReviewController.checkIfCanReview(str(destinationID), user)
        return {"result" : result} , 200
    except Exception as e:
        return str(e), 500


@application.route("/login", methods=["POST"])
# @required_token
def loginUser():
    username = request.json["username"]
    password = request.json["password"]
    try:
        return jsonify(UserController.authenticateUser(username, password)) , 200
    except Exception as e:
        return str(e), 500


@application.route("/signup", methods=["POST"])
# @required_token
def signUp():
   
    requestBody = dict(request.json)
    try:
        insertedID , result = UserController.registerUser(requestBody)
        if(not(result)):    
            Logger.addNodeToFile("user", insertedID , "CREATE" , requestBody["username"])
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route("/users", methods=["GET"])
@required_token
def getUsers(user):
    args = request.args
    username = args.get("username")
    name = args.get("name")
    surname = args.get("surname")
    index = args.get("index")
    direction = args.get("direction")
    try:
        return jsonify(AdminController.getUsers(
            user, username, name, surname, index, direction
        )) , 200
    except Exception as e:
        return str(e), 500


@application.route("/admin/announcements/<destination_type>", methods=["GET"])
@required_token
def getAnnouncementsToBeApproved(destination_type, user={}):
    args = request.args
    index = args.get("index")
    direction = args.get("direction")
    try:
        return jsonify(AdminController.getAnnouncementsToBeApproved(
            index, direction, escape(destination_type)
        )) , 200
    except Exception as e:
        return str(e), 500


@application.route("/admin/announcement/<destination_type>/<announcementID>", methods=["GET"])
@required_token
def getAnnouncementToBeApprovedByID(destination_type, announcementID , user={}):
    try:
        if not (validateObjecID(escape(announcementID))):
            raise Exception("Announcement non valido")
        return jsonify(AdminController.getAnnouncementToBeApprovedByID(escape(announcementID), escape(destination_type))) , 200
    except Exception as e:
        return str(e), 500


@application.route("/admin/announcement/<announcementID>", methods=["POST"])
@required_token
def approveAnnouncement(announcementID, user={}):
    if not (validateObjecID(announcementID)):
        return "Announcement non valido", 500
    try:
        requestBody = request.json
        destinationType = requestBody["destinationType"]
        destinationName = requestBody["destinationName"]
        AdminController.approveAnnouncement(announcementID , destinationType , destinationName , user)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route("/admin/announcement/<destination_type>/<announcementID>", methods=["DELETE"])
@required_token
def refuseAnnouncement(destination_type, announcementID, user={}):
    if not (validateObjecID(announcementID)):
        return "Announcement non valido", 500
    try:

        if escape(destination_type) == "accommodation":
            result = AccommodationController.refuseAccommodation(escape(announcementID), user)
        elif escape(destination_type) == "activity":
            result = ActivityController.refuseActivity(escape(announcementID), user)
        if not(result):
            Logger.addNodeToFile(escape(destination_type) , escape(announcementID) , "DELETE")
        return "OK", 200
    except Exception as e:
        return str(e), 500


@application.route("/myadvacc/<user_id>", methods=["GET"])
# @required_token
def getAccommodationsByUserID(user_id):
    userID = escape(user_id)
    try:
        result = AccommodationController.getAccommodationsByUserID(userID)
        return jsonify(result), 200
    except Exception as e:
        return str(e), 500


@application.route("/myadvact/<user_id>", methods=["GET"])
@required_token
def getActivitiesByUserID(user_id , user={}):
    userID = escape(user_id)
    try:
        return jsonify(ActivityController.getActivityByUserID(userID)) , 200
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    startup()
    #application.run(threaded=True, debug=True, use_reloader=True)
    application.run(host = "0.0.0.0" , threaded=True, debug=True, use_reloader=True)
