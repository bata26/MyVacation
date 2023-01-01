from controllers.analyticsManager import AnalyticsManager
from controllers.accomodationsManager import AccomodationsManager
from flask import Flask, abort, request, jsonify, Response
from dotenv import load_dotenv
from markupsafe import escape
from controllers.activityManager import ActivityManager
from controllers.reviewManager import ReviewManager
from controllers.userManager import UserManager
from controllers.userNodeManager import UserNodeManager
from controllers.followRelationManager import FollowRelationManager
from controllers.likeRelationManager import LikeRelationManager
from models.accomodationNode import AccomodationNode
from models.activityNode import ActivityNode
from controllers.userNodeManager import UserNodeManager
from controllers.followRelationManager import FollowRelationManager
from controllers.likeRelationManager import LikeRelationManager
from models.accomodationNode import AccomodationNode
from models.activityNode import ActivityNode
from controllers.adminManager import AdminManager
from controllers.reservationManager import ReservationManager
from models.accomodation import Accomodation
from models.reservation import Reservation
from models.activity import Activity
from models.user import User
from models.userNode import UserNode
from models.userNode import UserNode
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

# user = {
#   "_id": "637ce1a04ed62608566c5fa7"
# }

load_dotenv()
application = Flask(__name__)
cors = CORS(application, supports_credentials=True,
            origins=["*", "http://127.0.0.1:3000"])


def validateObjecID(userID):
    validationRegex = "^[0-9a-fA-F]{24}$"
    if re.match(validationRegex, userID):
        return True
    return False


def required_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return Response(json.dumps(f"Authorization token not found"), 401)
        print(request.headers.get('Authorization'))
        parsedUserObj = json.loads(request.headers.get('Authorization'))
        print(parsedUserObj)
        userID = parsedUserObj["_id"]
        if (not (validateObjecID(userID))):
            return Response(json.dumps("userID non valido"), 403)

        return f(*args, **kwargs, user=parsedUserObj)

    return decorator


@application.route("/test", methods=["POST"])
@required_token
def testValidation(user={}):
    requestBody = dict(request.json)

    userNode = UserNode(requestBody["userID"] , requestBody["username"])
    UserManager.createUserNode(userNode)
    return "" , 200


@application.route("/analytics/topcities", methods=["GET"])
#@required_token
def getBestCities(user={}):
    try:
        res = AnalyticsManager.getTopCities()
        return res
    except Exception as e:
        return str(e), 500


@application.route("/analytics/topadv", methods=["GET"])
#@required_token
def getBestAdv(user={}):
    try:
        res = AnalyticsManager.getTopAdv()
        return res
    except Exception as e:
        return str(e), 500


@application.route("/analytics/advinfo", methods=["POST"])
#@required_token
def getBestAdvInfo(user={}):
    try:
        requestBody = request.json
        accomodationsID = requestBody["accomodationsID"]
        activitiesID = requestBody["activitiesID"]
        result = {}
        result["accomodations"] = AccomodationsManager.getAccomodationsFromIdList(accomodationsID)
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

@application.route("/analytics/averageAccomodations", methods=["GET"])
@required_token
def getAccomodationsAverageCost(user={}):
    try:
        res = AnalyticsManager.getAccomodationAverageCost(user)
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

@application.route("/analytics/bestHost/<destinationType>", methods=["GET"])
@required_token
def getBestHost(destinationType , user={}):
    try:
        res = AnalyticsManager.getBestAdvertisers(user , escape(destinationType))
        return res
    except Exception as e:
        return str(e), 500

@application.route('/activities/<activity_id>', methods=['DELETE'])
@required_token
def deleteActivityByID(activity_id, user={}):
    activityID = escape(activity_id)
    try:
        result = ActivityManager.deleteActivity(activityID, user)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route('/activities/<activity_id>', methods=['GET'])
# @required_token
def getActivityByID(activity_id):
    activityID = escape(activity_id)
    try:
        result = ActivityManager.getActivityFromID(activityID)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route('/activities', methods=['GET'])
#@required_token
def getActivities(user={}):
    args = request.args
    city = args.get("city")
    guests = args.get("guests")
    start_date = args.get("startDate")
    index = args.get("index")
    direction = args.get("direction")
    try:
        result = ActivityManager.getFilteredActivity(
            start_date, city, guests, index, direction)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route('/accomodations/<accomodation_id>', methods=['DELETE'])
