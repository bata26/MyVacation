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
from controllers.accomodationsManager import AccomodationsManager
from controllers.activityManager import ActivityManager

class ReservationManager:

    @staticmethod
    def book(reservation):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        reservationCollection = db[os.getenv("RESERVATIONS_COLLECTION")]
        destinationCollection = db[os.getenv("ACCOMODATIONS_COLLECTION")] if reservation.destinationType == "accomodation" else db[os.getenv("ACTIVITIES_COLLECTION")]
        usersCollection = db[os.getenv("USERS_COLLECTION")]
        try:
            if(reservation.destinationType == "accomodation" and ObjectId(reservation.destinationID) in AccomodationsManager.getOccupiedAccomodationIDs(reservation.startDate , reservation.endDate)):
                raise Exception("accomodation occupata")
            elif (reservation.destinationType == "activity" and ObjectId(reservation.destinationID) in ActivityManager.getOccupiedActivities(reservation.startDate)):
                raise Exception("activity occupata")

            with client.start_session() as session:
                with session.start_transaction():
                    insertedReservation = reservationCollection.insert_one(reservation.getDictToUpload(), session=session)
                    reservation._id = insertedReservation.inserted_id
                    
                    destinationCollection.update_one({"_id" : ObjectId(reservation.destinationID)} , {"$push" : {"reservations": reservation.getDictForAdvertisement()}}, session=session)
                    usersCollection.update_one({"_id" : ObjectId(reservation.userID)} , {"$push" : {"reservations" : reservation.getDictForUser()}}, session=session)
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
        destinationCollection = db[os.getenv("ACCOMODATIONS_COLLECTION")] if reservation.destinationType == "accomodation" else db[os.getenv("ACTIVITIES_COLLECTION")]
        usersCollection = db[os.getenv("USERS_COLLECTION")]
        try:
            query = {}
            if( destinationType == "accomodation"):
                if (newStartDate != "" and newEndDate != "" and newEndDate != None and newStartDate != None):
                    prevEndDate = reservation["endDate"]
                    price = prevTotalExpense/((dateparser.parse(prevEndDate) - dateparser.parse(prevStartDate)).days)

                    # ottengo una lista di id di accomodations non occupate
                    # faccio una query per tutti gli id che non sono nella lista e che matchano per città e ospiti
                    occupiedAccomodationsID = AccomodationsManager.getOccupiedAccomodationIDs(newStartDate , newEndDate)

                    if ObjectId(destinationID) in occupiedAccomodationsID:
                        raise Exception("Accomodation Occupata, impossibile aggiornare")
                    newNightNumber = (((dateparser.parse(newEndDate) - dateparser.parse(newStartDate)).days))
                    newTotalExpense = newNightNumber*price
                    query = { '_id': ObjectId(reservationID) }
                   
                    with client.start_session() as session:
                        with session.start_transaction():
                            collection.update_one(query, {"$set": {'startDate': dateparser.parse(newStartDate), 'endDate': dateparser.parse(newEndDate), "totalExpense" : newTotalExpense}} , session=session)
                            destinationCollection.update_one({"_id" : ObjectId(reservation.destinationID) , "reservations._id" : ObjectId(reservation._id)} , {"$set" : {"reservations.$.startDate" : newStartDate , "reservations.$.endDate" : newEndDate}}, session=session)
                            usersCollection.update_one({"_id" : ObjectId(reservation.userID) , "reservations._id" : ObjectId(reservation._id)} , {"$set" : {"reservations.$.startDate" : newStartDate , "reservations.$.endDate" : newEndDate}} , session=session)
            elif(destinationType == "activity"):
                if (newStartDate != "" and newStartDate != None):
                    occupiedActivitiesID = collection.distinct("_id" , {"destinationID" : ObjectId(destinationID) , "startDate": dateparser.parse(newStartDate)})
                    
                    if len(occupiedActivitiesID) != 0:
                        print("Activity Occupata!")
                        raise Exception("Accomodation Occupata, impossibile aggiornare")

                    query = { '_id': ObjectId(reservationID) }
                    with client.start_session() as session:
                        with session.start_transaction():
                            collection.update_one(query, {"$set": {'startDate': dateparser.parse(newStartDate),  "totalExpense" : reservation.price }} , session=session)
                            destinationCollection.update_one({"_id" : ObjectId(reservation.destinationID) , "reservations._id" : ObjectId(reservation._id)} , {"$set" : {"reservations.$.startDate" : newStartDate }}, session=session)
                            usersCollection.update_one({"_id" : ObjectId(reservation.userID) , "reservations._id" : ObjectId(reservation._id)} , {"$set" : {"reservations.$.startDate" : newStartDate }} , session=session)
            
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
            
            destinationCollection = db[os.getenv("ACCOMODATIONS_COLLECTION")] if reservation["destinationType"] == "accomodation" else db[os.getenv("ACTIVITIES_COLLECTION")]

            with client.start_session() as session:
                with session.start_transaction():
                    reservationCollection.delete_one({"_id" : ObjectId(reservationID)}, session=session)
                    destinationCollection.update_one({"_id" : ObjectId(reservation["destinationID"])} , {"$pull" : {"reservations": {"_id" : ObjectId(reservationID)}}}, session=session)
                    usersCollection.update_one({"_id" : ObjectId(reservation["userID"])} , {"$pull" : {"reservations": {"_id" : ObjectId(reservationID)}}}, session=session)
                    
        except Exception as e:
            raise Exception("Impossibile eliminarte prenotazione "+reservationID+": " + str(e))