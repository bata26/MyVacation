import base64
from bson.objectid import ObjectId


class Activity:
    def __init__(self , host_id  , 
        host_name  , location , description , 
        duration , price , number_of_reviews , 
        reviews_score_rating , mainPicture , name , reservations=[],reviews=[], _id=""):
        self.host_id = host_id 
        self.host_name = host_name 
        self.location = {}
        self.location["address"] = location["address"]
        self.location["city"] = location["city"]
        self.location["country"] = location["country"]
        self.description = description 
        self.reservations = reservations 
        self.duration = duration 
        self.price = price 
        self.number_of_reviews = number_of_reviews 
        self.review_scores_rating = reviews_score_rating 
        self.mainPicture = mainPicture 
        self.name = name 
        self.reviews = reviews 
        if(_id != ""):
            self._id = _id 

    def getDictToUpload(self):
        return {
            "host_id" : ObjectId(self.host_id) ,
            "host_name" : self.host_name ,
            "location" : self.location ,
            "description" : self.description ,
            "reservations": self.reservations,
            "duration" : self.duration ,
            "price" : self.price ,
            "number_of_reviews" : self.number_of_reviews ,
            "review_scores_rating" : self.review_scores_rating,
            "mainPicture" : self.mainPicture.encode('utf-8'),
            "name" : self.name,
            "reviews": self.reviews
        }