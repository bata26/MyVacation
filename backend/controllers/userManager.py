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
            str(cursor["_id"]) ,
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
            cursor["reviews"] ,
            cursor["plaHistory"] ,
            cursor["actHistory"],
            cursor["picture"])
        return Serializer.serializeUser(user)
        #cursor["_id"] = str(cursor["_id"])
        #return cursor

    # we can filter for:
    #   - name
    #   - surname
    # TODO: da spostare
    @staticmethod
    def getFilteredUsers(user , id = "" , name = "" , surname = "" , index = "", direction  = ""):
        if (user["role"] != "admin"):
            raise Exception("L'utente non possiede i privilegi di admin")

        query = {}
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        result = []
        page_size = 2;

        if(id != "" and id != None):
            query["_id"] = ObjectId(id)
        if(name != "" and name != None):
            query["name"] = name
        if(surname != "" and surname != None):
            query["surname"] = surname

        collection = db[os.getenv("USERS_COLLECTION")]

        if index == "":
            # When it is first page
            users = collection.find().sort('_id', 1).limit(page_size)
        else:
            if (direction == "next"):
                users = collection.find({'_id': {'$gt': ObjectId(index)}} , {"picture" : 0}).sort('_id', 1).limit(page_size)
            elif (direction == "previous"):
                users = collection.find({'_id': {'$lt': ObjectId(index)}} , {"picture" : 0}).sort('_id', -1).limit(page_size)

        for user in users:
            userResult = User(
                str(user["_id"]) ,
                user["username"] ,
                user["password"] ,
                user["name"] ,
                user["surname"] ,
                user["type"] ,
                user["gender"] ,
                user["dateOfBirth"] ,
                user["nationality"] ,
                user["knownLanguages"] ,
                user["prenotations"] ,
                user["reviews"] ,
                user["plaHistory"] ,
                user["actHistory"])
            result.append(Serializer.serializeUser(userResult))
        return result



    @staticmethod
    def insertNewUser(user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("USERS_COLLECTION")]
        try:
            collection.insert_one(user.getDictToUpload())
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
                return str(cursor["_id"]) , cursor["type"]
            else:
                raise Exception("Credenziali non valide")
        except Exception:
            raise Exception("impossibile procedere con l'autenticazione")
