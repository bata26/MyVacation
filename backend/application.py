from controllers.analyticsManager import AnalyticsManager
from controllers.accommodationManager import AccommodationManager
from flask import Flask, abort, request, jsonify, Response
from dotenv import load_dotenv
from markupsafe import escape
from controllers.activityManager import ActivityManager
from controllers.reviewManager import ReviewManager
from controllers.userManager import UserManager
from controllers.userNodeManager import UserNodeManager
from models.accommodationNode import AccommodationNode
from models.activityNode import ActivityNode
from controllers.followRelationManager import FollowRelationManager
from controllers.likeRelationManager import LikeRelationManager
from controllers.accommodationNodeManager import AccommodationNodeManager
from controllers.activityNodeManager import ActivityNodeManager
from controllers.followRelationManager import FollowRelationManager
from models.activityNode import ActivityNode
from controllers.adminManager import AdminManager
from controllers.reservationManager import ReservationManager
from models.accommodation import Accommodation
from models.reservation import Reservation
from models.activity import Activity
from models.user import User
from models.userNode import UserNode
from models.likeRelation import LikeRelation
from models.followRelation import FollowRelation
from flask_cors import CORS, cross_origin
import json
from functools import wraps
import re
import bcrypt
from models.review import Review
import json
from werkzeug.datastructures import ImmutableMultiDict
import dateparser
from datetime import datetime
from utility.logger import Logger


load_dotenv()
application = Flask(__name__)
cors = CORS(
    application, supports_credentials=True, origins=["*", "http://127.0.0.1:3000"]
)


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
        print(request.headers.get("Authorization"))
        parsedUserObj = json.loads(request.headers.get("Authorization"))
        print(parsedUserObj)
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
    Logger.writeOnFile(json.dumps(nodeToDelete))
    return "", 200


@application.route("/analytics/topcities", methods=["GET"])
# @required_token
def getBestCities(user={}):
    try:
        res = AnalyticsManager.getTopCities()
        return res
    except Exception as e:
        return str(e), 500


@application.route("/analytics/topadv", methods=["GET"])
# @required_token
def getBestAdv(user={}):
    try:
        res = AnalyticsManager.getTopAdv()
        return res
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
        result["accommodations"] = AccommodationManager.getAccommodationsFromIdList(
            accommodationsID
        )
        result["activities"] = ActivityManager.getActivitiesFromIdList(activitiesID)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/analytics/monthReservations", methods=["GET"])
@required_token
def getMonthReservations(user={}):
    try:
        res = AnalyticsManager.getReservationByMonth(user)
        return res
    except Exception as e:
        return str(e), 500


@application.route("/analytics/usersForMonth", methods=["GET"])
@required_token
def getUsersForMonth(user={}):
    try:
        res = AnalyticsManager.getUsersForMonth()
        return res
    except Exception as e:
        return str(e), 500


@application.route("/analytics/averageAccommodations", methods=["GET"])
@required_token
def getAccommodationsAverageCost(user={}):
    try:
        res = AnalyticsManager.getAccommodationAverageCost(user)
        return res
    except Exception as e:
        return str(e), 500


@application.route("/analytics/averageActivities", methods=["GET"])
@required_token
def getActivitiesAverageCost(user={}):
    try:
        res = AnalyticsManager.getActivityAverageCost(user)
        return res
    except Exception as e:
        return str(e), 500


@application.route("/analytics/totalReservations", methods=["GET"])
@required_token
def getTotalReservations(user={}):
    try:
        res = AnalyticsManager.getTotReservations(user)
        return res
    except Exception as e:
        return str(e), 500


@application.route("/analytics/totalAdvertisement", methods=["GET"])
@required_token
def getTotalAdvs(user={}):
    try:
        res = AnalyticsManager.getTotAdvs(user)
        return res
    except Exception as e:
        return str(e), 500


