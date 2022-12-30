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
        cursor = dict(collection.find_one({"_id": ObjectId(reviewID)}))
        review = Review(
            cursor["userID"],
            cursor["destinationID"],
            cursor["score"],
            cursor["description"],
            cursor['reviewer'],
            str(cursor["_id"]))
        return Serializer.serializeReview(review)\


    @staticmethod
    def getReviewFromDestinationID(destinationID):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("REVIEW_COLLECTION")]
        cursor = list(collection.find(
            {"destinationID": ObjectId(destinationID)}))
        result = []
        for review in cursor:
            reviewResult = Review(
                str(review["userID"]),
                str(review["destinationID"]),
                review["score"],
                review["description"],
                review['reviewer'],
                str(review['_id']))
            result.append(Serializer.serializeReview(reviewResult))
        return result

    @staticmethod
    def insertNewReview(review):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("REVIEW_COLLECTION")]
        try:
            result = collection.insert_one(review.getDictToUpload())
            return result.inserted_id
        except Exception:
            raise Exception("Impossibile inserire")

    @staticmethod
    def deleteReview(reviewID,  destinationID, destinationType, user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        reviewCollection = db[os.getenv("REVIEW_COLLECTION")]
        destinationCollection = db[os.getenv("ACCOMODATIONS_COLLECTION")] if destinationType == "accomodation" else db[os.getenv("ACTIVITIES_COLLECTION")]

        if (user["role"] != "admin"):
            review = dict(reviewCollection.find_one(
                {"_id": ObjectId(reviewID)}))
            if (str(review["userID"]) != user["_id"]):
                raise Exception("L'utente non possiede la review")
        try:
            #with client.start_session() as session:
            #    with session.start_transaction():
            #        reviewCollection.delete_one({"_id" : ObjectId(reviewID)}, session=session)
            #        destinationCollection.update_one({"_id" : ObjectId(destinationID)} , {"$pull" : {"reviews": {"_id" : ObjectId(reviewID)}}}, session=session)
            reviewCollection.delete_one({"_id" : ObjectId(reviewID)})
            destinationCollection.update_one({"_id" : ObjectId(destinationID)} , {"$pull" : {"reviews": {"_id" : ObjectId(reviewID)}}})

        except Exception as e:
            raise Exception("Impossibile eliminare : " + str(e))

    @staticmethod
    def checkIfCanReview(destinationID, destinationType, user):
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        reservationCollection = db[os.getenv("RESERVATIONS_COLLECTION")]
        reviewCollection = db[os.getenv("REVIEW_COLLECTION")]
        query = {"destinationID": ObjectId(
            destinationID), "userID": ObjectId(user["_id"])}

        try:
            totalReservations = reservationCollection.count_documents(query)
            totalReviews = reviewCollection.count_documents(query)
            if totalReservations > 0 and totalReviews == 0:
                return True
            return False
        except Exception:
            raise Exception("Impossibile ottenere la prenotazione")
