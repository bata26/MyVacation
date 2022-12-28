from controllers.analyticsManager import AnalyticsManager
from controllers.accomodationsManager import AccomodationsManager
from flask import Flask, abort, request, jsonify, Response
from dotenv import load_dotenv
from markupsafe import escape
from controllers.activityManager import ActivityManager
from controllers.reviewManager import ReviewManager
from controllers.userManager import UserManager
from controllers.adminManager import AdminManager
from controllers.reservationManager import ReservationManager
from models.accomodation import Accomodation
from models.reservation import Reservation
from models.activity import Activity
from models.user import User
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


@application.route("/test", methods=["GET"])
@required_token
def testValidation(user={}):
    res = AnalyticsManager.getReservationByMonth(user)
    print(res)
    return "OK", 200


@application.route("/analytics/topcities", methods=["GET"])
@required_token
def getBestCities(user={}):
    try:
        res = AnalyticsManager.getTopCities()
        return res
    except Exception as e:
        return str(e), 500


@application.route("/analytics/topadv", methods=["GET"])
@required_token
def getBestAdv(user={}):
    try:
        res = AnalyticsManager.getTopAdv()
        return res
    except Exception as e:
        return str(e), 500


@application.route("/analytics/advinfo", methods=["GET"])
@required_token
def getBestAdvInfo(user={}):
    try:
        print(f"data: {request.data}")
        print(f"form: {request.form}")
        print(f"json: {request.json}")
        
        print("dentro")
        requestBody = request.json
        print("problemi")
        accomodationsID = requestBody["accomodationsID"]
        activitiesID = requestBody["activitiesID"]
        result = {}
        result["accomodations"] = AccomodationsManager.getAccomodationsFromIdList(accomodationsID)
        result["activities"] = ActivityManager.getActivitiesFromIdList(activitiesID)
        print(result)
        return result, 200
    except Exception as e:
        return str(e), 500


@application.route('/activities/<activity_id>', methods=['DELETE'])
@required_token
def deleteActivityByID(activity_id, user={}):
    activityID = escape(activity_id)
    result = ActivityManager.deleteActivity(activityID, user)
    return "", 200


@application.route('/activities/<activity_id>', methods=['GET'])
# @required_token
def getActivityByID(activity_id):
    activityID = escape(activity_id)
    result = ActivityManager.getActivityFromID(activityID)
    return result, 200


@application.route('/activities', methods=['GET'])
# @required_token
def getActivities(user={}):
    args = request.args
    city = args.get("city")
    guests = args.get("guests")
    start_date = args.get("startDate")
    index = args.get("index")
    direction = args.get("direction")
    result = ActivityManager.getFilteredActivity(
        start_date, city, guests, index, direction)
    return result, 200


@application.route('/accomodations/<accomodation_id>', methods=['DELETE'])
@required_token
def deleteAccomodationById(accomodation_id, user={}):
    accomodationId = escape(accomodation_id)
    result = AccomodationsManager.deleteAccomodation(accomodationId, user)
    return "", 200


@application.route('/edit/accomodations/<accomodationID>', methods=['POST'])
@required_token
def editAccomodationById(accomodationID, user={}):
    print("dentro")
    formData = dict(request.form)
    formData["location"] = {}
    formData["location"]["city"] = formData["city"]
    formData["location"]["address"] = formData["address"]
    formData["location"]["country"] = formData["country"]
    formData.pop("city")
    formData.pop("address")
    formData.pop("country")
    formData["approved"] = False
    result = AccomodationsManager.editAccomodation(
        accomodationID, formData, user)
    return "", 200


@application.route('/edit/activities/<activityID>', methods=['POST'])
@required_token
def editActivityById(activityID, user={}):
    formData = dict(request.form)
    formData["location"] = {}
    formData["location"]["city"] = formData["city"]
    formData["location"]["address"] = formData["address"]
    formData["location"]["country"] = formData["country"]
    formData.pop("city")
    formData.pop("address")
    formData.pop("country")
    formData["approved"] = False
    result = ActivityManager.editActivity(
        activityID, formData, user)
    return "", 200


@application.route('/accomodations/<accomodation_id>', methods=['GET'])
# @required_token
def getAccomodationById(accomodation_id):
    accomodationId = escape(accomodation_id)
    result = AccomodationsManager.getAccomodationFromId(accomodationId)
    return result, 200


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
        reservation._id = reservationID
        AccomodationsManager.addReservation(reservation)
        UserManager.addReservation(reservation)
        return "OK", 200
    except Exception as e:
        print("Errore: " + str(e))
        return str(e), 500


@application.route('/reservation/<reservation_id>', methods=['PATCH'])
@required_token
def updateReservation(reservation_id, user={}):
    requestBody = request.json
    type = requestBody["type"]
    startDate = requestBody["startDate"]
    destinationID = requestBody["destinationID"]
    endDate = None
    reservationID = escape(reservation_id)

    if (type == "accomodation"):
        endDate = requestBody["endDate"]

    try:
        ReservationManager.updateReservation(
            startDate, endDate, type, reservationID, destinationID)
        # se la update è andata bene, aggiorno anche la collection accomodation/activi
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
        print("Errore: " + str(e))
        return str(e), 500