@application.route("/activities/<activity_id>", methods=["DELETE"])
@required_token
def deleteActivityByID(activity_id, user={}):
    activityID = escape(activity_id)
    try:
        deleteResult = ActivityManager.deleteActivity(activityID, user)
    except Exception as e:
        return str(e), 500
    # provo ad eliminare il nodo
    try:
        if deleteResult:
            ActivityNodeManager.deleteActivityNode(activityID)
            return "OK", 200
    except Exception as e:
        # ho eliminato il documento ma non il nodo, aggiungo al logger
        Logger.addNodeToFile("activity", activityID)
        return str(e), 500


@application.route("/activities/<activity_id>", methods=["GET"])
def getActivityByID(activity_id):
    activityID = escape(activity_id)
    try:
        result = ActivityManager.getActivityFromID(activityID)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/activities", methods=["GET"])
def getActivities(user={}):
    args = request.args
    city = args.get("city")
    guests = args.get("guests")
    start_date = args.get("startDate")
    index = args.get("index")
    direction = args.get("direction")
    try:
        result = ActivityManager.getFilteredActivity(
            start_date, city, guests, index, direction
        )
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/accommodations/<accommodation_id>", methods=["DELETE"])
@required_token
def deleteaccommodationById(accommodation_id, user={}):
    accommodationID = escape(accommodation_id)
    try:
        deleteResult = AccommodationManager.deleteAccommodation(accommodationID, user)
    except Exception as e:
        return str(e), 500
    # provo ad eliminare il nodo
    try:
        if deleteResult:
            AccommodationNodeManager.deleteAccommodationNode(accommodationID)
            return "OK", 200
    except Exception as e:
        # ho eliminato il documento ma non il nodo, aggiungo al logger
        Logger.addNodeToFile("accommodation", accommodationID)
        return str(e), 500


@application.route("/update/accommodation/<accommodationID>", methods=["POST"])
@required_token
def updateAccommodationById(accommodationID, user={}):
    formData = dict(request.json)
    formData["location"] = {}
    formData["location"]["city"] = formData["city"]
    formData["location"]["address"] = formData["address"]
    formData["location"]["country"] = formData["country"]
    formData["guests"] = formData["guests"]
    formData["approved"] = False
    try:
        AccommodationManager.updateAccommodation(accommodationID, formData, user)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route("/update/activity/<activityID>", methods=["POST"])
@required_token
def updateActivityById(activityID, user={}):
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
        ActivityManager.updateActivity(activityID, formData, user)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route("/accommodations/<accommodation_id>", methods=["GET"])
def getAccommodationById(accommodation_id):
    accommodationID = escape(accommodation_id)
    try:
        result = AccommodationManager.getAccommodationFromId(accommodationID)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/book/accommodation", methods=["POST"])
@required_token
def bookAccommodation(user={}):
    if user["role"] != "admin":
        requestBody = request.json
        accommodation = requestBody["accommodation"]
        startDatetime = dateparser.parse(requestBody["startDate"])
        endDatetime = dateparser.parse(requestBody["endDate"])
        nightNumber = (endDatetime - startDatetime).days
        totalExpense = nightNumber * int(accommodation["price"])
        city = accommodation["city"]
        hostID = accommodation["hostID"]
        reservation = Reservation(
            user["_id"],
            accommodation["_id"],
            "accommodation",
            startDatetime,
            totalExpense,
            city,
            hostID,
            endDate=endDatetime,
        )
        try:
            reservationID = ReservationManager.book(reservation)
            return "OK", 200
        except Exception as e:
            return str(e), 500
    else:
        raise Exception("Admin non può prenotare")


@application.route("/reservation", methods=["PATCH"])
@required_token
def updateReservation(user={}):
    requestBody = request.json
    newStartDate = requestBody["startDate"]
    reservation = requestBody["reservation"]
    newEndDate = None
    if reservation["destinationType"] == "accommodation":
        newEndDate = requestBody["endDate"]
    try:
        ReservationManager.updateReservation(reservation, newStartDate, newEndDate)
        return "", 200
    except Exception as e:
        return e, 500


