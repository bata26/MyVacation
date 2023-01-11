from utility.connection import MongoManager
import os
from models.accommodation import Accommodation
from bson.objectid import ObjectId
from utility.serializer import Serializer
import dateparser

# This class represents the manager for the accommodation entity contained in MongoDB.
# Methods implements query and serialization of object.
class AccommodationManager:
    
    # return a list of objectId of accommodations that are approved
    @staticmethod
    def getApprovedAccommodationsID():
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]

        try:
            return collection.distinct("_id" , {"approved" : True})
        except Exception as e:
            raise Exception("Impossibile aggiornare: " + str(e))

    # update an accommodation
    @staticmethod
    def updateAccommodation(accommodationID, accommodation, user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]

        try:
            collection.update_one({"_id": ObjectId(accommodationID)}, {"$set": accommodation})
        except Exception as e:
            raise Exception("Impossibile aggiornare: " + str(e))

    # return a list of accommodation from a list of objectId
    @staticmethod
    def getAccommodationsFromIdList(accommodationsIdList):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        idList = [ObjectId(item) for item in accommodationsIdList]
        try:
            serializedAccommodations = []
            accommodationsList = list(collection.find({"_id": {"$in": idList}}, {"pictures": 0}))

            for accommodation in accommodationsList:
                # create an accommodation object
                accommodationObject = Accommodation(
                    accommodation["name"],
                    accommodation["description"],
                    str(accommodation["hostID"]),
                    accommodation["hostName"],
                    accommodation["mainPicture"],
                    accommodation["location"],
                    accommodation["propertyType"],
                    accommodation["guests"],
                    accommodation["bedrooms"],
                    accommodation["beds"],
                    accommodation["price"],
                    accommodation["approved"],
                    accommodation["reviews"],
                    _id=str(accommodation["_id"]),
                )
                # serialize the object and prepare the response
                serializedAccommodations.append(Serializer.serializeAccommodation(accommodationObject))
            return serializedAccommodations
        except Exception as e:
            raise Exception("Impossibile aggiornare: " + str(e))

    # return an accommodation from the id of it
    @staticmethod
    def getAccommodationFromId(accommodationID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        try:
            cursor = dict(collection.find_one({"_id": ObjectId(accommodationID)}))
            accommodation = Accommodation(
                cursor["name"],
                cursor["description"],
                str(cursor["hostID"]),
                cursor["hostName"],
                cursor["mainPicture"],
                cursor["location"],
                cursor["propertyType"],
                cursor["guests"],
                cursor["bedrooms"],
                cursor["beds"],
                cursor["price"],
                cursor["approved"],
                cursor["reviews"],
                _id=str(cursor["_id"]),
                pictures=cursor["pictures"],
            )
            return Serializer.serializeAccommodation(accommodation)
        except Exception as e:
            raise Exception("Impossibile ottenere: " + str(e))
    
    # return a list of accommodation's id that are not available for a specific date range
    # it also take a reservationID in case the user want to update his reservation otherwise 
    # it could throw error
    @staticmethod
    def getOccupiedAccommodationIDs(start_date, end_date , reservationID = ""):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]
        if not (isinstance(start_date, str) and isinstance(end_date, str)):
            start_date = start_date.strftime("%Y-%m-%d")
            end_date = end_date.strftime("%Y-%m-%d")
        query = {
                "destinationType": "accommodation",
                "$or": [
                    {
                        "$or": [
                            {
                                "$and": [
                                    {"startDate": {"$lte": dateparser.parse(end_date)}},
                                    {"startDate": {"$gte": dateparser.parse(start_date)}},
                                ]
                            },
                            {
                                "$and": [
                                    {"endDate": {"$lte": dateparser.parse(end_date)}},
                                    {"endDate": {"$gte": dateparser.parse(start_date)}},
                                ]
                            },
                        ]
                    },
                    {
                        "$and": [
                            {"startDate": {"$lte": dateparser.parse(start_date)}},
                            {"endDate": {"$gte": dateparser.parse(end_date)}},
                        ]
                    },
                ],
            }
        if(reservationID != ""):
            query["_id"] = {}
            query["_id"] = {"$ne": ObjectId(reservationID)}
        occupiedAccommodationsID = collection.distinct(
            "destinationID",
            query,
        )
        return occupiedAccommodationsID

    # return a list of accommodations filtered by paramaters setted by the user. It also manages the pagination response
    @staticmethod
    def getFilteredAccommodations(start_date="", end_date="", city="", guestNumbers="", index="", direction=""):
        query = {}
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        occupiedAccommodationsID = []
        result = []
        dateSetted = False

        if city != "" and city is not None:
            query["location.city"] = city
        if guestNumbers != "" and guestNumbers is not None:
            query["guests"] = {}
            query["guests"]["$gte"] = int(guestNumbers)

        if ( start_date != "" and end_date != "" and end_date is not None and start_date is not None):
            dateSetted = True
            occupiedAccommodationsID = AccommodationManager.getOccupiedAccommodationIDs(start_date, end_date)
            
            # with pagination we have to do a double condition on _id field
            if(index != ""):
                query["$and"] = [{} , {}]
                query["$and"][0] = {"_id" : {"$nin" : occupiedAccommodationsID}}
            else:
                query["_id"] = {}
                query["_id"]["$nin"] = occupiedAccommodationsID

        projection = {"pictures": 0, "reservations": 0, "reviews": 0}
        query["approved"] = True
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        accommodations = []

        # first page
        if index == "":
            accommodations = list(
                collection.find(query, projection)
                .sort("_id", 1)
                .limit(int(os.getenv("PAGE_SIZE")))
            )
        else:
            if direction == "next":
                if not(dateSetted):
                    query["_id"] = {}
                    query["_id"]["$gt"] = ObjectId(index)
                else:
                    query["$and"][1] = {"_id" : {"$gt" : ObjectId(index)}}

                accommodations = list(
                    collection.find(query, projection)
                    .sort("_id", 1)
                    .limit(int(os.getenv("PAGE_SIZE")))
                )
            elif direction == "previous":
                if not(dateSetted):
                    query["_id"] = {}
                    query["_id"]["$lt"] = ObjectId(index)
                else:
                    query["$and"][1] = {"_id" : {"$lt" : ObjectId(index)}}

                accommodations = list(
                    collection.find(query, projection)
                    .sort("_id", -1)
                    .limit(int(os.getenv("PAGE_SIZE")))
                )
        for accommodation in accommodations:
            accommodationResult = Accommodation(
                accommodation["name"],
                accommodation["description"],
                str(accommodation["hostID"]),
                accommodation["hostName"],
                accommodation["mainPicture"],
                accommodation["location"],
                accommodation["propertyType"],
                accommodation["guests"],
                accommodation["bedrooms"],
                accommodation["beds"],
                accommodation["price"],
                accommodation["approved"],
                _id=str(accommodation["_id"]),
            )
            result.append(Serializer.serializeAccommodation(accommodationResult))
        return result

    # create a new accommodation
    @staticmethod
    def insertNewAccommodation(accommodation: Accommodation):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        try:
            result = collection.insert_one(accommodation.getDictToUpload())
            return result.inserted_id
        except Exception:
            raise Exception("Impossibile inserire")

    # delete an accommodation
    @staticmethod
    def deleteAccommodation(accommodationID, user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        reservationCollection = db[os.getenv("RESERVATIONS_COLLECTION")]
        userCollection = db[os.getenv("USERS_COLLECTION")]
        reviewCollection = db[os.getenv("REVIEW_COLLECTION")]

        try:
            cursor = dict(collection.find_one({"_id": ObjectId(accommodationID)}, {"_id": 1, "hostID": 1}))
        except Exception as e:
            raise (str(e))
        if str(cursor["hostID"]) != user["_id"] and user["role"] != "admin":
            raise Exception("L'utente non possiede l'accommodations")
        else:
            try:
                # transaction to delete and update all documents connected to the accommodation that we are going to delete:
                # - delete all reservation made for the accommodation from the reservation collection
                # - remove from nested array in users collection all the reservations made for the accommodation
                # - delete all reviews for the accommodation
                with client.start_session() as session:
                    with session.start_transaction():
                        collection.delete_one({"_id": ObjectId(accommodationID)}, session=session)
                        reservationCollection.delete_many({"destinationID" : ObjectId(accommodationID)}, session=session)
                        userCollection.update_many({"_id" : ObjectId(user["_id"])} , {"$pull" : {"reservations" : {"destinationID" : ObjectId(accommodationID)}}}, session=session)
                        reviewCollection.delete_many({"destinationID" : ObjectId(accommodationID)}, session=session)
                return True
            except Exception:
                raise Exception("Impossibile eliminare")
    
    # return a list of accommodations hosted by a specific user
    @staticmethod
    def getAccommodationsByUserID(userID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        try:
            cursor = list(collection.find({"hostID": ObjectId(userID)}))
            result = []
            for accommodation in cursor:
                accommodationResult = Accommodation(
                    accommodation["name"],
                    accommodation["description"],
                    str(accommodation["hostID"]),
                    accommodation["hostName"],
                    accommodation["mainPicture"],
                    accommodation["location"],
                    accommodation["propertyType"],
                    accommodation["guests"],
                    accommodation["bedrooms"],
                    accommodation["beds"],
                    accommodation["price"],
                    accommodation["approved"],
                    accommodation["reviews"],
                    str(accommodation["_id"]),
                    accommodation["pictures"],
                )
                result.append(Serializer.serializeAccommodation(accommodationResult))
            return result
        except Exception as e:
            raise Exception("Impossibile ottenere: " + str(e))
    
    @staticmethod
    def getAccommodationsIDListByUserID(userID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        try:
            cursor = list(collection.distinct( "_id" , {"hostID": ObjectId(userID)}))
            return cursor
        except Exception as e:
            raise Exception("Impossibile ottenere: " + str(e))
        
