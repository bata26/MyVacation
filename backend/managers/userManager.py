from utility.connection import MongoManager
import os
from models.user import User
from bson.objectid import ObjectId
from utility.serializer import Serializer
import bcrypt
import dateparser
from flask import jsonify

class UserManager:
#Cheks if the username is already taken by another user
    @staticmethod
    def checkIfUserExists(username):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("USERS_COLLECTION")]
        try:
            result = collection.count_documents({"username" : username})
            return result
        except Exception:
            raise Exception("Impossibile inserire")

#Gets a user from his id
    @staticmethod
    def getUserFromID(userID):
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

#Inserts a user after the signUp
    @staticmethod
    def insertNewUser(user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("USERS_COLLECTION")]
        try:
            result = collection.insert_one(user.getDictToUpload())
            return result.inserted_id
        except Exception:
            raise Exception("Impossibile inserire")

#SignIn method
    @staticmethod
    def authenticateUser(username , password):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("USERS_COLLECTION")]

        try:
            cursor = dict(collection.find_one({"username" : username}))

            if(bcrypt.checkpw(password.encode('utf-8') , cursor["password"].encode('utf-8'))):
                return str(cursor["_id"]) , cursor["type"], cursor["username"] , cursor["name"]
            else:
                raise Exception("Credenziali non valide")
        except Exception:
            raise Exception("impossibile procedere con l'autenticazione")

#Adds a reservation in the user document
    @staticmethod
    def addReservation(reservation):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("USERS_COLLECTION")]
        try:
            collection.update_one({"_id" : ObjectId(reservation.userID)} , {"$push" : {"reservations" : reservation.getDictForUser()}})
        except Exception as e:
            raise Exception("Impossibile aggiungere la reservation: " + str(e))

#Updates a user
    @staticmethod
    def updateUser(user, userID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("USERS_COLLECTION")]
        try:
            collection.update_one({"_id" : ObjectId(userID)} , {"$set" : user})
        except Exception as e:
            raise Exception("Impossibile aggiornare l'utente: " + str(e))