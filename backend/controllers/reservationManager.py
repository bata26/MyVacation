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
        reservationCollection = db[os.getenv("RESERVATIONS_COLLECTION")]
        destinationCollection = db[os.getenv("ACCOMODATIONS_COLLECTION")] if reservation.destinationType == "accomodation" else db[os.getenv("ACTIVITIES_COLLECTION")]
        usersCollection = db[os.getenv("USERS_COLLECTION")]
        try:
            with client.start_session() as session:
                with session.start_transaction():
                    insertedReservation = reservationCollection.insert_one(reservation.getDictToUpload(), session=session)
                    reservation._id = insertedReservation.inserted_id
                    destinationCollection.update_one({"_id" : ObjectId(reservation.destinationID)} , {"$push" : {"reservations": reservation.getDictForAdvertisement()}}, session=session)
                    usersCollection.update_one({"_id" : ObjectId(reservation.userID)} , {"$push" : {"reservations" : reservation.getDictForUser()}})
            return insertedReservation.inserted_id
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
    def deleteReservationByID(reservationID , user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        reservationCollection = db[os.getenv("RESERVATIONS_COLLECTION")]
        
        try:
            reservation = dict(reservationCollection.find_one({"_id" : ObjectId(reservationID)}))
            print(reservation)
            print(user)
            if(user["role"] != "admin" and str(reservation["userID"]) != user["_id"]):
                raise Exception("Non si possiedono i privilegi necessari")
            
            destinationCollection = db[os.getenv("ACCOMODATIONS_COLLECTION")] if reservation["destinationType"] == "accomodation" else db[os.getenv("ACTIVITIES_COLLECTION")]

            with client.start_session() as session:
                with session.start_transaction():
                    reservationCollection.delete_one({"_id" : ObjectId(reservationID)}, session=session)
                    destinationCollection.update_one({"_id" : ObjectId(reservation["destinationID"])} , {"$pull" : {"reservations": {"_id" : ObjectId(reservationID)}}}, session=session)

        except Exception as e:
            raise Exception("Impossibile eliminarte prenotazione "+reservationID+": " + str(e))