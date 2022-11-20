from .connection import MongoManager
import os
from models.review import Review
from bson.objectid import ObjectId
from utility.serializer import Serializer

class ReviewManager:

    @staticmethod
    def getReviewFromID(reviewID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("REVIEW_COLLECTION")]
        cursor = dict(collection.find_one({"_id" : ObjectId(reviewID)}))
        review = Review(
            str(cursor["_id"]) ,
            cursor["reviewerID"] ,
            cursor["destinationID"] ,
            cursor["host_name"] ,
            cursor["score"] ,
            cursor["comment"])
        return Serializer.serializeReview(review)


    @staticmethod
    def insertNewReview(review):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("REVIEW_COLLECTION")]
        try:
            collection.insert_one(review.getDictToUpload())
        except Exception:
            raise Exception("Impossibile inserire")


    @staticmethod
    def deleteReview(reviewID , user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("REVIEW_COLLECTION")]

        if (user.type != "admin"):
            review = collection.find_one({"_id" : ObjectId(reviewID)})
            if(review.host_id != user._id):
                raise Exception("L'utente non possiede la review")
        try:
            res = collection.delete_one({"_id" : ObjectId(reviewID)})
            return res
        except Exception:
            raise Exception("Impossibile eliminare")