@application.route('/reservations/<user_id>', methods=['GET'])
# @required_token
def getReservationsByUserID(user_id):
    userID = escape(user_id)
    result = ReservationManager.getReservationsByUser(userID)
    return result, 200


@application.route('/reservations/<reservation_id>', methods=['DELETE'])
# @required_token
def deleteReservation(reservation_id):
    reservationID = escape(reservation_id)
    global user
    result = ReservationManager.deleteReservationByID(reservationID)
    return result, 200


@application.route('/accomodations', methods=['GET'])
# @required_token
def getAccomodations():
    args = request.args
    city = args.get("city")
    guests = args.get("guestsNumber")
    start_date = args.get("start_date")
    end_date = args.get("end_date")
    index = args.get("index")
    direction = args.get("direction")
    result = AccomodationsManager.getFilteredAccomodation(
        start_date, end_date, city, guests, index, direction)
    return result, 200


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
    accomodationID = AccomodationsManager.insertNewAccomodation(accomodation)
    return {"accomodationID": str(accomodationID)}, 200
    return "", 500


@application.route('/insert/activity', methods=['POST'])
# @required_token
def insertActivity():
    global user
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
    activityID = ActivityManager.insertNewActivity(activity)
    return {"activityID": str(activityID)}, 200
    return "", 500


@application.route('/reviews/<review_id>', methods=['GET'])
# @required_token
def getReviewByID(review_id):
    reviewID = escape(review_id)
    result = ReviewManager.getReviewFromID(reviewID)
    return result, 200


@application.route('/reviewsByDestination/<destination_id>', methods=['GET'])
# @required_token
def getReviewByAd(destination_id):
    destinationID = escape(destination_id)
    result = ReviewManager.getReviewFromDestinationID(destinationID)
    return result, 200


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


@application.route('/reviews/<reviewID>', methods=['DELETE'])
@required_token
def deleteReviewByID(reviewID, user={}):
    reviewID = escape(reviewID)
    result = ReviewManager.deleteReview(reviewID, user)
    return "", 200


@application.route('/users/<user_id>', methods=['DELETE'])
@required_token
def deleteUserById(user_id, user={}):
    userId = escape(user_id)
    result = AdminManager.deleteUser(userId, user)
    return "", 200


@application.route('/users/<user_id>', methods=['GET'])
@required_token
def getUserById(user_id, user={}):
    userId = escape(user_id)
    result = UserManager.getUserFromId(userId)
    return result, 200


@application.route('/review/check/<destination_id>', methods=['GET'])
@required_token
def getIfCanReview(destination_id, user={}):
    destinationID = escape(destination_id)
    user = json.loads(request.headers.get('Authorization'))
    args = request.args
    destinationType = args["destinationType"]
    print(f"sto controllando se posso recensire")
    print(f"user dentro getIFCanReview: {user}")
    #global user
    result = {"result": False}
    if ReviewManager.checkIfCanReview(str(destinationID), destinationType, user):
        result = {"result": True}
    return result, 200


@application.route('/login', methods=['POST'])
# @required_token
def loginUser():
    username = request.json["username"]
    password = request.json["password"]
    print(f"username : {username}")
    print(f"password : {password}")
    try:
        userID, userType, name = UserManager.authenicateUser(
            username, password)
        return {"userID": userID, "role": userType, "name": name}, 200
    except Exception as e:
        return str(e), 500


@application.route('/signup', methods=['POST'])
# @required_token
def signUp():
    # print(request.)
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
        datetime.strptime(dateOfBirth, "%Y-%m-%dT%H:%M:%S.%f%z"),
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
    print(f"user : {user}")
    result = AdminManager.getFilteredUsers(
        user, id, name, surname, index, direction)
    return result, 200


@application.route('/admin/announcements/<destination_type>', methods=['GET'])
# @required_token
def getAnnouncementsToBeApproved(destination_type):
    try:
        print("DEBUG12")
        args = request.args
        index = args.get("index")
        direction = args.get("direction")
        print(f"destinationType:{destination_type}")
        result = AdminManager.getAnnouncementsToApprove(index, direction, destination_type)
        return result, 200
    except Exception as e:
        return e, 500


@application.route('/admin/announcement/<destination_type>/<announcementID>', methods=['GET'])
# @required_token
def getAnnouncementToBeApprovedByID(destination_type, announcementID):
    try:
        if (not (validateObjecID(announcementID))):
            return "Announcement non valido", 500
        print(announcementID)

        print(f"DDDDDDDD:{destination_type}")
        result = AdminManager.getAnnouncementToApproveByID(announcementID, destination_type)
        return result, 200
    except Exception as e:
        return e, 500


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
        return e, 500


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
        return e, 500


@application.route('/myadvacc/<user_id>', methods=['GET'])
# @required_token
def getAccomodationsByUserID(user_id):
    userID = escape(user_id)
    result = AccomodationsManager.getAccomodationsByUserID(userID)
    return result, 200


@application.route('/myadvact/<user_id>', methods=['GET'])
# @required_token
def getActivitiesByUserID(user_id):
    userID = escape(user_id)
    result = ActivityManager.getActivityByUserID(userID)
    return result, 200


if __name__ == "__main__":

    application.run(threaded=True, debug=True, use_reloader=True)
