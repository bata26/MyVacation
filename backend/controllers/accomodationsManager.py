from .connection import MongoManager
import os
from models.accomodation import Accomodation
from bson.objectid import ObjectId
from utility.serializer import Serializer
from datetime import datetime
import dateparser
from models.review import Review


class AccomodationsManager:
    @staticmethod
    def updateAccomodation(accomodationID, accomodation, user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]

        try:
            collection.update_one(
                {"_id": ObjectId(accomodationID)}, {"$set": accomodation}
            )
        except Exception as e:
            raise Exception("Impossibile aggiornare: " + str(e))

    @staticmethod
    def getAccomodationsFromIdList(accomodationsIdList):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]
        idList = [ObjectId(item) for item in accomodationsIdList]
        try:
            serializedAccomodations = []
            accomodationsList = list(
                collection.find({"_id": {"$in": idList}}, {"pictures": 0})
            )

            for accomodation in accomodationsList:
                accomodationObject = Accomodation(
                    accomodation["name"],
                    accomodation["description"],
                    str(accomodation["host_id"]),
                    accomodation["host_name"],
                    accomodation["mainPicture"],
                    accomodation["location"],
                    accomodation["property_type"],
                    accomodation["accommodates"],
                    accomodation["bedrooms"],
                    accomodation["beds"],
                    accomodation["price"],
                    accomodation["minimum_nights"],
                    accomodation["number_of_reviews"],
                    accomodation["review_scores_rating"],
                    accomodation["approved"],
                    accomodation["reservations"],
                    accomodation["reviews"],
                    str(accomodation["_id"]),
                )
                serializedAccomodations.append(
                    Serializer.serializeAccomodation(accomodationObject)
                )
            return serializedAccomodations
        except Exception as e:
            raise Exception("Impossibile aggiornare: " + str(e))

    @staticmethod
    def getAccomodationFromId(accomodationID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]
        cursor = dict(collection.find_one({"_id": ObjectId(accomodationID)}))
        accomodation = Accomodation(
            cursor["name"],
            cursor["description"],
            str(cursor["host_id"]),
            cursor["host_name"],
            cursor["mainPicture"],
            cursor["location"],
            cursor["property_type"],
            cursor["accommodates"],
            cursor["bedrooms"],
            cursor["beds"],
            cursor["price"],
            cursor["minimum_nights"],
            cursor["number_of_reviews"],
            cursor["review_scores_rating"],
            cursor["approved"],
            cursor["reservations"],
            cursor["reviews"],
            str(cursor["_id"]),
            cursor["pictures"],
        )
        return Serializer.serializeAccomodation(accomodation)
        # cursor["_id"] = str(cursor["_id"])
        # return cursor

    @staticmethod
    def getOccupiedAccomodationIDs(start_date, end_date):
        # ottengo una lista di id di accomodations non occupate
        # faccio una query per tutti gli id che non sono nella lista e che matchano per città e ospiti
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]
        if not(isinstance(start_date, str) and isinstance(end_date, str)):
            start_date = start_date.strftime("%Y-%m-%d")
            end_date = end_date.strftime("%Y-%m-%d")
        occupiedAccomodationsID = collection.distinct(
            "destinationID",
            {   
                "destinationType" : "accomodation",
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
                ]
            },
        )
        return occupiedAccomodationsID

    # we can filter for:
    #   - start date
    #   - end date
    #   - city
    #   - number of guests
    @staticmethod
    def getFilteredAccomodation(
        start_date="", end_date="", city="", guestNumbers="", index="", direction=""
    ):
        query = {}
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        occupiedAccomodationsID = []
        result = []

        if city != "" and city != None:
            query["location.city"] = city
        if guestNumbers != "" and guestNumbers != None:
            query["accommodates"] = {}
            query["accommodates"]["$gte"] = int(guestNumbers)

        if ( start_date != "" and end_date != "" and end_date != None and start_date != None):
            # ottengo una lista di id di accomodations non occupate
            # faccio una query per tutti gli id che non sono nella lista e che matchano per città e ospiti
            occupiedAccomodationsID = AccomodationsManager.getOccupiedAccomodationIDs(start_date , end_date)
            
        query["_id"] = {}
        query["_id"]["$nin"] = occupiedAccomodationsID
        projection = {"pictures": 0, "reservations": 0, "reviews": 0}
        query["approved"] = True
        collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]

        if index == "":
            # When it is first page
            accomodations = list(
                collection.find(query, projection)
                .sort("_id", 1)
                .limit(int(os.getenv("PAGE_SIZE")))
            )
        else:
            if direction == "next":
                query["_id"]["$gt"] = ObjectId(index)
                accomodations = list(
                    collection.find(query, projection)
                    .sort("_id", 1)
                    .limit(int(os.getenv("PAGE_SIZE")))
                )
            elif direction == "previous":
                query["_id"]["$lt"] = ObjectId(index)
                accomodations = list(
                    collection.find(query, projection)
                    .sort("_id", -1)
                    .limit(int(os.getenv("PAGE_SIZE")))
                )
        for accomodation in accomodations:
            accomodationResult = Accomodation(
                accomodation["name"],
                accomodation["description"],
                str(accomodation["host_id"]),
                accomodation["host_name"],
                accomodation["mainPicture"],
                accomodation["location"],
                accomodation["property_type"],
                accomodation["accommodates"],
                accomodation["bedrooms"],
                accomodation["beds"],
                accomodation["price"],
                accomodation["minimum_nights"],
                accomodation["number_of_reviews"],
                accomodation["review_scores_rating"],
                accomodation["approved"],
                _id=str(accomodation["_id"]),
            )
            result.append(Serializer.serializeAccomodation(accomodationResult))
        return result

    @staticmethod
    def insertNewAccomodation(accomodation):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]
        try:
            result = collection.insert_one(accomodation.getDictToUpload())
            return result.inserted_id
        except Exception:
            raise Exception("Impossibile inserire")

    @staticmethod
    def deleteAccomodation(accomodationID, user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]

        try:
            cursor = dict(collection.find_one({"_id": ObjectId(accomodationID)}, {"_id": 1, "host_id": 1}))
        except Exception as e:
            raise(str(e))
        if str(cursor["host_id"]) != user["_id"] and user["role"] != "admin":
            raise Exception("L'utente non possiede l'accomodations")
        else:
            try:
                collection.delete_one({"_id": ObjectId(accomodationID)})
                return True
            except Exception:
                raise Exception("Impossibile eliminare")

    @staticmethod
    def addReview(review):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]
        try:
            collection.update_one(
                {"_id": ObjectId(review.destinationID)},
                {"$push": {"reviews": review.getDictForAdvertisement()}},
            )
        except Exception as e:
            raise Exception("Impossibile aggiungere la review: " + str(e))

    @staticmethod
    def addReservation(reservation):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]
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
        collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]
        prevStartDate = reservation["startDate"]
        prevEndDate = reservation["endDate"]
        prevTotalExpense = int(reservation["totalExpense"])
        price = prevTotalExpense / ((dateparser.parse(prevEndDate) - dateparser.parse(prevStartDate)).days)
        newNightNumber = (dateparser.parse(newEndDate) - dateparser.parse(newStartDate)).days
        newTotalExpense = newNightNumber * price

        if(str(reservation.destinationID) in AccomodationsManager.getOccupiedAccomodationIDs(newStartDate , newEndDate)):
            raise Exception("Accomodation occupata")

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

    @staticmethod
    def getAccomodationsByUserID(userID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]
        try:
            cursor = list(collection.find({"host_id": ObjectId(userID)}))
            result = []
            for accomodation in cursor:
                accomodationResult = Accomodation(
                    accomodation["name"],
                    accomodation["description"],
                    str(accomodation["host_id"]),
                    accomodation["host_name"],
                    accomodation["mainPicture"],
                    accomodation["location"],
                    accomodation["property_type"],
                    accomodation["accommodates"],
                    accomodation["bedrooms"],
                    accomodation["beds"],
                    accomodation["price"],
                    accomodation["minimum_nights"],
                    accomodation["number_of_reviews"],
                    accomodation["review_scores_rating"],
                    accomodation["approved"],
                    accomodation["reservations"],
                    accomodation["reviews"],
                    str(accomodation["_id"]),
                    accomodation["pictures"],
                )
                result.append(Serializer.serializeAccomodation(accomodationResult))
            return result
        except Exception as e:
            raise Exception("Impossibile ottenere prenotazioni: " + str(e))
