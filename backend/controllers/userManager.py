from .connection import MongoManager
import os
from models.user import User
from bson.objectid import ObjectId
from utility.serializer import Serializer
import bcrypt

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
            cursor["type"] ,
            cursor["surname"] ,
            cursor["gender"] ,
            cursor["dateOfBirth"] ,
            cursor["nationality"] ,
            cursor["knownLanguages"] ,
            cursor["prenotations"] ,
            cursor["reviews"] ,
            cursor["plaHistory"] ,
            cursor["actHistory"])
        return Serializer.serializeUser(user)
        #cursor["_id"] = str(cursor["_id"])
        #return cursor

    # we can filter for:
    #   - name
    #   - surname
    @staticmethod
    def getFilteredUsers(user , name = "" , surname = "" ):
        if (user["type"] != "admin"):
            raise Exception("L'utente non possiede i privilegi di admin")

        query = {}
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        result = []

        if(name != "" and name != None):
            query["name"] = name
        if(surname != "" and surname != None):
            query["surname"] = surname
        
        collection = db[os.getenv("USERS_COLLECTION")]
        users = list(collection.find(query))
        print(users)
        for user in users:
            userResult = User(
                str(user["_id"]) ,
                user["username"] ,
                user["password"] ,
                user["name"] ,
                user["type"] ,
                user["surname"] ,
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
                return str(cursor["_id"])
            else:
                raise Exception("Credenziali non valide")
        except Exception:
            raise Exception("impossibile procedere con l'autenticazione")