@required_token
def deleteAccomodationById(accomodation_id, user={}):
    accomodationId = escape(accomodation_id)
    try:
        result = AccomodationsManager.deleteAccomodation(accomodationId, user)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route('/edit/accomodations/<accomodationID>', methods=['POST'])
@required_token
def updateAccomodationById(accomodationID, user={}):
    formData = dict(request.json)
    formData["location"] = {}
    formData["location"]["city"] = formData["city"]
    formData["location"]["address"] = formData["address"]
    formData["location"]["country"] = formData["country"]
    formData.pop("city")
    formData.pop("address")
    formData.pop("country")
    formData["accommodates"] = formData["accommodates"]
    formData["approved"] = False
    try:
        result = AccomodationsManager.updateAccomodation(
            accomodationID, formData, user)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route('/edit/activities/<activityID>', methods=['POST'])
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
        result = ActivityManager.updateActivity(
            activityID, formData, user)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route('/accomodations/<accomodation_id>', methods=['GET'])
# @required_token
def getAccomodationById(accomodation_id):
    accomodationId = escape(accomodation_id)
    try:
        result = AccomodationsManager.getAccomodationFromId(accomodationId)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route('/book/accomodation', methods=['POST'])
@required_token
def bookAccomodation(user={}):
    requestBody = request.json
    accomodation = requestBody["accomodation"]
    user = json.loads(request.headers.get('Authorization'))
    startDatetime = dateparser.parse(requestBody["startDate"])
    endDatetime = dateparser.parse(requestBody["endDate"])
    nightNumber = (((endDatetime - startDatetime).days))
    totalExpense = nightNumber*accomodation["price"]
    city = accomodation["city"]
    hostID = accomodation["hostID"]
    reservation = Reservation(user['_id'], accomodation["_id"], "accomodation",
                              startDatetime, totalExpense, city, hostID, endDatetime)
    try:
        reservationID = ReservationManager.book(reservation)
        return "OK", 200
    except Exception as e:
        return str(e), 500


@application.route('/reservation/<reservation_id>', methods=['PATCH'])
@required_token
def updateReservation(reservation_id, user={}):
    requestBody = request.json
    newStartDate = requestBody["startDate"]
    reservation = requestBody["reservation"]
    newEndDate = None
    if (reservation['destinationType'] == "accomodation"):
        newEndDate = requestBody["endDate"]
    try:
        ReservationManager.updateReservation(reservation, newStartDate, newEndDate)
        if(reservation['destinationType'] == "accomodation"):
            AccomodationsManager.updateReservation(reservation, newStartDate, newEndDate)
        else:
             ActivityManager.updateReservation(reservation, newStartDate)
        return "", 200
    except Exception as e:
        return e, 500

@application.route('/user/<user_id>', methods=['PATCH'])
@required_token
def updateUser(user_id, user={}):
    updatedData = request.json
    updatedData["dateOfBirth"] = dateparser.parse(updatedData["dateOfBirth"])
    try:
        if(user["role"] != "admin" and user["_id"] != user_id):
            raise Exception("Impossibile aggiornare")
        else:
            UserManager.updateUser(updatedData, user_id)
        return "", 200
    except Exception as e:
        return str(e), 500

@application.route('/user/following', methods=['GET'])
@required_token
def getFollowedUsersByUserID(user={}):
    try:
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        UserNodeManager.getFollowedUser(userNode)
        return "", 200
    except Exception as e:
        return str(e), 500

@application.route('/user/following', methods=['GET'])
@required_token
def getFollowedUsersByUserID(user={}):
    try:
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        UserNodeManager.getFollowedUser(userNode)
        return "", 200
    except Exception as e:
        return str(e), 500

@application.route('/user/following', methods=['POST'])
@required_token
def followUser(user={}):
    try:
        requestBody = request.json
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        followedUserNode = UserNode(
            requestBody["followedUserID"],
            requestBody["followedUsername"]
        )
        FollowRelationManager.addFollowRelation(userNode, followedUserNode)
        return "", 200
    except Exception as e:
        return str(e), 500

@application.route('/users/unfollowing', methods=['POST'])
@required_token
def unfollowUser(user={}):
    try:
        requestBody = request.json
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        unfollowedUserNode = UserNode(
            requestBody["unfollowedUserID"],
            requestBody["unfollowedUsername"]
        )
        FollowRelationManager.removeFollowRelation(userNode, unfollowedUserNode)
        return "", 200
    except Exception as e:
        return str(e), 500

