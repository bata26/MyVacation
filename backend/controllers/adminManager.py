from userManager import UserManager
from connection import MongoManager
from models.activity import Activity
from models.accomodation import Accomodation
from utility.serializer import Serializer
import os

class AdminManager(UserManager):

    @staticmethod
    def getItemToApprove():
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("APPROVE_COLLECTIONS")]

        cursor = list(collection.find())
        result = []
        for item in cursor:
            if item["type"] == "activity":
                tempActivity = Activity(
                    str(item["_id"]) ,
                    str(item["host_id"]) ,
                    item["host_url"] ,
                    item["host_name"] ,
                    item["host_picture"] ,
                    item["location"] ,
                    item["description"] ,
                    item["prenotations"] ,
                    item["duration"] ,
                    item["pricePerPerson"] ,
                    item["number_of_reviews"] ,
                    item["review_scores_rating"],
                    item["picture"],
                    item["category"])
                result.append(Serializer.serializeActivity(tempActivity))
            else:
                tempAccomodation = Accomodation(
                    str(item["_id"]) ,
                    item["name"] ,
                    item["description"] ,
                    item["pictures"] ,
                    item["host_id"] ,
                    item["host_url"] ,
                    item["host_name"] ,
                    item["mainPicture"] ,
                    item["host_picture"] ,
                    item["location"] ,
                    item["property_type"] ,
                    item["accommodates"] ,
                    item["bedrooms"] ,
                    item["beds"] ,
                    item["price"] ,
                    item["minimum_nights"] ,
                    item["number_of_reviews"] ,
                    item["review_scores_rating"])
            result.append(Serializer.serializeAccomodation(tempAccomodation))
        return result
        