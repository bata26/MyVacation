import os
from bson.objectid import ObjectId

class Accomodation:
    def __init__(self , _id , name , description , 
        picture_url , host_id , host_url , host_name , host_since , 
        host_picture_url , location , property_type , accommodates , 
        bathrooms , bedrooms , beds , price , minimum_nights , number_of_reviews , 
        review_scores_rating):
        self._id = _id 
        self.name = name 
        self.description = description 
        self.picture_url = picture_url 
        self.host_id = host_id 
        self.host_url = host_url 
        self.host_name = host_name 
        self.host_since = host_since 
        self.host_picture_url = host_picture_url 
        self.location.address = location.address 
        self.location.city = location.city 
        self.location.nation = location.nation 
        self.property_type = property_type 
        self.accommodates = accommodates 
        self.bathrooms = bathrooms 
        self.bedrooms = bedrooms 
        self.beds = beds 
        self.price = price 
        self.minimum_nights = minimum_nights 
        self.number_of_reviews = number_of_reviews 
        self.review_scores_rating = review_scores_rating 
    
    def getDictToUpload(self):
        return {
            "_id" : self._id ,
            "name" : self.name ,
            "description" : self.description ,
            "picture_url" : self.picture_url ,
            "host_id" : self.host_id ,
            "host_url" : self.host_url ,
            "host_name" : self.host_name ,
            "host_since" : self.host_since ,
            "host_picture_url" : self.host_picture_url ,
            "location" : self.location,
            "property_type" : self.property_type ,
            "accommodates" : self.accommodates ,
            "bathrooms" : self.bathrooms ,
            "bedrooms" : self.bedrooms ,
            "beds" : self.beds ,
            "price" : self.price ,
            "minimum_nights" : self.minimum_nights ,
            "number_of_reviews" : self.number_of_reviews ,
            "review_scores_rating" : self.review_scores_rating ,
        }