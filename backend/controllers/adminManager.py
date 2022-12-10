from .connection import MongoManager
from models.toApprove import ToApprove
from models.accomodation import Accomodation
from models.activity import Activity
from utility.serializer import Serializer
import os
import time
from bson.objectid import ObjectId

class AdminManager():

    @staticmethod
    def getAnnouncementToApprove(index, direction):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("APPROVE_COLLECTION")]
        page_size = 2

        if index == "":
            # When it is first page
            items = collection.find().sort('_id', 1).limit(page_size)
        else:
            if (direction == "next"):
                items = collection.find({'_id': {'$gt': ObjectId(index)}}).sort('_id', 1).limit(page_size)
            elif (direction == "previous"):
                items = collection.find({'_id': {'$lt': ObjectId(index)}}).sort('_id', -1).limit(page_size)

        result = []

        for item in items:
            tempToApprove = ToApprove(
                str(item["_id"]) ,
                item["name"] ,
                str(item["host_id"]) ,
                item["location"] ,
                item["type"])
            result.append(Serializer.serializeToApprove(tempToApprove))
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

        