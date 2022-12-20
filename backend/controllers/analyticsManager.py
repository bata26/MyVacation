from .connection import MongoManager
import os
import datetime
class AnalyticsManager:
    
    @staticmethod
    def getUsersForMonth():
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("USERS_COLLECTION")]
        year = datetime.datetime.now().year
        try:
            result = list(collection.aggregate([
                        {"$match" : 
                            { "$expr":
                                {
                                    "$eq" : [{"$year" : "$registrationDate"} , year]
                                }
                            }
                        },
                        {
                            "$group" : {
                                "_id" : {"$month" : "$registrationDate"},
                                "users" : {
                                    "$count" : {}
                                }
                            }
                        },
                        {
                            "$project" : {"month" : "$_id" , "users" : "$users" , "_id" : 0}
                        }]))

            print(result)
        except Exception as e:
            raise Exception("Impossibile ottenere: " + str(e))


    # Ottieni i tre annunci più prenotati di sempre
    @staticmethod
    def getTopAdv():
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        accomodationsCollection = db[os.getenv("ACCOMODATIONS_COLLECTION")]
        activitiesCollection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:

            accomodationsResult = list(accomodationsCollection.aggregate([
                {"$group" : {"_id" : "$reservations", "count" : {"$sum" : 1}}},
                {"$sort" : {"count" : -1}},
                {"$limit": 3}
                ]))
            
            activitiesResult = list(activitiesCollection.aggregate([
                {"$group" : {"_id" : "$reservations", "count" : {"$sum" : 1}}},
                {"$sort" : {"count" : -1}},
                {"$limit": 3}
                ]))
                
            print(accomodationsResult)
            print(activitiesResult)

        except Exception as e:
            raise Exception("Impossibile ottenere: " + str(e))

    # Ottieni le tre città con più prenotazioni nell'ultimo mese (data da rivedere)
    @staticmethod
    def getTopCities():
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]
        try:

            result = list(collection.aggregate([
                {"$match" : {"startDate": {
                    "$gte": datetime(2022, 12, 1, 0, 0, 0, tzinfo=timezone.utc), 
                    "$lt": datetime(2022, 12, 31, 0, 0, 0, tzinfo=timezone.utc)
                }}},
                {"$group" : {"_id" : "$city", "count" : {"$sum" : 1}}},
                {"$sort" : {"count" : -1}},
                {"$limit": 3}
                ]))
                
            print(result)

        except Exception as e:
            raise Exception("Impossibile ottenere: " + str(e))