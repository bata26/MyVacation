from .connection import MongoManager
import os
from models.accommodation import Accommodation
from bson.objectid import ObjectId
from utility.serializer import Serializer
from datetime import datetime
import dateparser
from models.review import Review


class AccommodationManager:
    @staticmethod
    def updateAccommodation(accommodationID, accommodation, user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]

        try:
            collection.update_one(
                {"_id": ObjectId(accommodationID)}, {"$set": accommodation}
            )
        except Exception as e:
            raise Exception("Impossibile aggiornare: " + str(e))

    @staticmethod
    def getAccommodationsFromIdList(accommodationsIdList):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        idList = [ObjectId(item) for item in accommodationsIdList]
        try:
            serializedAccommodations = []
            accommodationsList = list(
                collection.find({"_id": {"$in": idList}}, {"pictures": 0})
            )

            for accommodation in accommodationsList:
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
                serializedAccommodations.append(
                    Serializer.serializeAccommodation(accommodationObject)
                )
            return serializedAccommodations
        except Exception as e:
            raise Exception("Impossibile aggiornare: " + str(e))

    @staticmethod
    def getAccommodationFromId(accommodationID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
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
        # cursor["_id"] = str(cursor["_id"])
        # return cursor

    @staticmethod
    def getOccupiedAccommodationIDs(start_date, end_date):
        # ottengo una lista di id di accommodations non occupate
        # faccio una query per tutti gli id che non sono nella lista e che matchano per città e ospiti
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]
        if not (isinstance(start_date, str) and isinstance(end_date, str)):
            start_date = start_date.strftime("%Y-%m-%d")
            end_date = end_date.strftime("%Y-%m-%d")
        occupiedAccommodationsID = collection.distinct(
            "destinationID",
            {
                "destinationType": "accommodation",
                "$or": [
                    {
                        "$or": [
                            {
                                "$and": [
                                    {"startDate": {"$lte": dateparser.parse(end_date)}},
                                    {
                                        "startDate": {
                                            "$gte": dateparser.parse(start_date)
                                        }
                                    },
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
            },
        )
        return occupiedAccommodationsID

    # we can filter for:
    #   - start date
    #   - end date
    #   - city
    #   - number of guests
    @staticmethod
    def getFilteredAccommodation(
        start_date="", end_date="", city="", guestNumbers="", index="", direction=""
    ):
        query = {}
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        occupiedAccommodationsID = []
        result = []

        if city != "" and city != None:
            query["location.city"] = city
        if guestNumbers != "" and guestNumbers != None:
            query["accommodates"] = {}
            query["accommodates"]["$gte"] = int(guestNumbers)

        if (
            start_date != ""
            and end_date != ""
            and end_date != None
            and start_date != None
        ):
            # ottengo una lista di id di accommodations non occupate
            # faccio una query per tutti gli id che non sono nella lista e che matchano per città e ospiti
            occupiedAccommodationsID = AccommodationManager.getOccupiedAccommodationIDs(
                start_date, end_date
            )

        query["_id"] = {}
        query["_id"]["$nin"] = occupiedAccommodationsID
        projection = {"pictures": 0, "reservations": 0, "reviews": 0}
        query["approved"] = True
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]

        if index == "":
            # When it is first page
            accommodations = list(
                collection.find(query, projection)
                .sort("_id", 1)
                .limit(int(os.getenv("PAGE_SIZE")))
            )
        else:
            if direction == "next":
                query["_id"]["$gt"] = ObjectId(index)
                accommodations = list(
                    collection.find(query, projection)
                    .sort("_id", 1)
                    .limit(int(os.getenv("PAGE_SIZE")))
                )
            elif direction == "previous":
                query["_id"]["$lt"] = ObjectId(index)
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

    @staticmethod
    def insertNewAccommodation(accommodation):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        try:
            result = collection.insert_one(accommodation.getDictToUpload())
            return result.inserted_id
        except Exception:
            raise Exception("Impossibile inserire")

    @staticmethod
    def deleteAccommodation(accommodationID, user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]

        try:
            cursor = dict(
                collection.find_one(
                    {"_id": ObjectId(accommodationID)}, {"_id": 1, "hostID": 1}
                )
            )
        except Exception as e:
            raise (str(e))
        if str(cursor["hostID"]) != user["_id"] and user["role"] != "admin":
            raise Exception("L'utente non possiede l'accommodations")
        else:
            try:
                collection.delete_one({"_id": ObjectId(accommodationID)})
                return True
            except Exception:
                raise Exception("Impossibile eliminare")

    @staticmethod
    def addReview(review):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        try:
            collection.update_one(
                {"_id": ObjectId(review.destinationID)},
                {"$push": {"reviews": review.getDictForAdvertisement()}},
            )
        except Exception as e:
            raise Exception("Impossibile aggiungere la review: " + str(e))
    """
    @staticmethod
    def addReservation(reservation):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        try:
            collection.update_one(
                {"_id": ObjectId(reservation.destinationID)},
                {"$push": {"reservations": reservation.getDictForAdvertisement()}},
            )
        except Exception as e:
            raise Exception("Impossibile aggiungere la reservation: " + str(e))

    @staticmethod
    def updateReservation(reservation, newStartDate, newEndDate):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        prevStartDate = reservation["startDate"]
        prevEndDate = reservation["endDate"]
        prevTotalExpense = int(reservation["totalExpense"])
        price = prevTotalExpense / (
            (dateparser.parse(prevEndDate) - dateparser.parse(prevStartDate)).days
        )
        newNightNumber = (
            dateparser.parse(newEndDate) - dateparser.parse(newStartDate)
        ).days
        newTotalExpense = newNightNumber * price

        if str(
            reservation.destinationID
        ) in AccommodationManager.getOccupiedAccommodationIDs(newStartDate, newEndDate):
            raise Exception("Accommodation occupata")

        try:
            collection.update_one(
                {"reservations._id": ObjectId(reservation["_id"])},
                {
                    "$set": {
                        "reservations.$.startDate": dateparser.parse(newStartDate),
                        "reservations.$.endDate": dateparser.parse(newEndDate),
                        "reservations.$.totalExpense": newTotalExpense,
                    }
                },
            )
        except Exception as e:
            raise Exception("Impossibile aggiornare la reservation: " + str(e))
    """
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
            raise Exception("Impossibile ottenere prenotazioni: " + str(e))
