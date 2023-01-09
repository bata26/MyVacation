from utility.connection import MongoManager
import os
from models.activity import Activity
from bson.objectid import ObjectId
from utility.serializer import Serializer
import dateparser

class ActivityManager:

    @staticmethod
    def getApprovedActivitiesID():
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]

        try:
            return collection.distinct("_id" , {"approved" : True})
        except Exception as e:
            raise Exception("Impossibile aggiornare: " + str(e))

    @staticmethod
    def updateActivity(activityID, activity,  user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]

        try:
            #print("pre edit")
            res = collection.update_one(
                {"_id": ObjectId(activityID)}, {"$set": activity})
            #print(res)
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
                    str(activity["hostID"]),
                    activity["hostName"],
                    activity["location"],
                    activity["description"],
                    activity["duration"],
                    activity["price"],
                    activity["mainPicture"],
                    activity["name"],
                    activity["approved"],
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
            str(cursor["hostID"]),
            cursor["hostName"],
            cursor["location"],
            cursor["description"],
            cursor["duration"],
            cursor["price"],
            cursor["mainPicture"],
            cursor["name"],
            cursor["approved"],
            cursor["reviews"],
            str(cursor["_id"]))
        return Serializer.serializeActivity(activity)

    @staticmethod
    def insertNewActivity(activity: Activity):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            result = collection.insert_one(activity.getDictToUpload())
            return result.inserted_id
        except Exception:
            raise Exception("Impossibile inserire")

    @staticmethod
    def deleteActivity(activityID, user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            activity = dict(collection.find_one({"_id": ObjectId(activityID)}, {"_id": 1, "hostID": 1}))
        except Exception as e:
            raise Exception(str(e))
            
        if (user['role'] != "admin" and str(activity["hostID"]) != user['_id']):
            raise Exception("L'utente non possiede l'activity")
        else:
            try:
                collection.delete_one({"_id": ObjectId(activityID)})
                return True
            except Exception:
                raise Exception("Impossibile eliminare")

    @staticmethod
    def getOccupiedActivities(start_date , reservation = ""):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]

        if not(isinstance(start_date, str) ):
            start_date = start_date.strftime("%Y-%m-%d")
        
        query = {"destinationType" : "activity" , "startDate": dateparser.parse(start_date)}
        if reservation != "":
            query["_id"] = {}
            query["_id"] = {"$ne" : ObjectId(reservation)}
        occupiedActivitiesID = collection.distinct("destinationId", query)
        return occupiedActivitiesID

    @staticmethod
    def getFilteredActivities(start_date="", city="", index="", direction=""):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        occupiedActivitiesID = []
        result = []
        query = {}

        if (city != "" and city is not None):
            query["location.city"] = city

        # Deve essere stato inserito il periodo di svolgimento
        if (start_date != "" and start_date is not None):
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
                str(activity["hostID"]),
                activity["hostName"],
                activity["location"],
                activity["description"],
                activity["duration"],
                activity["price"],
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
    def getActivityByUserID(userID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            cursor = list(collection.find({"hostID": ObjectId(userID)}))
            result = []
            for activity in cursor:
                activity = Activity(
                    str(activity["hostID"]),
                    activity["hostName"],
                    activity["location"],
                    activity["description"],
                    activity["duration"],
                    activity["price"],
                    activity["mainPicture"],
                    activity["name"],
                    activity["approved"],
                    activity["reviews"],
                    str(activity["_id"]))
                result.append(Serializer.serializeActivity(activity))
            return result
        except Exception as e:
            raise Exception("Impossibile ottenere prenotazioni: " + str(e))