@application.route("/user/<user_id>", methods=["PATCH"])
@required_token
def updateUser(user_id, user={}):
    updatedData = request.json
    updatedData["dateOfBirth"] = dateparser.parse(updatedData["dateOfBirth"])
    try:
        if user["role"] != "admin" and user["_id"] != user_id:
            raise Exception("Impossibile aggiornare")
        else:
            UserManager.updateUser(updatedData, user_id)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route("/users/isfollowing/<user_id>", methods=["GET"])
@required_token
def checkIfIsFollowing(user_id , user={}):
    try:
        result = UserNodeManager.checkIfIsFollowing(user["_id"] , escape(user_id))
        return {"following" : result}, 200
    except Exception as e:
        return str(e), 500


@application.route("/users/following/<user_id>", methods=["GET"])
@required_token
def getFollowedUsersByUserID(user_id , user={}):
    try:
        result = UserNodeManager.getFollowedUser(escape(user_id))
        return result, 200
    except Exception as e:
        return str(e), 500

@application.route("/users/follow", methods=["POST"])
@required_token
def followUser(user={}):
    if user["role"] != "admin":
        requestBody = dict(request.json)
        try:
            followerNode = UserNode(user["_id"], user["username"])
            followedNode = UserNode(requestBody["userID"] , requestBody["username"])
            followRelation = FollowRelation(followerNode , followedNode)
            FollowRelationManager.addFollowRelation(followRelation)
            return "OK", 200
        except Exception as e:
            return str(e), 500
    else:
        raise Exception("Admin non può seguire")

@application.route("/users/liking/<destination_type>/<destination_id>", methods=["GET"])
@required_token
def checkIfUserLikesDestination(destination_type, destination_id , user={}):
    destinationType = escape(destination_type)
    try:
        result = UserNodeManager.checkIfUserLikesDestination(user["_id"], escape(destination_id), destinationType)
        return {"liked" : result}, 200
    except Exception as e:
        return str(e), 500


@application.route("/users/liked/<destination_type>/<user_id>", methods=["GET"])
@required_token
def getLikedAdvsByUserID(destination_type,user_id, user={}):
    destinationType = escape(destination_type)
    try:
        result = UserNodeManager.getLikedAdvs(escape(user_id), destinationType)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/users/liking", methods=["POST"])
@required_token
def likeAdv(user={}):
    if user["role"] != "admin":
        try:
            requestBody = request.json
            userNode = UserNode(user["_id"], user["username"])
            if requestBody["destinationType"] == "accommodation":
                accommodationNode = AccommodationNode(requestBody["likedAdvID"], requestBody["likedAdvName"])
                likeRelation = LikeRelation(userNode, accommodationNode=accommodationNode)
            elif requestBody["destinationType"] == "activity":
                activityNode = ActivityNode(requestBody["likedAdvID"], requestBody["likedAdvName"])
                likeRelation = LikeRelation(userNode, activityNode=activityNode)

            LikeRelationManager.addLikeRelation(likeRelation)
            return "", 200
        except Exception as e:
            return str(e), 500
    else:
        raise Exception("Admin non può mettere like")

@application.route("/commonadvs/<destination_type>/<user_id>", methods=["GET"])
@required_token
def getCommonAdv(destination_type, user_id, user={}):
    destinationType = escape(destination_type)
    userID = escape(user_id)

    userNode = UserNode(user["_id"], user["username"])
    try:
        if destinationType == "accommodation":
            result = AccommodationNodeManager.getCommonLikedAccommodation(userNode, userID)
        else:
            result = ActivityNodeManager.getCommonLikedActivity(userNode, userID)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/likenumber/<destination_type>/<destination_id>", methods=["GET"])
@required_token
def getTotalLike(destination_type, destination_id, user={}):
    destinationType = escape(destination_type)
    destinationID = escape(destination_id)
    try:
        if destinationType == "accommodation":
            total = AccommodationNodeManager.getTotalLikes(destinationID)
        else:
            total = ActivityNodeManager.getTotalLikes(destinationID)
        return {"likes": total}, 200
    except Exception as e:
        return str(e), 500


