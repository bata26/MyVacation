from utility.connection import MongoManager
from models.accommodation import Accommodation
from models.user import User
from models.activity import Activity
from utility.serializer import Serializer
import os
import time
from bson.objectid import ObjectId


class AdminManager:

    # we can filter for:
    #   - username
    #   - name
    #   - surname
    @staticmethod
    def getFilteredUsers(
        user, username="", name="", surname="", index="", direction=""
    ):
        if user["role"] != "admin":
            raise Exception("L'utente non possiede i privilegi di admin")

        query = {}
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        result = []

        if username != "" and username is not None:
            query["username"] = username
        if name != "" and name is not None:
            query["name"] = name
        if surname != "" and surname is not None:
            query["surname"] = surname

        collection = db[os.getenv("USERS_COLLECTION")]

        if index == "":
            # When it is first page
            users = (
                collection.find(query)
                .sort("_id", 1)
                .limit(int(os.getenv("ADMIN_PAGE_SIZE")))
            )
        else:
            if direction == "next":
                query["_id"] = {}
                query["_id"]["$gt"] = ObjectId(index)
                users = (
                    collection.find({"_id": {"$gt": ObjectId(index)}})
                    .sort("_id", 1)
                    .limit(int(os.getenv("ADMIN_PAGE_SIZE")))
                )
            elif direction == "previous":
                query["_id"] = {}
                query["_id"]["$lt"] = ObjectId(index)
                users = (
                    collection.find({"_id": {"$lt": ObjectId(index)}})
                    .sort("_id", -1)
                    .limit(int(os.getenv("ADMIN_PAGE_SIZE")))
                )

        for user in users:
            userResult = User(
                user["username"],
                user["password"],
                user["name"],
                user["surname"],
                user["type"],
                user["gender"],
                user["dateOfBirth"],
                user["nationality"],
                user["knownLanguages"],
                [],
                user["registrationDate"],
                str(user["_id"]),
            )
            result.append(Serializer.serializeUser(userResult))
        return result

    @staticmethod
    def getAnnouncementsToApprove(index, direction, destinationType):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        if destinationType == "accommodation":
            collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        else:
            collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        result = []
        query = {}
        query["approved"] = False
        projection = {}
        projection["pictures"] = 0
        projection["mainPicture"] = 0
        if index == "":
            # When it is first page
            items = list(
                collection.find(query, projection)
                .sort("_id", 1)
                .limit(int(os.getenv("ADMIN_PAGE_SIZE")))
            )
        else:
            query["_id"] = {}
            if direction == "next":
                query["_id"]["$gt"] = ObjectId(index)
                items = list(
                    collection.find(query, projection)
                    .sort("_id", 1)
                    .limit(int(os.getenv("ADMIN_PAGE_SIZE")))
                )
            elif direction == "previous":
                query["_id"]["$lt"] = ObjectId(index)
                items = list(
                    collection.find(query, projection)
                    .sort("_id", -1)
                    .limit(int(os.getenv("ADMIN_PAGE_SIZE")))
                )
        if destinationType == "accommodation":
            for item in items:
                tempToApprove = Accommodation(
                    item["name"],
                    item["description"],
                    str(item["hostID"]),
                    item["hostName"],
                    None,  # ignoriamo la mainPicture
                    item["location"],
                    item["propertyType"],
                    item["guests"],
                    item["bedrooms"],
                    item["beds"],
                    item["price"],
                    item["approved"],
                    _id=str(item["_id"]),
                )
                result.append(Serializer.serializeAccommodation(tempToApprove))
        else:
            for item in items:
                tempToApprove = Activity(
                    str(item["hostID"]),
                    item["hostName"],
                    item["location"],
                    item["description"],
                    item["duration"],
                    item["price"],
                    None,  # ignoriamo la mainPicture
                    item["name"],
                    item["approved"],
                    _id=str(item["_id"]),
                )
                result.append(Serializer.serializeActivity(tempToApprove))
            #print(result)
        return result

    @staticmethod
    def getAnnouncementToApproveByID(announcementID, destinationType):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]

        if destinationType == "accommodation":
            collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        else:
            collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        announcement = collection.find_one({"_id": ObjectId(announcementID)})
        result = None
        if destinationType == "accommodation":
            accommodationToBeApproved = Accommodation(
                announcement["name"],
                announcement["description"],
                str(announcement["hostID"]),
                announcement["hostName"],
                announcement["mainPicture"],
                announcement["location"],
                announcement["propertyType"],
                announcement["guests"],
                announcement["bedrooms"],
                announcement["beds"],
                announcement["price"],
                announcement["approved"],
                _id = str(announcement["_id"]),
                pictures = announcement["pictures"],
            )
            result = Serializer.serializeAccommodation(accommodationToBeApproved)

        elif destinationType == "activity":
            activityToBeApproved = Activity(
                str(announcement["hostID"]),
                announcement["hostName"],
                announcement["location"],
                announcement["description"],
                announcement["duration"],
                announcement["price"],
                announcement["mainPicture"],
                announcement["name"],
                announcement["approved"],
                _id = str(announcement["_id"]),
            )
            result = Serializer.serializeActivity(activityToBeApproved)
        return result

    @staticmethod
    def approveAnnouncement(announcementID, user, destinationType):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]

        if destinationType == "accommodation":
            collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        else:
            collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            if user["role"] != "admin":
                raise Exception("L'utente non è admin")
            else:
                collection.update_one(
                    {"_id": ObjectId(announcementID)}, {"$set": {"approved": True}}
                )
        except Exception as e:
            raise Exception(f"Impossibile trovare l'annuncio: {announcementID}")

    @staticmethod
    def removeApprovalAnnouncement(announcementID, user, destinationType):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]

        if destinationType == "accommodation":
            collection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        else:
            collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        try:
            if user["role"] != "admin":
                raise Exception("L'utente non è admin")
            else:
                collection.update_one(
                    {"_id": ObjectId(announcementID)}, {"$set": {"approved": False}}
                )
        except Exception as e:
            raise Exception(f"Impossibile trovare l'annuncio: {announcementID}")

    @staticmethod
    def deleteUser(userID, user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        usersCollection = db[os.getenv("USERS_COLLECTION")]
        activitiesCollection = db[os.getenv("ACTIVITIES_COLLECTION")]
        accommodationCollection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        reviewsCollection = db[os.getenv("REVIEWS_COLLECTION")]

        if user["role"] != "admin":
            raise Exception("L'utente non possiede i privilegi di admin")
        #try:
        #    res = collection.delete_one({"_id": ObjectId(userID)})
        #    return res
        try:
            with client.start_session() as session:
                 with session.start_transaction():
                    usersCollection.delete_one({"_id": ObjectId(userID)})
                    activitiesCollection.delete_many({"hostID" : ObjectId(userID)}, session=session)
                    accommodationCollection.delete_many({"hostID" : ObjectId(userID)}, session=session)
                    reviewsCollection.delete_many({"userID" : ObjectId(userID)}, session=session)
                    activitiesCollection.update_many({"reviews.userID" : ObjectId(userID)}, session=session)
                    accommodationCollection.update_many({"reviews.userID" : ObjectId(userID)}, session=session)
            return True
        except Exception:
            raise Exception("Impossibile eliminare")
