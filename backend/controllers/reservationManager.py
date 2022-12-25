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
    def updateReservation(reservation, newStartDate, newEndDate):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]
        prevStartDate = reservation["startDate"]
        destinationID = reservation["destinationID"]
        reservationID = reservation["_id"]
        prevTotalExpense = int(reservation["totalExpense"])
        destinationType = reservation["destinationType"]
        try:
            query = {}
            print(f"DestinationType: {destinationType}")
            if( destinationType == "accomodation"):
                if (newStartDate != "" and newEndDate != "" and newEndDate != None and newStartDate != None):
                    prevEndDate = reservation["endDate"]
                    price = prevTotalExpense/((dateparser.parse(prevEndDate) - dateparser.parse(prevStartDate)).days)

                    # ottengo una lista di id di accomodations non occupate
                    # faccio una query per tutti gli id che non sono nella lista e che matchano per città e ospiti
                    occupiedAccomodationsID = collection.distinct("destinationID",{
                        "$and" : [
                            {"_id": {"$ne":ObjectId(reservationID)}},
                            {"$or": [
                                {"$and": [
                                    {"startDate": {"$lte": dateparser.parse(newEndDate)}},
                                    {"startDate": {"$gte": dateparser.parse(newStartDate)}}
                                ]},
                                {"$and": [
                                    {"endDate": {"$lte": dateparser.parse(newEndDate)}},
                                    {"endDate": {"$gte": dateparser.parse(newStartDate)}}
                                ]}
                            ]}]})

                    if ObjectId(destinationID) in occupiedAccomodationsID:
                        print("Accomodation Occupata!")
                        raise Exception("Accomodation Occupata, impossibile aggiornare")
                    newNightNumber = (((dateparser.parse(newEndDate) - dateparser.parse(newStartDate)).days))
                    newTotalExpense = newNightNumber*price
                    query = { '_id': ObjectId(reservationID) }
                    result = collection.update_one(query, {"$set": {'startDate': dateparser.parse(newStartDate), 'endDate': dateparser.parse(newEndDate), "totalExpense" : newTotalExpense}})

                    return result
            elif(destinationType == "activity"):
                if (newStartDate != "" and newStartDate != None):
                    occupiedActivitiesID = collection.distinct("_id" , {"destinationID" : ObjectId(destinationID) , "startDate": dateparser.parse(newStartDate)})
                    
                    if len(occupiedActivitiesID) != 0:
                        print("Activity Occupata!")
                        raise Exception("Accomodation Occupata, impossibile aggiornare")

                    query["_id"] = ObjectId(reservationID)
                    result = collection.update_one(query, {"$set": {'startDate': dateparser.parse(newStartDate)}})
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