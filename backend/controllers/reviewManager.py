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
            cursor["comment"] ,
            cursor['reviewer'])
        return Serializer.serializeReview(review)


    @staticmethod
    def insertNewReview(review):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("REVIEW_COLLECTION")]
        try:
            print("pre")
            result = collection.insert_one(review.getDictToUpload())
            print(f"inserita , _id : {result.inserted_id}")
            return result.inserted_id
        except Exception:
            raise Exception("Impossibile inserire")


    @staticmethod
    def deleteReview(reviewID , user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("REVIEW_COLLECTION")]

        if (user["role"] != "admin"):
            review = collection.find_one({"_id" : ObjectId(reviewID)})
            if(review.host_id != user._id):
                raise Exception("L'utente non possiede la review")
        try:
            res = collection.delete_one({"_id" : ObjectId(reviewID)})
            return res
        except Exception:
            raise Exception("Impossibile eliminare")
    
    @staticmethod
    def checkIfCanReview(destinationID , destinationType, user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        if(destinationType == "accomodation"):
            collection = db[os.getenv("ACCOMODATIONS_COLLECTION")]
        if(destinationType == "activity"):
            collection = db[os.getenv("ACTIVITIES_COLLECTION")]
        queryReservations = {"reservations.userID" : ObjectId(user["_id"]) , "_id" : ObjectId(destinationID)}
        queryReviews = {"reviews.userID" : ObjectId(user["_id"]) , "_id" : ObjectId(destinationID)}
        print(queryReviews)
        print(queryReservations)
        try:
            totalReservations = collection.count_documents(queryReservations)
            totalReviews = collection.count_documents(queryReviews)
            print(f"totalReservations: {totalReservations}")
            print(f"totalReviews: {totalReviews}")
            if totalReservations > 0 and totalReviews == 0:
                return True
            return False
        except Exception:
            raise Exception("Impossibile ottenere la prenotazione")