@application.route("/recommendations/user", methods=["GET"])
@required_token
def getRecommendedUsers(user={}):
    try:
        userNode = UserNode(user["_id"], user["username"])
        result = UserNodeManager.getRecommendedUsers(userNode)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/users/unfollow", methods=["POST"])
@required_token
def unfollowUser(user={}):
    if user["role"] != "admin":
        try:
            requestBody = request.json
            userNode = UserNode(user["_id"], user["username"])
            unfollowedUserNode = UserNode(requestBody["userID"], requestBody["username"])
            followRelation = FollowRelation(userNode,unfollowedUserNode)
            FollowRelationManager.removeFollowRelation(followRelation)
            return "", 200
        except Exception as e:
            return str(e), 500
    else:
        raise Exception("Admin non può smettere di seguire")

@application.route("/users/unliking", methods=["POST"])
@required_token
def unlikeAdv(user={}):
    if user["role"] != "admin":
        try:
            requestBody = request.json
            userNode = UserNode(user["_id"], user["username"])
            if requestBody["destinationType"] == "accommodation":
                accommodationNode = AccommodationNode(requestBody["unlikedAdvID"], requestBody["unlikedAdvName"])
                likeRelation = LikeRelation(userNode, accommodationNode=accommodationNode )
                LikeRelationManager.removeLikeRelation(likeRelation)
            elif requestBody["destinationType"] == "activity":
                activityNode = ActivityNode(requestBody["unlikedAdvID"], requestBody["unlikedAdvName"])
                likeRelation = LikeRelation(userNode, activityNode=activityNode )
                LikeRelationManager.removeLikeRelation(likeRelation)

            return "", 200
        except Exception as e:
            return str(e), 500
    else:
        raise Exception("Admin non può rimuovere il like")


@application.route("/recommendations/<destination_type>", methods=["GET"])
@required_token
def getRecommendedAdvs(destination_type, user={}):
    try:
        userNode = UserNode(user["_id"], user["username"])
        result = UserNodeManager.getRecommendedAdvs(userNode, destination_type)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/book/activity", methods=["POST"])
@required_token
def bookActivity(user={}):
    if user["role"] != "admin":
        requestBody = request.json
        activity = requestBody["activity"]
        startDate = dateparser.parse(requestBody["startDate"])
        city = activity["city"]
        hostID = activity["hostID"]
        reservation = Reservation(
            user["_id"],
            activity["_id"],
            "activity",
            startDate,
            activity["price"],
            city,
            hostID,
        )
        try:
            reservationID = ReservationManager.book(reservation)
            return reservationID, 200
        except Exception as e:
            return str(e), 500
    else:
        raise Exception("Admin non può prenotare")

@application.route("/reservations/<user_id>", methods=["GET"])
# @required_token
def getReservationsByUserID(user_id):
    userID = escape(user_id)
    try:
        result = ReservationManager.getReservationsByUser(userID)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/reservations/<reservation_id>", methods=["DELETE"])
@required_token
def deleteReservation(reservation_id, user={}):
    reservationID = escape(reservation_id)
    try:
        ReservationManager.deleteReservationByID(reservationID , user)
        return "OK", 200
    except Exception as e:
        return str(e), 500


@application.route("/accommodations", methods=["GET"])
# @required_token
def getAccommodations():
    args = request.args
    city = args.get("city")
    guests = args.get("guestsNumber")
    start_date = args.get("startDate")
    end_date = args.get("endDate")
    index = args.get("index")
    direction = args.get("direction")
    try:
        result = AccommodationManager.getFilteredAccommodation(
            start_date, end_date, city, guests, index, direction
        )
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/insert/accommodation", methods=["POST"])
@required_token
def insertAccommodations(user={}):
    if user["role"] != "admin":
        formData = dict(request.json)
        try:
            host = UserManager.getUserFromId(user["_id"])
            pictures = []
            imagesLength = formData["imagesLength"]
            for i in range(1, int(imagesLength)):
                pictures.append(formData["img"][i])

            location = {
                "address": formData["address"],
                "city": formData["city"],
                "country": formData["country"],
            }

            accommodation = Accommodation(
                formData["name"],
                formData["description"],
                host["_id"],
                host["name"],
                formData["img"][0],
                location,
                formData["propertyType"],
                formData["guests"],
                formData["bedrooms"],
                formData["beds"],
                formData["price"],
                False,
                pictures=pictures,
            )
            accommodationID = AccommodationManager.insertNewAccommodation(accommodation)
            if user["role"] != "host":
                updatedRole = {"type": "host"}
                UserManager.updateUser(updatedRole, host["_id"])
            return {"accommodationID": str(accommodationID)}, 200
        except Exception as e:
            return str(e), 500
    else:
        raise Exception("Admin non può inserire un alloggio")