@application.route('/users/liking/<destination_type>', methods=['GET'])
@required_token
def getLikedAdvsByUserID(destination_type, user={}):
    try:
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        UserNodeManager.getLikedAdvs(userNode, destination_type)
        return "", 200
    except Exception as e:
        return str(e), 500

@application.route('/users/liking', methods=['POST'])
@required_token
def likeAdv(user={}):
    try:
        requestBody = request.json
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        if(requestBody["destinationType"] == "accomodation"):
            likedAdv = AccomodationNode(
            requestBody["likedAdvID"],
            requestBody["likedAdvName"]
            )
            LikeRelationManager.addLikeRelation(userNode, accomodationNode=likedAdv)
        elif(requestBody["destinationType"] == "activity"):
            likedAdv = ActivityNode(
                requestBody["likedAdvID"],
                requestBody["likedAdvName"]
            )
            LikeRelationManager.addLikeRelation(userNode, activityNode=likedAdv)
        return "", 200
    except Exception as e:
        return str(e), 500

@application.route('/users/unliking', methods=['POST'])
@required_token
def unlikeAdv(user={}):
    try:
        requestBody = request.json
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        if(requestBody["destinationType"] == "accomodation"):
            unlikedAdv = AccomodationNode(
                requestBody["unlikedAdvID"],
                requestBody["unlikedAdvName"]
            )
            LikeRelationManager.removeLikeRelation(userNode, accomodationNode=unlikedAdv)
        elif(requestBody["destinationType"] == "activity"):
            unlikedAdv = ActivityNode(
                requestBody["unlikedAdvID"],
                requestBody["unlikedAdvName"]
            )
            LikeRelationManager.removeLikeRelation(userNode, activityNode=unlikedAdv)

        return "", 200
    except Exception as e:
        return str(e), 500

@application.route('/recommendations/<destination_type>', methods=['GET'])
@required_token
def getrecommendedAdvs(destination_type, user={}):
    try:
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        UserNodeManager.getRecommendedAdvs(userNode, destination_type)
        return "", 200
    except Exception as e:
        return str(e), 500

@application.route('/recommendations/user', methods=['GET'])
@required_token
def getRecommendedUsers(user={}):
    try:
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        UserNodeManager.getRecommendedUsers(userNode)
        return "", 200
    except Exception as e:
        return str(e), 500
@application.route('/user/following', methods=['POST'])
@required_token
def followUser(user={}):
    try:
        requestBody = request.json
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        followedUserNode = UserNode(
            requestBody["followedUserID"],
            requestBody["followedUsername"]
        )
        FollowRelationManager.addFollowRelation(userNode, followedUserNode)
        return "", 200
    except Exception as e:
        return str(e), 500

@application.route('/users/unfollowing', methods=['POST'])
@required_token
def unfollowUser(user={}):
    try:
        requestBody = request.json
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        unfollowedUserNode = UserNode(
            requestBody["unfollowedUserID"],
            requestBody["unfollowedUsername"]
        )
        FollowRelationManager.removeFollowRelation(userNode, unfollowedUserNode)
        return "", 200
    except Exception as e:
        return str(e), 500

@application.route('/users/liking/<destination_type>', methods=['GET'])
@required_token
def getLikedAdvsByUserID(destination_type, user={}):
    try:
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        UserNodeManager.getLikedAdvs(userNode, destination_type)
        return "", 200
    except Exception as e:
        return str(e), 500

@application.route('/users/liking', methods=['POST'])
@required_token
def likeAdv(user={}):
    try:
        requestBody = request.json
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        if(requestBody["destinationType"] == "accomodation"):
            likedAdv = AccomodationNode(
            requestBody["likedAdvID"],
            requestBody["likedAdvName"]
            )
            LikeRelationManager.addLikeRelation(userNode, accomodationNode=likedAdv)
        elif(requestBody["destinationType"] == "activity"):
            likedAdv = ActivityNode(
                requestBody["likedAdvID"],
                requestBody["likedAdvName"]
            )
            LikeRelationManager.addLikeRelation(userNode, activityNode=likedAdv)
        return "", 200
    except Exception as e:
        return str(e), 500

