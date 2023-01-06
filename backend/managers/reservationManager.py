from utility.connection import MongoManager
import os
from models.accommodation import Accommodation
from bson.objectid import ObjectId
from utility.serializer import Serializer
from models.reservation import Reservation
from datetime import datetime
import dateparser
from bson.objectid import ObjectId
from utility.serializer import Serializer
from managers.accommodationManager import AccommodationManager
from managers.activityManager import ActivityManager

class ReservationManager:

    @staticmethod
    def book(reservation):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        reservationCollection = db[os.getenv("RESERVATIONS_COLLECTION")]
        usersCollection = db[os.getenv("USERS_COLLECTION")]
        try:
            if(reservation.destinationType == "accommodation" and ObjectId(reservation.destinationID) in AccommodationManager.getOccupiedAccommodationIDs(reservation.startDate , reservation.endDate)):
                raise Exception("accommodation occupata")
            elif (reservation.destinationType == "activity" and ObjectId(reservation.destinationID) in ActivityManager.getOccupiedActivities(reservation.startDate)):
                raise Exception("activity occupata")

            with client.start_session() as session:
                with session.start_transaction():
                    insertedReservation = reservationCollection.insert_one(reservation.getDictToUpload(), session=session)
                    reservation._id = insertedReservation.inserted_id
                    usersCollection.update_one({"_id" : ObjectId(reservation.userID)} , {"$push" : {"reservations" : reservation.getDictForUser()}}, session=session)
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
                    accommodationResult = Reservation(
                        str(reservation['userID']),
                        str(reservation['destinationID']),
                        reservation['destinationType'],
                        reservation['startDate'],
                        reservation['totalExpense'],
                        reservation["city"],                        
                        str(reservation["hostID"]),
                        reservation['endDate'],
                        str(reservation['_id']))
                    result.append(Serializer.serializeReservation(accommodationResult))
            return result
        except Exception as e:
            raise Exception("Impossibile ottenere prenotazioni: " + str(e))

    @staticmethod
    def updateReservation(reservation, newStartDate, newEndDate , user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("RESERVATIONS_COLLECTION")]
        prevStartDate = reservation["startDate"]
        destinationID = reservation["destinationID"]
        reservationID = reservation["_id"]
        prevTotalExpense = int(reservation["totalExpense"])
        destinationType = reservation["destinationType"]
        print(reservation)
        usersCollection = db[os.getenv("USERS_COLLECTION")]
        try:
            oldReservation = collection.find_one({"_id" : ObjectId(reservationID)})
            if(user["_id"] != str(oldReservation["userID"])):
                raise Exception("L'utente non possiede la reservation")

            query = {}
            if( destinationType == "accommodation"):
                if (newStartDate != "" and newEndDate != "" and newEndDate != None and newStartDate != None):
                    prevEndDate = reservation["endDate"]
                    price = prevTotalExpense/((dateparser.parse(prevEndDate) - dateparser.parse(prevStartDate)).days)

                    # ottengo una lista di id di accommodations non occupate
                    # faccio una query per tutti gli id che non sono nella lista e che matchano per città e ospiti
                    occupiedAccommodationsID = AccommodationManager.getOccupiedAccommodationIDs(newStartDate , newEndDate , reservation["_id"])
                    if ObjectId(destinationID) in occupiedAccommodationsID:
                        raise Exception("Accommodation Occupata, impossibile aggiornare")

                    print("pre")
                    newNightNumber = (((dateparser.parse(newEndDate) - dateparser.parse(newStartDate)).days))
                    newTotalExpense = newNightNumber*price
                    query = { '_id': ObjectId(reservationID) }
                    print("post")
                    with client.start_session() as session:
                        with session.start_transaction():
                            collection.update_one(query, {"$set": {'startDate': dateparser.parse(newStartDate), 'endDate': dateparser.parse(newEndDate), "totalExpense" : newTotalExpense}} , session=session)
                            usersCollection.update_one({"_id" : ObjectId(user["_id"]) , "reservations._id" : ObjectId(reservation["_id"])} , {"$set" : {"reservations.$.startDate" : dateparser.parse(newStartDate) , "reservations.$.endDate" : dateparser.parse(newEndDate)}} , session=session)

                    
            elif(destinationType == "activity"):
                if (newStartDate != "" and newStartDate != None):
                    occupiedActivitiesID = ActivityManager.getOccupiedActivities(newStartDate , reservation["_id"] )
                    
                    if len(occupiedActivitiesID) != 0:
                        raise Exception("Accommodation Occupata, impossibile aggiornare")

                    query = { '_id': ObjectId(reservationID) }
                    with client.start_session() as session:
                        with session.start_transaction():
                            collection.update_one(query, {"$set": {'startDate': dateparser.parse(newStartDate),  "totalExpense" : reservation.price }} , session=session)
                            usersCollection.update_one({"_id" : ObjectId(user["_id"]) , "reservations._id" : ObjectId(reservation["_id"])} , {"$set" : {"reservations.$.startDate" : newStartDate }} , session=session)
            
        except Exception as e:
            raise Exception("Impossibile aggiornare prenotazione "+reservationID+": " + str(e))


    @staticmethod
    def deleteReservationByID(reservationID , user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        reservationCollection = db[os.getenv("RESERVATIONS_COLLECTION")]
        usersCollection = db[os.getenv("USERS_COLLECTION")]

        try:
            reservation = dict(reservationCollection.find_one({"_id" : ObjectId(reservationID)}))

            if(user["role"] != "admin" and str(reservation["userID"]) != user["_id"]):
                raise Exception("Non si possiedono i privilegi necessari")
            
            with client.start_session() as session:
                with session.start_transaction():
                    reservationCollection.delete_one({"_id" : ObjectId(reservationID)}, session=session)
                    usersCollection.update_one({"_id" : ObjectId(reservation["userID"])} , {"$pull" : {"reservations": {"_id" : ObjectId(reservationID)}}}, session=session)
                    
        except Exception as e:
            raise Exception("Impossibile eliminarte prenotazione "+reservationID+": " + str(e))