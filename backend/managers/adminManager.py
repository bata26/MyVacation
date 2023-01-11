from utility.connection import MongoManager
from models.accommodation import Accommodation
from models.user import User
from models.activity import Activity
from utility.serializer import Serializer
import os
from bson.objectid import ObjectId
from datetime import datetime
from managers.accommodationManager import AccommodationManager
from managers.activityManager import ActivityManager


# This class represents the manager for the admin query.
# Methods implements query and serialization of object.

class AdminManager:

    # method that returns a list of user filtered by paramters setted by the user
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

    # method that returns accommodation or activity that aren't yet been approved
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

    # method that return a specific accommodation/activity that is not yet benn approved
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

    # method that approve a specific accommodation/activity
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

    # method that disapprove a specific accommodation/activity, used for the rollback in case of failure 
    # when approving
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

    # method that delete a user
    @staticmethod
    def deleteUser(userID, user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        usersCollection = db[os.getenv("USERS_COLLECTION")]
        activitiesCollection = db[os.getenv("ACTIVITIES_COLLECTION")]
        accommodationCollection = db[os.getenv("ACCOMMODATIONS_COLLECTION")]
        reviewsCollection = db[os.getenv("REVIEW_COLLECTION")]
        reservationCollection = db[os.getenv("RESERVATIONS_COLLECTION")]

        if user["role"] != "admin":
            raise Exception("L'utente non possiede i privilegi di admin")
        
        try:
            
            activityHostedByUser = ActivityManager.getActivitiesIDListByUserID(userID)
            accommodationHostedByUser = AccommodationManager.getAccommodationsIDListByUserID(userID)
            totalHostedByUser = [*activityHostedByUser, *accommodationHostedByUser] 
            # we have to delete all the info connected to the user:
            # - remove all the nested reservation in user collection
            # - remove all the activities hosted by the user
            # - remove all the activities's review done by the user
            # - remove all the activities's review for the activities hosted by the user
            # - remove all the accommodation hosted by the user
            # - remove all the accommodation's review done by the user
            # - remove all the accommodations's review for the accommodations hosted by the user
            # - remove all the reviews written by the user
            # - remove all the reservation hosted by the user
            with client.start_session() as session:
                 with session.start_transaction():
                    usersCollection.delete_one({"_id": ObjectId(userID)} , session=session)
                    usersCollection.update_many({"reservations.hostID" : ObjectId(userID)} , {"$pull" : {"reservations" : {"hostID" : ObjectId(userID)}}} , session=session)
                    activitiesCollection.delete_many({"hostID" : ObjectId(userID)}, session=session)
                    activitiesCollection.update_many({"reviews.userID" : ObjectId(userID)}, {"$pull" : {"reviews" : {"userID" : ObjectId(userID)}}}, session=session)
                    activitiesCollection.update_many({"_id" : {"$in" :activityHostedByUser }} , {"$pull" : {"reviews": {"destinationID" : {"$in" :activityHostedByUser }}}}, session=session)
                    accommodationCollection.delete_many({"hostID" : ObjectId(userID)}, session=session)
                    accommodationCollection.update_many({"reviews.userID" : ObjectId(userID)}, {"$pull" : {"reviews" : {"userID" : ObjectId(userID)}}} ,session=session)
                    accommodationCollection.update_many({"_id" : {"$in" :accommodationHostedByUser }} , {"$pull" : {"reviews": {"destinationID" : {"$in" :accommodationHostedByUser }}}}, session=session)
                    reviewsCollection.delete_many({"$or" : [{"destinationID" :{"$in" :totalHostedByUser}},{"userID" : ObjectId(userID)}]} , session=session)
                    reservationCollection.delete_many({"hostID" : ObjectId(userID) , "startDate" : {"$gte" : datetime.today()}} , session=session)
            return True
        except Exception as e:
            raise Exception("Impossibile eliminare " + str(e))