@application.route('/users/unliking', methods=['POST'])
@required_token
def unlikeAdv(user={}):
    try:
        requestBody = request.json
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        if(requestBody["destinationType"] == "accomodation"):
            unlikedAdv = AccomodationNode(
                requestBody["unlikedAdvID"],
                requestBody["unlikedAdvName"]
            )
            LikeRelationManager.removeLikeRelation(userNode, accomodationNode=unlikedAdv)
        elif(requestBody["destinationType"] == "activity"):
            unlikedAdv = ActivityNode(
                requestBody["unlikedAdvID"],
                requestBody["unlikedAdvName"]
            )
            LikeRelationManager.removeLikeRelation(userNode, activityNode=unlikedAdv)

        return "", 200
    except Exception as e:
        return str(e), 500

@application.route('/recommendations/<destination_type>', methods=['GET'])
@required_token
def getrecommendedAdvs(destination_type, user={}):
    try:
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        UserNodeManager.getRecommendedAdvs(userNode, destination_type)
        return "", 200
    except Exception as e:
        return str(e), 500

@application.route('/recommendations/user', methods=['GET'])
@required_token
def getRecommendedUsers(user={}):
    try:
        userNode = UserNode(
            user["_id"] ,
            user["username"]
        )
        UserNodeManager.getRecommendedUsers(userNode)
        return "", 200
    except Exception as e:
        return e, 500

@application.route('/book/activity', methods=['POST'])
@required_token
def bookActivity(user={}):
    requestBody = request.json
    activity = requestBody["activity"]
    startDate = dateparser.parse(requestBody["startDate"])
    city = activity["city"]
    hostID = activity["hostID"]
    reservation = Reservation(
        user['_id'], activity["_id"], "activity", startDate, activity["price"], city, hostID)
    try:
        reservationID = ReservationManager.book(reservation)
        reservation._id = reservationID
        ActivityManager.addReservation(reservation)
        return "OK", 200
    except Exception as e:
        return str(e), 500


@application.route('/reservations/<user_id>', methods=['GET'])
# @required_token
def getReservationsByUserID(user_id):
    userID = escape(user_id)
    try:
        result = ReservationManager.getReservationsByUser(userID)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route('/reservations/<reservation_id>', methods=['DELETE'])
@required_token
def deleteReservation(reservation_id, user={}):
    reservationID = escape(reservation_id)
    try:
        result = ReservationManager.deleteReservationByID(reservationID)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route('/accomodations', methods=['GET'])
#@required_token
def getAccomodations():
    args = request.args
    city = args.get("city")
    guests = args.get("guestsNumber")
    start_date = args.get("start_date")
    end_date = args.get("end_date")
    index = args.get("index")
    direction = args.get("direction")
    try:
        result = AccomodationsManager.getFilteredAccomodation(
            start_date, end_date, city, guests, index, direction)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route('/insert/accomodation', methods=['POST'])
@required_token
# TODO Da rivedere
def insertAccomodations(user={}):
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

    accomodation = Accomodation(
        formData["name"],
        formData["description"],
        pictures,
        host["_id"],
        host["name"],
        formData["img-0"],
        host["picture"],
        location,
        formData["propertyType"],
        formData["guests"],
        formData["bedrooms"],
        formData["beds"],
        formData["price"],
        formData["minimumNights"],
        0,
        0,
        False
    )
    try:
        accomodationID = AccomodationsManager.insertNewAccomodation(accomodation)
        if (user["role"]!= "host" and user["role"]!= "admin"):
            updatedRole = {"type": "host"}
            UserManager.updateUser(updatedRole, host["_id"])
        return {"accomodationID": str(accomodationID)}, 200
    except Exception as e:
        return str(e), 500


@application.route('/insert/activity', methods=['POST'])
@required_token
def insertActivity(user={}):
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
        [],
        formData["duration"],
        formData["price"],
        0,
        0,
        formData["img-0"],
        formData["category"],
        False
    )
    try:
        activityID = ActivityManager.insertNewActivity(activity)
        return {"activityID": str(activityID)}, 200
    except Exception as e:
        return str(e), 500


@application.route('/reviews/<review_id>', methods=['GET'])
# @required_token
def getReviewByID(review_id):
    reviewID = escape(review_id)
    try:
        result = ReviewManager.getReviewFromID(reviewID)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route('/reviewsByDestination/<destination_id>', methods=['GET'])
# @required_token
def getReviewByAd(destination_id):
    destinationID = escape(destination_id)
    try:
        result = ReviewManager.getReviewFromDestinationID(destinationID)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route('/reviews', methods=['PUT'])
