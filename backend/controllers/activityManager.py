from .connection import MongoManager
import os
from models.activity import Activity
from bson.objectid import ObjectId
from utility.serializer import Serializer

class ActivityManager:

    @staticmethod
    def getActivityFromID(activityID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        cursor = dict(collection.find_one({"_id" : ObjectId(activityID)}))
        activity = Activity(
            str(cursor["host_id"]) ,
            cursor["host_name"] ,
            cursor["location"] ,
            cursor["description"] ,
            cursor["reservations"] ,
            cursor["duration"] ,
            cursor["price"] ,
            cursor["number_of_reviews"] ,
            cursor["review_scores_rating"],
            cursor["mainPicture"],
            cursor["name"],
            cursor["reviews"] ,
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
    def deleteActivity(activityID , user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]

        if (user["type"] != "admin"):
            activity = collection.find_one({"_id" : ObjectId(activityID)})
            if(activity.host_id != user._id):
                raise Exception("L'utente non possiede l'activity")
        try:
            res = collection.delete_one({"_id" : ObjectId(activityID)})
            return res
        except Exception:
            raise Exception("Impossibile inserire")


    @staticmethod
    def getFilteredActivity(start_date = "" , city="" , guestNumbers="", index="", direction=""):
        query = {}
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        occupiedActivitiesID = []
        result = []

        if(city != ""):
            query["location.city"] = city
        if(guestNumbers != ""):
            query["accomodates"] = {}
            query["accomodates"]["$gte"] = guestNumbers
        
        # Deve essere stato inserito il periodo di svolgimento
        if(start_date != ""):
            collection = db[os.getenv("RESERVATIONS_COLLECTION")]
            occupiedActivitiesID = collection.distinct("destinationId" , 
                {"startDate" : start_date}
            )
        query["_id"] = {}
        query["_id"]["$nin"] = occupiedActivitiesID
        projection = {
            "reservations" : 0,
            "reviews" : 0
        }
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        if index == "":
            # When it is first page
            activities = list(collection.find(query , projection).sort('_id', 1).limit(int(os.getenv("PAGE_SIZE"))))
        else:
            if (direction == "next"):
                query["_id"]["$gt"] = ObjectId(index)
                activities = list(collection.find(query , projection).sort('_id', 1).limit(int(os.getenv("PAGE_SIZE"))))
            elif (direction == "previous"):
                query["_id"]["$lt"] = ObjectId(index)
                activities = list(collection.find(query , projection).sort('_id', -1).limit(int(os.getenv("PAGE_SIZE"))))

        for activity in activities:
            activityResult = Activity(
                str(activity["host_id"]) ,
                activity["host_name"] ,
                activity["location"] ,
                activity["description"] ,
                activity["duration"] ,
                activity["price"] ,
                activity["number_of_reviews"] ,
                activity["review_scores_rating"],
                activity["mainPicture"],
                activity["name"],
                _id=str(activity["_id"]))
            result.append(Serializer.serializeActivity(activityResult))

        return result
    
    @staticmethod
    def addReview(review):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            collection.update_one({"_id" : ObjectId(review.destinationID)} , {"$push" : {"reviews" : review.getDictForAdvertisement()}})
        except Exception as e:
            raise Exception("Impossibile aggiungere la review: " + str(e))
    
    @staticmethod
    def addReservation(reservation):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            collection.update_one({"_id" : ObjectId(reservation.destinationID)} , {"$push" : {"reservations" : reservation.getDictForAdvertisement()}})
        except Exception as e:
            raise Exception("Impossibile aggiungere la reservation: " + str(e))