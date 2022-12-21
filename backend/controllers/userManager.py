from .connection import MongoManager
import os
from models.user import User
from bson.objectid import ObjectId
from utility.serializer import Serializer
import bcrypt
from flask import jsonify

class UserManager:

    @staticmethod
    def getUserFromId(userID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("USERS_COLLECTION")]
        cursor = dict(collection.find_one({"_id" : ObjectId(userID)}))
        user = User(
            cursor["username"] ,
            cursor["password"] ,
            cursor["name"] ,
            cursor["surname"] ,
            cursor["type"] ,
            cursor["gender"] ,
            cursor["dateOfBirth"] ,
            cursor["nationality"] ,
            cursor["knownLanguages"] ,
            cursor["reservations"] ,
            cursor["registrationDate"] ,
            str(cursor["_id"]))
        return Serializer.serializeUser(user)

    @staticmethod
    def insertNewUser(user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("USERS_COLLECTION")]
        try:
            result = collection.insert_one(user.getDictToUpload())
            print(f"inserita , _id : {result.inserted_id}")
            return result.inserted_id
        except Exception:
            raise Exception("Impossibile inserire")

    @staticmethod
    def authenicateUser(username , password):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("USERS_COLLECTION")]

        try:
            print("dentro")
            cursor = dict(collection.find_one({"username" : username}))
            print(cursor["password"])
            
            if(bcrypt.checkpw(password.encode('utf-8') , cursor["password"].encode('utf-8'))):
                return str(cursor["_id"]) , cursor["type"], cursor["name"]
            else:
                raise Exception("Credenziali non valide")
        except Exception:
            raise Exception("impossibile procedere con l'autenticazione")

    @staticmethod
    def addReservation(reservation):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("USERS_COLLECTION")]
        try:
            collection.update_one({"_id" : ObjectId(reservation.userID)} , {"$push" : {"reservations" : reservation.getDictForUser()}})
        except Exception as e:
            raise Exception("Impossibile aggiungere la reservation: " + str(e))