@application.route("/insert/activity", methods=["POST"])
@required_token
def insertActivity(user={}):
    if user["role"] != "admin":
        formData = dict(request.form)
        host = UserManager.getUserFromId(user["_id"])
        pictures = []
        imagesLength = formData["imagesLength"]
        for i in range(1, int(imagesLength)):
            pictures.append(formData[f"img-{i}"])
        location = {
            "address": formData["address"],
            "city": formData["city"],
            "country": formData["country"],
        }

        activity = Activity(
            host["_id"],
            host["name"],
            location,
            formData["description"],
            formData["duration"],
            formData["price"],
            formData["img"][0],
            formData["category"],
            False,
        )
        try:
            activityID = ActivityManager.insertNewActivity(activity)
            return {"activityID": str(activityID)}, 200
        except Exception as e:
            return str(e), 500
    else:
        raise Exception("Admin non può inserire un'attività")

@application.route("/reviews/<review_id>", methods=["GET"])
# @required_token
def getReviewByID(review_id):
    reviewID = escape(review_id)
    try:
        result = ReviewManager.getReviewFromID(reviewID)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/reviewsByDestination/<destination_id>", methods=["GET"])
# @required_token
def getReviewByAd(destination_id):
    destinationID = escape(destination_id)
    try:
        result = ReviewManager.getReviewFromDestinationID(destinationID)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/reviews", methods=["PUT"])
@required_token
def insertReview(user={}):
    if user["role"] != "admin":
        requestBody = request.json
        destinationType = requestBody["destinationType"]
        reviewer = requestBody["reviewer"]
        review = Review(
            user["_id"],
            requestBody["destinationID"],
            requestBody["score"],
            requestBody["description"],
            reviewer,
        )
        try:
            insertedID = ReviewManager.insertNewReview(review)
            review._id = insertedID
            if destinationType == "accommodation":
                AccommodationManager.addReview(review)
            elif destinationType == "activity":
                ActivityManager.addReview(review)
            return "", 200
        except Exception as e:
            return str(e), 200
    else:
        raise Exception("Admin non può inserire recensione")

@application.route(
    "/reviews/<destinationType>/<destinationID>/<reviewID>", methods=["DELETE"]
)
@required_token
def deleteReviewByID(destinationType, destinationID, reviewID, user={}):
    reviewID = escape(reviewID)
    destinationType = escape(destinationType)
    destinationID = escape(destinationID)
    try:
        result = ReviewManager.deleteReview(
            reviewID, destinationID, destinationType, user
        )
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route("/users/<user_id>", methods=["DELETE"])
@required_token
def deleteUserById(user_id, user={}):
    userId = escape(user_id)
    try:
        result = AdminManager.deleteUser(userId, user)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route("/users/<user_id>", methods=["GET"])
@required_token
def getUserById(user_id, user={}):
    userId = escape(user_id)
    try:
        result = UserManager.getUserFromId(userId)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/review/check/<destination_id>", methods=["GET"])