@required_token
def insertReview(user={}):
    requestBody = request.json
    destinationType = requestBody["destinationType"]
    reviewer = requestBody["reviewer"]
    review = Review(user["_id"],
                    requestBody["destinationID"],
                    requestBody["score"],
                    requestBody["description"],
                    reviewer)
    try:
        insertedID = ReviewManager.insertNewReview(review)
        review._id = insertedID
        if (destinationType == "accomodation"):
            AccomodationsManager.addReview(review)
        elif (destinationType == "activity"):
            ActivityManager.addReview(review)
        return "", 200
    except Exception as e:
        return str(e), 200


@application.route('/reviews/<destinationType>/<destinationID>/<reviewID>', methods=['DELETE'])
@required_token
def deleteReviewByID(destinationType, destinationID, reviewID , user={}):
    reviewID = escape(reviewID)
    destinationType = escape(destinationType)
    destinationID = escape(destinationID)
    try:
        result = ReviewManager.deleteReview(reviewID, destinationID, destinationType, user)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route('/users/<user_id>', methods=['DELETE'])
@required_token
def deleteUserById(user_id, user={}):
    userId = escape(user_id)
    try:
        result = AdminManager.deleteUser(userId, user)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route('/users/<user_id>', methods=['GET'])
@required_token
def getUserById(user_id, user={}):
    userId = escape(user_id)
    try:
        result = UserManager.getUserFromId(userId)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route('/review/check/<destination_id>', methods=['GET'])
@required_token
def getIfCanReview(destination_id, user={}):
    destinationID = escape(destination_id)
    user = json.loads(request.headers.get('Authorization'))
    args = request.args
    destinationType = args["destinationType"]
    result = {"result": False}
    try:
        if ReviewManager.checkIfCanReview(str(destinationID), destinationType, user):
            result = {"result": True}
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route('/login', methods=['POST'])
# @required_token
def loginUser():
    username = request.json["username"]
    password = request.json["password"]
    try:
        userID, userType, name = UserManager.authenicateUser(
            username, password)
        return {"userID": userID, "role": userType, "name": name}, 200
    except Exception as e:
        return str(e), 500


@application.route('/signup', methods=['POST'])
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
    dbHash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
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
        datetime.today().replace(microsecond=0, second=0, hour=0, minute=0)
    )
    try:
        insertedID = UserManager.insertNewUser(user)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route('/users', methods=['GET'])
@required_token
def getUsers(user):
    args = request.args
    id = args.get("id")
    name = args.get("name")
    surname = args.get("surname")
    index = args.get("index")
    direction = args.get("direction")
    try:
        result = AdminManager.getFilteredUsers(
            user, id, name, surname, index, direction)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route('/admin/announcements/<destination_type>', methods=['GET'])
@required_token
def getAnnouncementsToBeApproved(destination_type , user={}):
    args = request.args
    index = args.get("index")
    direction = args.get("direction")
    try:
        result = AdminManager.getAnnouncementsToApprove(index, direction, destination_type)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route('/admin/announcement/<destination_type>/<announcementID>', methods=['GET'])
# @required_token
def getAnnouncementToBeApprovedByID(destination_type, announcementID):
    try:
        if (not (validateObjecID(announcementID))):
            return "Announcement non valido", 500
        result = AdminManager.getAnnouncementToApproveByID(announcementID, destination_type)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route('/admin/announcement/<announcementID>', methods=['POST'])
@required_token
def approveAnnouncement(announcementID, user={}):
    if (not (validateObjecID(announcementID))):
        return "Announcement non valido", 500
    try:
        requestBody = request.json
        destinationType = requestBody["destinationType"]
        AdminManager.approveAnnouncement(announcementID, user, destinationType)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route('/admin/announcement/<destination_type>/<announcementID>', methods=['DELETE'])
@required_token
def refuseAnnouncement(destination_type, announcementID, user={}):
    if (not (validateObjecID(announcementID))):
        return "Announcement non valido", 500
    try:
        if(destination_type == "accomodation"):
            AccomodationsManager.deleteAccomodation(announcementID, user)
        elif(destination_type == "activity"):
            ActivityManager.deleteActivity(announcementID, user)
        return "", 200
    except Exception as e:
        return str(e), 500


@application.route('/myadvacc/<user_id>', methods=['GET'])
# @required_token
def getAccomodationsByUserID(user_id):
    userID = escape(user_id)
    try:
        result = AccomodationsManager.getAccomodationsByUserID(userID)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route('/myadvact/<user_id>', methods=['GET'])
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
