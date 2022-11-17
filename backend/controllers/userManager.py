from .connection import MongoManager
import os
from models.user import User
from bson.objectid import ObjectId
from utility.serializer import Serializer

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
            cursor["description"] ,
            cursor["gender"] ,
            cursor["dateOfBirth"] ,
            cursor["nationality"] ,
            cursor["knownLanguages"] ,
            cursor["prenotations"] ,
            cursor["reviews"] ,
            cursor["plaHistory"] ,
            cursor["actHistory"])
        return Serializer.serializeUser(User)
        #cursor["_id"] = str(cursor["_id"])
        #return cursor

    # we can filter for:
    #   - name
    #   - surname
    @staticmethod
    def getFilteredUsers(name = "" , surname = "" ):
        if (user["type"] != "admin"):
            raise Exception("L'utente non possiede i privilegi di admin")

        query = {}
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        result = []

        if(name != ""):
            query["name"] = name
        if(surname != ""):
            query["surname"] = surname
        
        collection = db[os.getenv("USERS_COLLECTION")]
        users = list(collection.find(query))
        for user in users:
            userResult = User(
                str(user["_id"]) ,
                user["username"] ,
                user["password"] ,
                user["name"] ,
                user["surname"] ,
                user["type"] ,
                user["description"] ,
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
    def deleteUser(userID , user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("USERS_COLLECTION")]

        if (user["type"] != "admin"):
           raise Exception("L'utente non possiede i privilegi di admin")
        try:
            res = collection.delete_one({"_id" : ObjectId(userID)})
            return res
        except Exception:
            raise Exception("Impossibile eliminare")