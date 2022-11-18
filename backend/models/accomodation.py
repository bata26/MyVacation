import base64
class Accomodation:
    def __init__(self , _id , name , description , 
        pictures , host_id , host_url , host_name  , 
        host_picture , location , property_type , accommodates , 
        bedrooms , beds , price , minimum_nights , number_of_reviews , 
        review_scores_rating):
        self._id = _id 
        self.name = name 
        self.description = description 
        self.pictures = pictures 
        self.host_id = host_id 
        self.host_url = host_url 
        self.host_name = host_name 
        self.host_picture = host_picture 
        self.location = {}
        self.location["address"] = location["address"] 
        self.location["city"] = location["city"] 
        self.location["country"] = location["country"] 
        self.property_type = property_type 
        self.accommodates = accommodates 
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
            "picture" : base64.encode(self.picture) ,
            "host_id" : self.host_id ,
            "host_url" : self.host_url ,
            "host_name" : self.host_name ,
            "host_picture" : base64.encode(self.host_picture) ,
            "location" : self.location,
            "property_type" : self.property_type ,
            "accommodates" : self.accommodates ,
            "bedrooms" : self.bedrooms ,
            "beds" : self.beds ,
            "price" : self.price ,
            "minimum_nights" : self.minimum_nights ,
            "number_of_reviews" : self.number_of_reviews ,
            "review_scores_rating" : self.review_scores_rating ,
        }
    
    def getDictToResponse(self):
        return {
            "_id" : self._id ,
            "name" : self.name ,
            "description" : self.description ,
            "picture" : self.picture.decode('utf-8'),
            "host_id" : self.host_id ,
            "host_url" : self.host_url ,
            "host_name" : self.host_name ,
            "host_picture" : self.host_picture.decode("utf-8") ,
            "location" : self.location,
            "property_type" : self.property_type ,
            "accommodates" : self.accommodates ,
            "bedrooms" : self.bedrooms ,
            "beds" : self.beds ,
            "price" : self.price ,
            "minimum_nights" : self.minimum_nights ,
            "number_of_reviews" : self.number_of_reviews ,
            "review_scores_rating" : self.review_scores_rating ,
        }