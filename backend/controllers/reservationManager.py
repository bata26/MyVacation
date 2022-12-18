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
            cursor = list(collection.find({"userID" : userID}))
            result =[]
            for reservation in cursor:
                if reservation['destinationType'] == 'activity':
                    activityResult = Reservation(
                        reservation['userID'],
                        reservation['destinationID'],
                        reservation['destinationType'],
                        reservation['startDate'],
                        "",
                        reservation['totalExpense'],
                        reservation['_id'])
                    result.append(Serializer.serializeReservation(activityResult))
                else:
                    accomodationResult = Reservation(
                        reservation['userID'],
                        reservation['destinationID'],
                        reservation['destinationType'],
                        reservation['startDate'],
                        reservation['endDate'],
                        reservation['totalExpense'],
                        reservation['_id'])
                    result.append(Serializer.serializeReservation(accomodationResult))
            return result
        except Exception as e:
            raise Exception("Impossibile ottenere prenotazioni: " + str(e))

    
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