@required_token
def getIfCanReview(destination_id, user={}):
    destinationID = escape(destination_id)
    user = json.loads(request.headers.get("Authorization"))
    args = request.args
    destinationType = args["destinationType"]
    result = {"result": False}
    try:
        if ReviewManager.checkIfCanReview(str(destinationID), destinationType, user):
            result = {"result": True}
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/login", methods=["POST"])
# @required_token
def loginUser():
    username = request.json["username"]
    password = request.json["password"]
    try:
        userID, userType, username, name = UserManager.authenicateUser(
            username, password
        )
        return {
            "userID": userID,
            "role": userType,
            "name": name,
            "username": username,
        }, 200
    except Exception as e:
        return str(e), 500


@application.route("/signup", methods=["POST"])
# @required_token
def signUp():
    username = request.json["username"]
    password = request.json["password"]
    name = request.json["name"]
    surname = request.json["surname"]
    gender = request.json["gender"]
    dateOfBirth = request.json["dateOfBirth"]
    nationality = request.json["nationality"]
    knownLanguages = request.json["knownLanguages"]

    salt = bcrypt.gensalt(12)
    dbHash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
    user = User(
        username,
        dbHash,
        name,
        surname,
        "user",
        gender,
        dateparser.parse(dateOfBirth),
        nationality,
        knownLanguages,
        [],
        datetime.today().replace(microsecond=0, second=0, hour=0, minute=0),
    )
    try:
        insertedID = UserManager.insertNewUser(user)
    except Exception as e:
        return str(e), 500
    # documento inserito nel document, tento creazione nodo
    try:
        userNode = UserNode(insertedID, username)
        UserNodeManager.createUserNode(userNode)
        return "OK" , 200
    except Exception as e:
        Logger.addNodeToFile("user", insertedID, "CREATE", username)
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
        result = AdminManager.getFilteredUsers(
            user, username, name, surname, index, direction
        )
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/admin/announcements/<destination_type>", methods=["GET"])
@required_token
def getAnnouncementsToBeApproved(destination_type, user={}):
    args = request.args
    index = args.get("index")
    direction = args.get("direction")
    try:
        result = AdminManager.getAnnouncementsToApprove(
            index, direction, destination_type
        )
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route(
    "/admin/announcement/<destination_type>/<announcementID>", methods=["GET"]
)
# @required_token
def getAnnouncementToBeApprovedByID(destination_type, announcementID):
    try:
        if not (validateObjecID(announcementID)):
            return "Announcement non valido", 500
        result = AdminManager.getAnnouncementToApproveByID(
            announcementID, destination_type
        )
        return result, 200
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
        try:
            # provo ad approvare
            AdminManager.approveAnnouncement(announcementID, user, destinationType)
        except Exception as e:
            raise Exception(str(e))
        # se l'approvazione è andata bene provo a creare il nodo accommodation
        try:
            if destinationType == "accommodation":
                accommodationNode = AccommodationNode(announcementID, destinationName)
                AccommodationNodeManager.createAccommodationNode(accommodationNode)
            else:
                activityNode = ActivityNode(announcementID, destinationName)
                ActivityNodeManager.createActivityNode(activityNode)
        except Exception as e:
            # eseguo il rollback se non riesco a creare il nodo
            AdminManager.removeApprovalAnnouncement(announcementID, user, destinationType)
            raise Exception(str(e))
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route(
    "/admin/announcement/<destination_type>/<announcementID>", methods=["DELETE"]
)
@required_token
def refuseAnnouncement(destination_type, announcementID, user={}):
    if not (validateObjecID(announcementID)):
        return "Announcement non valido", 500
    try:
        if destination_type == "accommodation":
            AccommodationManager.deleteAccommodation(announcementID, user)
        elif destination_type == "activity":
            ActivityManager.deleteActivity(announcementID, user)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route("/myadvacc/<user_id>", methods=["GET"])
# @required_token
def getAccommodationsByUserID(user_id):
    userID = escape(user_id)
    try:
        result = AccommodationManager.getAccommodationsByUserID(userID)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route("/myadvact/<user_id>", methods=["GET"])
# @required_token
def getActivitiesByUserID(user_id):
    userID = escape(user_id)
    try:
        result = ActivityManager.getActivityByUserID(userID)
        return result, 200
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":

    application.run(threaded=True, debug=True, use_reloader=True)
