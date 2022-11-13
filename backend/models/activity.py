class Activity:
    def __init__(self , _id , host_id , host_url , 
        host_name , host_since , host_picture_url , location , description , 
        prenotations , duration , pricePerPerson , 
        number_of_reviews , reviews_score_rating):
        self._id = _id 
        self.host_id = host_id 
        self.host_url = host_url 
        self.host_name = host_name 
        self.host_since = host_since 
        self.host_picture_url = host_picture_url 
        self.location.address = location.address 
        self.location.city = location.city 
        self.location.nation = location.nation 
        self.description = description 
        self.prenotations = prenotations 
        self.duration = duration 
        self.pricePerPerson = pricePerPerson 
        self.number_of_reviews = number_of_reviews 
        self.review_scores_rating = reviews_score_rating 

    def getDictToUpload(self):
        return {
            "_id" : self._id ,
            "host_id" : self.host_id ,
            "host_url" : self.host_url ,
            "host_name" : self.name ,
            "host_since" : self.host_since ,
            "host_picture_url" : self.host_picture_url ,
            "location" : self.location ,
            "description" : self.description ,
            "prenotations" : self.prenotations ,
            "duration" : self.duration ,
            "pricePerPerson" : self.pricePerPerson ,
            "number_of_reviews" : self.number_of_reviews ,
            "review_scores_rating" : self.review_scores_rating
        }