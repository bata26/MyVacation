import base64

class Activity:
    def __init__(self , _id , host_id , host_url , 
        host_name  , host_picture , location , description ,
        reservations , duration , price ,
        number_of_reviews , reviews_score_rating , mainPicture , name):
        self._id = _id 
        self.host_id = host_id 
        self.host_url = host_url 
        self.host_name = host_name 
        self.host_picture = host_picture
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

    def getDictToUpload(self):
        return {
            "_id" : self._id ,
            "host_id" : self.host_id ,
            "host_url" : self.host_url ,
            "host_name" : self.host_name ,
            "host_picture" : base64.encode(self.host_picture),
            "location" : self.location ,
            "description" : self.description ,
            "reservations" : self.reservations ,
            "duration" : self.duration ,
            "price" : self.price ,
            "number_of_reviews" : self.number_of_reviews ,
            "review_scores_rating" : self.review_scores_rating,
            "mainPicture" : base64.encode(self.mainPicture),
            "name" : self.name,
        }