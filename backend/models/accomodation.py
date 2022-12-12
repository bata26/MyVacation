import base64
class Accomodation:
    def __init__(self , name , description , 
        pictures , host_id , host_url , host_name  , mainPicture , 
        host_picture , location , property_type , accommodates , 
        bedrooms , beds , price , minimum_nights , number_of_reviews , 
        review_scores_rating ,_id = ""):
        self.name = name 
        self.description = description 
        self.pictures = pictures 
        self.host_id = host_id 
        self.host_url = host_url 
        self.host_name = host_name 
        self.mainPicture = mainPicture 
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
        if(_id != ""):
            self._id = _id
    
    def getDictToUpload(self):
        binaryMainPicture = self.mainPicture.encode("ascii")
        pictures = []
        for picture in self.pictures:
            binaryPicture = picture.encode("ascii")
            pictures.append(binaryPicture)
        return {
            "name" : self.name ,
            "description" : self.description ,
            "mainPicture" : binaryMainPicture,
            "host_id" : self.host_id ,
            "host_url" : self.host_url ,
            "host_name" : self.host_name ,
            "host_picture" : self.host_picture,
            "location" : self.location,
            "property_type" : self.property_type ,
            "accommodates" : self.accommodates ,
            "bedrooms" : self.bedrooms ,
            "beds" : self.beds ,
            "price" : self.price ,
            "minimum_nights" : self.minimum_nights ,
            "number_of_reviews" : self.number_of_reviews ,
            "review_scores_rating" : self.review_scores_rating ,
            "pictures" : pictures ,
        }