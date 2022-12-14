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
from models.accomodationReservation import AccomodationReservation
from models.activityReservation import ActivityReservation
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

user = {
    "_id": "637ce1a04ed62608566c5fa7"
}

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
def testValidation():
    return "OK", 200


@application.route('/activities/<activity_id>', methods=['DELETE'])
# @required_token
def deleteActivityByID(activity_id):
    activityID = escape(activity_id)
    user = {
        "type": "admin"
    }
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
def getActivities():
    args = request.args
    city = args.get("city")
    guests = args.get("guests")
    start_date = args.get("start_date")
    index = args.get("index")
    direction = args.get("direction")
    print("sono nella activities")
    result = ActivityManager.getFilteredActivity(
        start_date, city, guests, index, direction)
    return result, 200


@application.route('/accomodations/<accomodation_id>', methods=['DELETE'])
@required_token
def deleteAccomodationById(accomodation_id):
    accomodationId = escape(accomodation_id)
    user = {
        "type": "admin"
    }
    result = AccomodationsManager.deleteAccomodation(accomodationId, user)
    return "", 200


@application.route('/accomodations/<accomodation_id>', methods=['GET'])
# @required_token
def getAccomodationById(accomodation_id):
    accomodationId = escape(accomodation_id)
    result = AccomodationsManager.getAccomodationsFromId(accomodationId)
    print(f"res : {result['_id']}")
    return result, 200


@application.route('/book/accomodation', methods=['POST'])
@required_token
def bookAccomodation(user={}):
    requestBody = request.json
    accomodation = requestBody["accomodation"]
    startDatetime = dateparser.parse(requestBody["startDate"])
    endDatetime = dateparser.parse(requestBody["endDate"])
    nightNumber = (((endDatetime - startDatetime).days) - 1)
    totalExpense = nightNumber*accomodation["price"]
    reservation = AccomodationReservation(user["_id"] , accomodation["_id"] , "accomodation" , startDatetime , endDatetime , totalExpense)
    
    try:
        reservationID = ReservationManager.book(reservation)
        reservation._id = reservationID
        AccomodationsManager.addReservation(reservation)
        return "OK" , 200 
    except Exception as e:
        print("Errore: " + str(e))
        return str(e) , 500


@application.route('/book/activity', methods=['POST'])
@required_token
def bookActivity(user={}):
    requestBody = request.json
    activity = requestBody["activity"]
    startDate = dateparser.parse(requestBody["startDate"])
    reservation = ActivityReservation(user["_id"] , activity["_id"] , "accomodation" , startDate , activity["price"])

    try:
        reservationID = ReservationManager.book(reservation)
        reservation._id = reservationID
        ActivityManager.addReservation(reservation)
        return "OK" , 200 
    except Exception as e:
        print("Errore: " + str(e))
        return str(e) , 500


@application.route('/reservations', methods=['GET'])
@required_token
def getReservationsByUserID(user={}):
    #global user
    result = ReservationManager.getReservationsByUser(user["_id"])
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
    print(f"city : {city}")
    print(f"guests : {guests}")
    print(f"start_date : {start_date}")
    print(f"end_date : {end_date}")
    print(f"index : {index}")
    print(f"direction : {direction}")
    result = AccomodationsManager.getFilteredAccomodation(
        start_date, end_date, city, guests, index, direction)
    return result, 200


@application.route('/insert/accomodation', methods=['POST'])
# @required_token
#TODO Da rivedere
def insertAccomodation():
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


@application.route('/reviews', methods=['PUT'])
@required_token
def insertReview(user={}):
    requestBody = request.json
    destinationType = requestBody["destinationType"]
    review = Review(user["_id"],
                    requestBody["destinationID"],
                    requestBody["score"],
                    requestBody["description"])
    print("nell'endpoint")
    
    try:
        insertedID = ReviewManager.insertNewReview(review)
        review._id = insertedID
        print(f"inserito id : {insertedID}")
        if(destinationType == "accomodation"):
            print("sto gestendo una accomodation")
            AccomodationsManager.addReview(review)
        elif(destinationType == "activity"):
            print("sto gestendo una activity")
            ActivityManager.addReview(review)
        return "", 200
    except Exception as e:
        return str(e), 200


@application.route('/reviews/<review_id>', methods=['DELETE'])
# @required_token
def deleteReviewByID(reviewID):
    reviewID = escape(reviewID)
    user = {
        "type": "admin"
    }
    result = ReviewManager.deleteReview(reviewID, user)
    return "", 200


@application.route('/users/<user_id>', methods=['DELETE'])
# @required_token
def deleteUserById(user_id):
    userId = escape(user_id)
    user = {
        "type": "admin"
    }
    result = AdminManager.deleteUser(userId, user)
    return "", 200


@application.route('/users/<user_id>', methods=['GET'])
# @required_token
def getUserById(user_id):
    userId = escape(user_id)
    result = UserManager.getUserFromId(userId)
    return result, 200


@application.route('/review/check/<destination_id>', methods=['GET'])
@required_token
def getIfCanReview(destination_id, user={}):
    destinationID = escape(destination_id)
    #user = json.loads(request.headers.get('Authorization'))
    print(user)
    #global user
    result = {"result": False}
    if ReviewManager.checkIfCanReview(str(destinationID), user):
        result = {"result": True}
    return result, 200


@application.route('/login', methods=['POST'])
# @required_token
def loginUser():
    # print(request.)
    username = request.json["username"]
    password = request.json["password"]
    print(f"username : {username}")
    print(f"password : {password}")
    try:
        userID, userType = UserManager.authenicateUser(username, password)
        return {"userID": userID, "role": userType}, 200
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
    print(f"username : {username}")
    print(f"password : {password}")
    print(f"name : {name}")
    print(f"surname : {surname}")
    print(f"gender : {gender}")
    print(f"dateOfBirth : {dateOfBirth}")
    print(f"nationality : {nationality}")
    print(f"knownLanguages : {knownLanguages}")

    user = User(
        username,
        password,
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
    print("nell'endpoint")
    try:
        insertedID = UserManager.insertNewUser(user)
        print(f"inserito id : {insertedID}")
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
    result = UserManager.getFilteredUsers(
        user, id, name, surname, index, direction)
    return result, 200


@application.route('/admin/announcements', methods=['GET'])
# @required_token
def getAnnouncementToBeApproved():
    try:
        args = request.args
        index = args.get("index")
        direction = args.get("direction")
        result = AdminManager.getAnnouncementToApprove(index, direction)
        return result, 200
    except Exception as e:
        return e, 500


@application.route('/admin/announcements/<announcementID>', methods=['POST'])
# @required_token
def approveAnnouncement(announcementID):
    if (not (validateObjecID(announcementID))):
        return "Announcement non valido", 500
    try:
        AdminManager.approveAnnouncement(announcementID)
        return "", 200
    except Exception as e:
        return e, 500


if __name__ == "__main__":

    application.run(threaded=True, debug=True, use_reloader=True)
