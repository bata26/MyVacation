from .connection import MongoManager
import os
from models.accomodation import Accomodation
from bson.objectid import ObjectId
from utility.serializer import Serializer
from models.reservation import Reservation
from datetime import datetime
import dateparser
from bson.objectid import ObjectId
from utility.serializer import Serializer

class ReservationManager:

    @staticmethod
    def book(reservation):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]
        try:
            res = collection.insert_one(reservation.getDictToUpload())
            return res.inserted_id
        except Exception as e:
            raise Exception("Impossibile prenotare: " + str(e) )

    @staticmethod
    def getReservationsByUser(userID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]
        try:
            cursor = list(collection.find({"userID" : ObjectId(userID)}))
            result =[]
            for reservation in cursor:
                if reservation['destinationType'] == 'activity':
                    activityResult = Reservation(
                        str(reservation['userID']),
                        str(reservation['destinationID']),
                        reservation['destinationType'],
                        reservation['startDate'],
                        reservation['totalExpense'],
                        reservation["city"],                        
                        str(reservation["hostID"]),
                        _id = str(reservation['_id']))
                    result.append(Serializer.serializeReservation(activityResult))
                else:
                    accomodationResult = Reservation(
                        str(reservation['userID']),
                        str(reservation['destinationID']),
                        reservation['destinationType'],
                        reservation['startDate'],
                        reservation['totalExpense'],
                        reservation["city"],                        
                        str(reservation["hostID"]),
                        reservation['endDate'],
                        str(reservation['_id']))
                    result.append(Serializer.serializeReservation(accomodationResult))
            return result
        except Exception as e:
            raise Exception("Impossibile ottenere prenotazioni: " + str(e))

    @staticmethod
    def updateReservation(startDate, endDate, type, reservationID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]
        try:
            query = {}
            if(type == "accomodation"):
                if (startDate != "" and endDate != "" and endDate != None and startDate != None):
                    print("DEBUG1")
                    # ottengo una lista di id di accomodations non occupate
                    # faccio una query per tutti gli id che non sono nella lista e che matchano per città e ospiti
                    occupiedAccomodationsID = collection.distinct("destinationID", {"$or": [
                    {"$and": [
                        {"startDate": {"$lte": dateparser.parse(endDate)}},
                        {"starDate": {"$gte": dateparser.parse(startDate)}}
                    ]},
                    {"$and": [
                        {"endDate": {"$lte": dateparser.parse(endDate)}},
                        {"endDate": {"$gte": dateparser.parse(startDate)}}
                    ]}
                    ]})
                    print("DEBUG2")
                    query = { '$match': { '$and': [ { '_id': ObjectId(reservationID) }, { 'destinationID': { '$nin': occupiedAccomodationsID } } ] } }
                    #query["_id"] = ObjectId(reservationID)
                    print("DEBUG3")
                    print(query)
                    #query["destinationID"]["$nin"] = occupiedAccomodationsID
                    result = collection.update_one({query}, {"$set": {'startDate': dateparser.parse(startDate), 'endDate': dateparser.parse(endDate)}})
                    print("DEBUG4")
            if(type == "activity"):
                if (startDate != "" and startDate != None):
                    occupiedActivitiesID = collection.distinct("destinationID",
                                                       {"startDate": dateparser.parse(startDate)}
                                                       )
                    query["_id"] = ObjectId(reservationID)
                    query["destinationID"]["$nin"] = occupiedActivitiesID
                    result = collection.update_one({query}, {"$set": {'startDate': dateparser.parse(startDate)}})
            if(result.matched_count == 0):
                raise Exception ("Impossibile aggiornare la prenotazione alle date inserite")
            else:
                return result
        except Exception as e:
            raise Exception("Impossibile aggiornare prenotazione "+reservationID+": " + str(e))


    @staticmethod
    def deleteReservationByID(reservationID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]

        try:
            collection.delete_one({"_id" : ObjectId(reservationID)})
            return "OK"
        except Exception as e:
            raise Exception("Impossibile eliminarte prenotazione "+reservationID+": " + str(e))