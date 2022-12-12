import base64

class Activity:
    def __init__(self , host_id , host_url , 
        host_name  , host_picture , location , description , 
        reservations , duration , price , 
        number_of_reviews , reviews_score_rating , mainPicture , name , _id=""):
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
        if(_id != ""):
            self._id = _id 

    def getDictToUpload(self):
        return {
            "host_id" : self.host_id ,
            "host_url" : self.host_url ,
            "host_name" : self.host_name ,
            "host_picture" : self.host_picture,
            "location" : self.location ,
            "description" : self.description ,
            "reservations" : self.reservations ,
            "duration" : self.duration ,
            "price" : self.price ,
            "number_of_reviews" : self.number_of_reviews ,
            "review_scores_rating" : self.review_scores_rating,
            "mainPicture" : self.mainPicture.encode("ascii"),
            "name" : self.name,
        }