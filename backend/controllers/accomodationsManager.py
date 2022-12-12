from .connection import MongoManager
import os
from models.accomodation import Accomodation
from bson.objectid import ObjectId
from utility.serializer import Serializer
from datetime import datetime
import dateparser

class AccomodationsManager:

    @staticmethod
    def getAccomodationsFromId(accomodationID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]
        cursor = dict(collection.find_one({"_id" : ObjectId(accomodationID)}))
        accomodation = Accomodation(
            str(cursor["_id"]),
            cursor["name"] ,
            cursor["description"] ,
            cursor["pictures"] ,
            cursor["host_id"] ,
            cursor["host_url"] ,
            cursor["host_name"] ,
            cursor["mainPicture"] ,
            cursor["host_picture"] ,
            cursor["location"] ,
            cursor["property_type"] ,
            cursor["accommodates"] ,
            cursor["bedrooms"] ,
            cursor["beds"] ,
            cursor["price"] ,
            cursor["minimum_nights"] ,
            cursor["number_of_reviews"] ,
            cursor["review_scores_rating"])
        return Serializer.serializeAccomodation(accomodation)
        #cursor["_id"] = str(cursor["_id"])
        #return cursor

    # we can filter for:
    #   - start date
    #   - end date
    #   - city
    #   - number of guests
    @staticmethod
    def getFilteredAccomodation(start_date = "" , end_date = "" , city="" , guestNumbers="", index="", direction=""):
        query = {}
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        occupiedAccomodationsID = []
        result = []
        page_size = 12

        if(city != "" and city != None):
            query["location.city"] = city
        if(guestNumbers != "" and guestNumbers != None):
            query["accommodates"] = {}
            query["accommodates"]["$gte"] = int(guestNumbers)
        # se inserisce la data iniziale deve per forza esserci anche la data finale (la validazione verrà fatta sulla richiesta)
        if(start_date != "" and end_date != "" and end_date != None and start_date != None):
            # ottengo una lista di id di accomodations non occupate
            # faccio una query per tutti gli id che non sono nella lista e che matchano per città e ospiti
            collection = db[os.getenv("RESERVATIONS_COLLECTION")]
            occupiedAccomodationsID = collection.distinct("destinationId" , { "$or" : [
                    {"$and" : [
                        { "start_date" : { "$lte" : end_date}},
                        { "start_date" : { "$gte" : start_date}}
                    ]} ,
                    {"$and" : [
                        { "end_date" : { "$lte" : end_date}},
                        { "end_date" : { "$gte" : start_date}}
                    ]} 
            ]})
        query["_id"] = {}
        query["_id"]["$nin"] = occupiedAccomodationsID
        collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]

        if index == "":
        # When it is first page
            accomodations = collection.find().sort('_id', 1).limit(page_size)
        else:
            if (direction == "next"):
                accomodations = collection.find({'_id': {'$gt': ObjectId(index)}}).sort('_id', 1).limit(page_size)
            elif (direction == "previous"):
                accomodations = collection.find({'_id': {'$lt': ObjectId(index)}}).sort('_id', -1).limit(page_size)
        for accomodation in accomodations:
            accomodationResult = Accomodation(
                str(accomodation["_id"]) ,
                accomodation["name"] ,
                accomodation["description"] ,
                accomodation["pictures"] ,
                accomodation["host_id"] ,
                accomodation["host_url"] ,
                accomodation["host_name"] ,
                accomodation["mainPicture"] ,
                accomodation["host_picture"] ,
                accomodation["location"] ,
                accomodation["property_type"] ,
                accomodation["accommodates"] ,
                accomodation["bedrooms"] ,
                accomodation["beds"] ,
                accomodation["price"] ,
                accomodation["minimum_nights"] ,
                accomodation["number_of_reviews"] ,
                accomodation["review_scores_rating"])
            result.append(Serializer.serializeAccomodation(accomodationResult))
        print("Lenght List is :",len(result))
        return result
        
    @staticmethod
    def insertNewAccomodation(accomodation):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]
        try:
            collection.insert_one(accomodation.getDictToUpload())
        except Exception:
            raise Exception("Impossibile inserire")


    @staticmethod
    def deleteAccomodation(accomodationID , user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]

        if (user["type"] != "admin"):
            accomodation = collection.find_one({"_id" : ObjectId(accomodationID)})
            if(accomodation.host_id != user._id):
                raise Exception("L'utente non possiede l'accomodations")
        try:
            res = collection.delete_one({"_id" : ObjectId(accomodationID)})
            return res
        except Exception:
            raise Exception("Impossibile inserire")