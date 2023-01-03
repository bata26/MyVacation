from .connection import MongoManager
import os
from models.activity import Activity
from bson.objectid import ObjectId
from utility.serializer import Serializer
import dateparser

class ActivityManager:

    @staticmethod
    def updateActivity(activityID, activity,  user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]

        try:
            print("pre edit")
            res = collection.update_one(
                {"_id": ObjectId(activityID)}, {"$set": activity})
            print(res)
        except Exception as e:
            raise Exception("Impossibile aggiornare: " + str(e))

    @staticmethod
    def getActivitiesFromIdList(activitiesIdList):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]

        idList = [ObjectId(item) for item in activitiesIdList]

        try:
            serializedActivities = []
            activitiesList = list(collection.find({"_id": {"$in": idList}}))
            
            for activity in activitiesList:
                activityObject = Activity(
                    str(activity["host_id"]),
                    activity["host_name"],
                    activity["location"],
                    activity["description"],
                    activity["duration"],
                    activity["price"],
                    activity["number_of_reviews"],
                    activity["review_scores_rating"],
                    activity["mainPicture"],
                    activity["name"],
                    activity["approved"],
                    activity["reservations"],
                    activity["reviews"],
                    str(activity["_id"]))
                serializedActivities.append(Serializer.serializeActivity(activityObject))
            return serializedActivities
        except Exception as e:
            raise Exception("Impossibile aggiornare: " + str(e))

    @staticmethod
    def getActivityFromID(activityID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        cursor = dict(collection.find_one({"_id": ObjectId(activityID)}))
        activity = Activity(
            str(cursor["host_id"]),
            cursor["host_name"],
            cursor["location"],
            cursor["description"],
            cursor["duration"],
            cursor["price"],
            cursor["number_of_reviews"],
            cursor["review_scores_rating"],
            cursor["mainPicture"],
            cursor["name"],
            cursor["approved"],
            cursor["reservations"],
            cursor["reviews"],
            str(cursor["_id"]))
        return Serializer.serializeActivity(activity)

    @staticmethod
    def insertNewActivity(activity):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            collection.insert_one(activity.getDictToUpload())
        except Exception:
            raise Exception("Impossibile inserire")

    @staticmethod
    def deleteActivity(activityID, user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            activity = dict(collection.find_one({"_id": ObjectId(activityID)}, {"_id": 1, "host_id": 1}))
        except Exception as e:
            raise Exception(str(e))
            
        if (user['role'] != "admin" and str(activity["host_id"]) != user['_id']):
            raise Exception("L'utente non possiede l'activity")
        else:
            try:
                collection.delete_one({"_id": ObjectId(activityID)})
                return True
            except Exception:
                raise Exception("Impossibile eliminare")

    @staticmethod
    def getOccupiedActivities(start_date):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]

        if not(isinstance(start_date, str) ):
            start_date = start_date.strftime("%Y-%m-%d")
        occupiedActivitiesID = collection.distinct("destinationId",{"destinationType" : "activity" , "startDate": dateparser.parse(start_date)})
        return occupiedActivitiesID

    @staticmethod
    def getFilteredActivity(start_date="", city="", guestNumbers="", index="", direction=""):
        query = {}
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        occupiedActivitiesID = []
        result = []

        if (city != ""):
            query["location.city"] = city
        if (guestNumbers != ""):
            query["accomodates"] = {}
            query["accomodates"]["$gte"] = guestNumbers

        # Deve essere stato inserito il periodo di svolgimento
        if (start_date != "" and start_date != None):
            collection = db[os.getenv("RESERVATIONS_COLLECTION")]
            occupiedActivitiesID = ActivityManager.getOccupiedActivities(start_date)
        query["_id"] = {}
        query["_id"]["$nin"] = occupiedActivitiesID
        projection = {
            "reservations": 0,
            "reviews": 0
        }
        query["approved"] = True
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        if index == "":
            # When it is first page
            activities = list(collection.find(query, projection).sort(
                '_id', 1).limit(int(os.getenv("PAGE_SIZE"))))
        else:
            if (direction == "next"):
                query["_id"]["$gt"] = ObjectId(index)
                activities = list(collection.find(query, projection).sort('_id', 1).limit(int(os.getenv("PAGE_SIZE"))))
            elif (direction == "previous"):
                query["_id"]["$lt"] = ObjectId(index)
                activities = list(collection.find(query, projection).sort('_id', -1).limit(int(os.getenv("PAGE_SIZE"))))

        for activity in activities:
            activityResult = Activity(
                str(activity["host_id"]),
                activity["host_name"],
                activity["location"],
                activity["description"],
                activity["duration"],
                activity["price"],
                activity["number_of_reviews"],
                activity["review_scores_rating"],
                activity["mainPicture"],
                activity["name"],
                activity["approved"],
                _id=str(activity["_id"]))
            result.append(Serializer.serializeActivity(activityResult))

        return result

    @staticmethod
    def addReview(review):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            collection.update_one({"_id": ObjectId(review.destinationID)}, {
                                  "$push": {"reviews": review.getDictForAdvertisement()}})
        except Exception as e:
            raise Exception("Impossibile aggiungere la review: " + str(e))

    @staticmethod
    def addReservation(reservation):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            collection.update_one({"_id": ObjectId(reservation.destinationID)}, {
                                  "$push": {"reservations": reservation.getDictForAdvertisement()}})
        except Exception as e:
            raise Exception("Impossibile aggiungere la reservation: " + str(e))

    @staticmethod
    def updateReservation(reservation, newStartDate):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            collection.update_one({"reservations._id": ObjectId(reservation['_id'])}, {"$set": {"reservations.$.startDate": dateparser.parse(newStartDate)}})
        except Exception as e:
            raise Exception("Impossibile aggiornare la reservation: " + str(e))

    @staticmethod
    def getActivityByUserID(userID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            cursor = list(collection.find({"host_id": ObjectId(userID)}))
            result = []
            for activity in cursor:
                activity = Activity(
                    str(activity["host_id"]),
                    activity["host_name"],
                    activity["location"],
                    activity["description"],
                    activity["duration"],
                    activity["number_of_reviews"],
                    activity["review_scores_rating"],
                    activity["price"],
                    activity["mainPicture"],
                    activity["name"],
                    activity["approved"],
                    activity["reservations"],
                    activity["reviews"],
                    str(activity["_id"]))
                result.append(Serializer.serializeActivity(activity))
            return result
        except Exception as e:
            raise Exception("Impossibile ottenere prenotazioni: " + str(e))
