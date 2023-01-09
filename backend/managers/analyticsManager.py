from utility.connection import MongoManager
import os
import datetime
from models.accommodation import Accommodation
from models.activity import Activity
from bson.objectid import ObjectId
from utility.serializer import Serializer
from managers.accommodationManager import AccommodationManager
from managers.activityManager import ActivityManager


class AnalyticsManager:
    @staticmethod
    def getReservationByMonth(user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]
        try:
            result = list(collection.aggregate(([
                {"$match": {"hostID": ObjectId(user["_id"])}},
                {"$group": {
                    "_id": {
                        "city": "$city",
                        "month": {"$month": "$startDate"}
                    },
                    "count": {"$count": {}}
                }},
                {"$project": {"total": "$count", "month": "$_id.month",
                              "_id": 0, "city": "$_id.city"}},
                {"$group": {
                    "_id": "$city",
                    "stats": {
                        "$push": {
                            "month": "$month",
                            "total": "$total"
                        }
                    }
                }},
                {"$project": {"_id": 0, "city": "$_id", "stats": "$stats"}}
            ])))
            return result
        except Exception as e:
            raise Exception("Impossibile eseguire la query: " + str(e))

    @staticmethod
    def getUsersForMonth():
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("USERS_COLLECTION")]
        year = datetime.datetime.now().year
        try:
            result = list(collection.aggregate([
                {"$match":
                 {"$expr":
                  {
                      "$eq": [{"$year": "$registrationDate"}, year]
                  }
                  }
                 },
                {
                    "$group": {
                        "_id": {"$month": "$registrationDate"},
                        "users": {
                            "$count": {}
                        }
                    }
                },
                {'$sort': {'users': -1}},
                {
                    "$project": {"month": "$_id", "users": "$users", "_id": 0}
                }]))
            return result
        except Exception as e:
            raise Exception("Impossibile ottenere: " + str(e))

    # Ottieni le tre città con più prenotazioni nell'ultimo mese (data da rivedere)
    @staticmethod
    def getTopCities():
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]
        month = datetime.datetime.now().month
        try:
            result = list(collection.aggregate([
                {"$match":
                 {"$expr":
                  {
                      "$eq": [{"$month": "$startDate"}, month]
                  }
                  }
                 },
                {"$group": {"_id": "$city", "count": {"$sum": 1}}},
                {"$sort": {"count": -1, "_id": 1}},
                {"$project": {"city": "$_id", "_id": 0}},
                {"$limit": 3}
            ]))
            return result
        except Exception as e:
            raise Exception("Impossibile ottenere: " + str(e))
            #print("impossibile ottenere: " + str(e))

    @staticmethod
    def getAccommodationAverageCost(user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        try:
            result = list(collection.aggregate([
                {"$group":
                 {
                     "_id": "$location.city",
                     "averageCost": {"$avg": "$price"}
                 }
                 },
                {'$sort': {'averageCost': -1}},
                {"$project": {"_id": 0, "city": "$_id", "averageCost": {"$round": ["$averageCost", 2]}}}

            ]))
            return result
        except Exception as e:
            raise Exception("Impossibile ottenere: " + str(e))
            #print("Impossibile eseguire la query: " + str(e))

    @staticmethod
    def getActivityAverageCost(user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            result = list(collection.aggregate([
                {"$group":
                 {
                     "_id": "$location.city",
                     "averageCost": {"$avg": "$price"}
                 }
                 },
                {'$sort': {'averageCost': -1}},
                {"$project": {"_id": 0, "city": "$_id", "averageCost": {"$round": ["$averageCost", 2]}}}

            ]))
            return result
        except Exception as e:
            raise Exception("Impossibile ottenere: " + str(e))
            #print("Impossibile eseguire la query: " + str(e))

    # Ottieni i tre annunci più prenotati di sempre
    @staticmethod
    def getTopAdv():
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]
        try:
            serializedAccommodations = []
            serializedActivities = []
            approvedAccommodations = AccommodationManager.getApprovedAccommodationsID()
            accommodationsResult = list(collection.aggregate([
                {"$match": {"destinationType": "accommodation" , "destinationID" : {"$in" : approvedAccommodations}}},
                {"$group": {"_id": "$destinationID", "count": {"$sum": 1}}},
                {"$sort": {"count": -1, "_id": 1}},
                {"$limit": 3},
                {"$project": {"count": 0}}
            ]))

            for accommodation in accommodationsResult:
                stringId = str(accommodation["_id"])
                accommodation["_id"] = stringId
                serializedAccommodations.append(accommodation)

            aprovedActivities = ActivityManager.getApprovedActivitiesID()
            activitiesResult = list(collection.aggregate([
                {"$match": {"destinationType": "activity" , "destinationID" : {"$in" : aprovedActivities}}},
                {"$group": {"_id": "$destinationID", "count": {"$sum": 1}}},
                {"$sort": {"count": -1, "_id": 1}},
                {"$limit": 3},
                {"$project": {"count": 0}}
            ]))

            for activity in activitiesResult:
                stringId = str(activity["_id"])
                activity["_id"] = stringId
                serializedActivities.append(activity)

            return {"accommodationsID": serializedAccommodations,
                    "activitiesID": serializedActivities}
        except Exception as e:
            raise Exception("Impossibile ottenere: " + str(e))

    @staticmethod
    def getTotReservations(user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]
        result = None
        try:
            if (user["role"] == "admin"):
                result = list(collection.aggregate([
                    {
                        '$count': 'totalReservation'
                    }
                ]))
            else:
                result = list(collection.aggregate([
                    {
                        '$match': {
                            'hostID': ObjectId(user["_id"])
                        }
                    }, {
                        '$count': 'totalReservation'
                    }
                ]))
            return result[0]
        except Exception as e:
            raise Exception("Impossibile eseguire la query: " + str(e))


    @staticmethod
    def getTotAdvs(user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        accommodationCollection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        activityCollection = db[os.getenv("ACTIVITIES_COLLECTION")]
        result = 0
        try:
            if (user["role"] == "admin"):
                resultAcc = list(accommodationCollection.aggregate([
                    {
                        '$count': 'totalAccommodations'
                    }
                ]))
                resultAct = list(activityCollection.aggregate([
                    {
                        '$count': 'totalActivities'
                    }
                ]))
            else:
                resultAcc = list(accommodationCollection.aggregate([
                    {
                        '$match': {
                            'hostID': ObjectId(user["_id"])
                        }
                    }, {
                        '$count': 'totalAccommodations'
                    }
                ]))
                resultAct = list(activityCollection.aggregate([
                    {
                        '$match': {
                            'hostID': ObjectId(user["_id"])
                        }
                    }, {
                        '$count': 'totalActivities'
                    }
                ]))
            result = {
                "totalAccommodations": resultAcc[0]["totalAccommodations"] , 
                "totalActivities": resultAct[0]["totalActivities"] 
            }
            return result
        except Exception as e:
            raise Exception("Impossibile ottenere: " + str(e))
            #print("Impossibile eseguire la query: " + str(e))
