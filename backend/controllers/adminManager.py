from .userManager import UserManager
from .connection import MongoManager
from models.activity import Activity
from models.accomodation import Accomodation
from utility.serializer import Serializer
import os
import time
from bson.objectid import ObjectId

class AdminManager(UserManager):

    @staticmethod
    def getAnnouncementToApprove():
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("APPROVE_COLLECTION")]
        try:
            cursor = list(collection.find())
        except Exception as e:
            raise Exception("Impossibile connettersi al database")
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

    @staticmethod
    def approveAnnouncement(announcementID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        approveCollection = db[os.getenv("APPROVE_COLLECTION")]
        try:
            ann = approveCollection.find_one({"_id" : ObjectId(announcementID)})
            if(ann):
                if(ann["type"] == "activity"):
                    collection = db[os.getenv("ACTIVITIES_COLLECTION")]
                else:
                    collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]
                try:
                    ann.pop("_id")
                    ann.pop("type")
                    insertedID = collection.insert_one(ann) # inserisco nella nuova collection
                    print(f"inserito {insertedID}")
                    time.sleep(30)
                    try:
                        res = approveCollection.delete_one({"_id" : ObjectId(announcementID)})
                        print(res)
                    except Exception as e:
                        # impossibile eliminare da approvations quindi eseguo il rollback
                        collection.delete_one({"_id" : ObjectId(insertedID)})
                except Exception as e:
                    raise Exception("Impossibile inserire nella collection destinataria")
            else:
                raise Exception("L'announcementID non esiste")
        except Exception as e:
            raise Exception(f"Impossibile trovare l'annuncio: {announcementID}")

        