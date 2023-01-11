from utility.connection import MongoManager
import os
from models.activity import Activity
from bson.objectid import ObjectId
from utility.serializer import Serializer
import dateparser

# This class represents the manager for the activity entity contained in MongoDB.
# Methods implements query and serialization of object.
class ActivityManager:

    # return a list of objectId of activities that are approved
    @staticmethod
    def getApprovedActivitiesID():
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]

        try:
            return collection.distinct("_id" , {"approved" : True})
        except Exception as e:
            raise Exception("Impossibile aggiornare: " + str(e))
    
    # update an activity
    @staticmethod
    def updateActivity(activityID, activity,  user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]

        try:
            collection.update_one(
                {"_id": ObjectId(activityID)}, {"$set": activity})
        except Exception as e:
            raise Exception("Impossibile aggiornare: " + str(e))
    
    # return a list of activity from a list of objectId
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
    
    # return an activity from the id of it
    @staticmethod
    def getActivityFromID(activityID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
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
        except Exception as e:
            raise Exception("Impossibile ottenere: " + str(e))

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
        reservationCollection = db[os.getenv("RESERVATIONS_COLLECTION")]
        userCollection = db[os.getenv("USERS_COLLECTION")]
        reviewCollection = db[os.getenv("REVIEW_COLLECTION")]

        try:
            activity = dict(collection.find_one({"_id": ObjectId(activityID)}, {"_id": 1, "hostID": 1}))
        except Exception as e:
            raise Exception(str(e))
            
        if (user['role'] != "admin" and str(activity["hostID"]) != user['_id']):
            raise Exception("L'utente non possiede l'activity")
        else:
            try:
                # transaction to delete and update all documents connected to the activity that we are going to delete:
                # - delete all reservation made for the activity from the reservation collection
                # - remove from nested array in users collection all the reservations made for the activity
                # - delete all reviews for the activity
                with client.start_session() as session:
                    with session.start_transaction():
                        collection.delete_one({"_id": ObjectId(activityID)} , session=session)
                        reservationCollection.delete_many({"destinationID" : ObjectId(activityID)} , session=session)
                        userCollection.update_many({"_id" : ObjectId(user["_id"])} , {"$pull" : {"reservations" : {"destinationID" : ObjectId(activityID)}}} , session=session)
                        reviewCollection.delete_many({"destinationID" : ObjectId(activityID)}, session=session)
                return True
            except Exception:
                raise Exception("Impossibile eliminare")

    # return a list of activity's id that are not available for a specific date 
    # it also take a reservationID in case the user want to update his reservation otherwise 
    # it could throw error
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

    # return a list of available activies based on parameters setted by the user
    @staticmethod
    def getFilteredActivities(start_date="", city="", index="", direction=""):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        occupiedActivitiesID = []
        result = []
        query = {}
        dateSetted = False

        if (city != "" and city is not None):
            query["location.city"] = city

        if (start_date != "" and start_date is not None):
            dateSetted = True
            occupiedActivitiesID = ActivityManager.getOccupiedActivities(start_date)
            # with pagination we have to do a double condition on _id field
            if(index != ""):
                query["$and"] = [{} , {}]
                query["$and"][0] = {"_id" : {"$nin" : occupiedActivitiesID}}
            else:
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
                if not(dateSetted):
                    query["_id"] = {}
                    query["_id"]["$gt"] = ObjectId(index)
                else:
                    query["$and"][1] = {"_id" : {"$gt" : ObjectId(index)}}


                activities = list(collection.find(query, projection).sort('_id', 1).limit(int(os.getenv("PAGE_SIZE"))))
            elif (direction == "previous"):
                if not(dateSetted):
                    query["_id"] = {}
                    query["_id"]["$lt"] = ObjectId(index)
                else:
                    query["$and"][1] = {"_id" : {"$lt" : ObjectId(index)}}

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

    # return a list of activities hosted by a specific user
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


    @staticmethod
    def getActivitiesIDListByUserID(userID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            cursor = list(collection.distinct( "_id" , {"hostID": ObjectId(userID)}))
            return cursor
        except Exception as e:
            raise Exception("Impossibile ottenere: " + str(e))