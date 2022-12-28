from .connection import MongoManager
from models.accomodation import Accomodation
from models.user import User
from models.activity import Activity
from utility.serializer import Serializer
import os
import time
from bson.objectid import ObjectId

class AdminManager():

    # we can filter for:
    #   - name
    #   - surname
    @staticmethod
    def getFilteredUsers(user , id = "" , name = "" , surname = "" , index = "", direction  = ""):
        if (user["role"] != "admin"):
            raise Exception("L'utente non possiede i privilegi di admin")

        query = {}
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        result = []

        if(id != "" and id != None):
            query["_id"] = ObjectId(id)
        if(name != "" and name != None):
            query["name"] = name
        if(surname != "" and surname != None):
            query["surname"] = surname

        collection = db[os.getenv("USERS_COLLECTION")]

        if index == "":
            # When it is first page
            users = collection.find(query).sort('_id', 1).limit(int(os.getenv("ADMIN_PAGE_SIZE")))
        else:
            if (direction == "next"):
                query["_id"] = {}
                query["_id"]["$gt"] = ObjectId(index)
                users = collection.find({'_id': {'$gt': ObjectId(index)}}).sort('_id', 1).limit(int(os.getenv("ADMIN_PAGE_SIZE")))
            elif (direction == "previous"):
                query["_id"] = {}
                query["_id"]["$lt"] = ObjectId(index)
                users = collection.find({'_id': {'$lt': ObjectId(index)}}).sort('_id', -1).limit(int(os.getenv("ADMIN_PAGE_SIZE")))

        for user in users:
            userResult = User(
                user["username"] ,
                user["password"] ,
                user["name"] ,
                user["surname"] ,
                user["type"] ,
                user["gender"] ,
                user["dateOfBirth"] ,
                user["nationality"] ,
                user["knownLanguages"] ,
                [] ,
                user["registrationDate"] ,
                str(user["_id"])
            )
            result.append(Serializer.serializeUser(userResult))
        return result

    @staticmethod
    def getAnnouncementsToApprove(index, direction, destinationType):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        if(destinationType == "accomodation"):
            collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]
        else:
            collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        result = []

        if index == "":
            # When it is first page
            items = list(collection.find({"approved" : False}).sort('_id', 1).limit(int(os.getenv("ADMIN_PAGE_SIZE"))))
        else:
            if (direction == "next"):
                items = list(collection.find({'_id': {'$gt': ObjectId(index)}, 'approved': False}).sort('_id', 1).limit(int(os.getenv("ADMIN_PAGE_SIZE"))))
            elif (direction == "previous"):
                items = list(collection.find({'_id': {'$lt': ObjectId(index)}, 'approved': False}).sort('_id', -1).limit(int(os.getenv("ADMIN_PAGE_SIZE"))))
        if(destinationType == "accomodation"):
            for item in items:
                tempToApprove = Accomodation(
                    item["name"] ,
                    item["description"] ,
                    str(item["host_id"]) ,
                    item["host_name"] ,
                    None,
                    item["location"] ,
                    item["property_type"] ,
                    item["accommodates"] ,
                    item["bedrooms"] ,
                    item["beds"] ,
                    item["price"] ,
                    item["minimum_nights"] ,
                    item["number_of_reviews"] ,
                    item["review_scores_rating"] ,
                    item["approved"] ,
                    _id = str(item["_id"]) ,
                    )
                result.append(Serializer.serializeAccomodation(tempToApprove))
        else:
            print("Sono nella query")
            for item in items:
                tempToApprove = Activity(
                    str(item["host_id"]) ,
                    item["host_name"] ,
                    item["location"] ,
                    item["description"] ,
                    item["duration"] ,
                    item["price"] ,
                    item["number_of_reviews"] ,
                    item["review_scores_rating"] ,
                    None ,
                    item["name"] ,
                    item["approved"] ,
                    _id = str(item["_id"]))
                result.append(Serializer.serializeActivity(tempToApprove))
            print(result)
        return result

    @staticmethod
    def getAnnouncementToApproveByID(announcementID, destinationType):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        if(destinationType == "accomodation"):
            collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]
        else:
            collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        announcement = collection.find_one({"_id" : ObjectId(announcementID)})
        result = None
        if(destinationType == "accomodation"):
            accomodationToBeApproved = Accomodation(
                announcement["name"],
                announcement["description"],
                str(announcement["host_id"]),
                announcement["host_name"],
                announcement["mainPicture"],
                announcement["location"],
                announcement["property_type"],
                announcement["accommodates"],
                announcement["bedrooms"],
                announcement["beds"],
                announcement["price"],
                announcement["minimum_nights"],
                "0",
                "0",
                announcement["approved"],
                [],
                [],
                str(announcement["_id"]),
                announcement["pictures"]
            )
            result = Serializer.serializeAccomodation(accomodationToBeApproved)

        elif(destinationType == "activity"):
            activityToBeApproved = Activity(
                str(announcement["host_id"]),
                announcement["host_name"],
                announcement["location"],
                announcement["description"],
                announcement["duration"],
                announcement["price"],
                0,
                0,
                announcement["mainPicture"],
                announcement["name"],
                announcement["approved"],
                [],
                [],
                str(announcement["_id"])
            )
            result = Serializer.serializeActivity(activityToBeApproved)
        return result

    @staticmethod
    def approveAnnouncement(announcementID, user, destinationType):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        if(destinationType == "accomodation"):
            collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]
        else:
            collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            if (user['role'] != "admin"):
                raise Exception("L'utente non è admin")
            else:
                try:
                    result = collection.update_one({"_id" : ObjectId(announcementID)}, {"$set":{"approved" : True}})
                    return result
                except Exception as e:
                    raise Exception("Impossibile approvare l'annuncio")
        except Exception as e:
            raise Exception(f"Impossibile trovare l'annuncio: {announcementID}")\

    @staticmethod
    def deleteUser(userID , user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("USERS_COLLECTION")]

        if (user["role"] != "admin"):
            raise Exception("L'utente non possiede i privilegi di admin")
        try:
            res = collection.delete_one({"_id" : ObjectId(userID)})
            return res
        except Exception:
            raise Exception("Impossibile eliminare")