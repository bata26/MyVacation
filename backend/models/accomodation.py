import base64
from bson.objectid import ObjectId
class Accomodation:
    def __init__(self, name, description,
                 host_id, host_name, mainPicture,
                 location, property_type, accommodates,
                 bedrooms, beds, price, minimum_nights, number_of_reviews,
                 review_scores_rating, approved, reservations = [], reviews = [], _id="" , pictures=[]):
        self.name = name
        self.description = description
        self.pictures = pictures
        self.host_id = host_id
        self.host_name = host_name
        self.mainPicture = mainPicture
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
        self.approved = approved
        self.reservations = reservations
        self.reviews = reviews
        if (_id != ""):
            self._id = _id

    def getDictToUpload(self):
        binaryMainPicture = self.mainPicture.encode("utf-8")
        pictures = []
        for picture in self.pictures:
            binaryPicture = picture.encode("utf-8")
            pictures.append(binaryPicture)
        return {
            "name": self.name,
            "description": self.description,
            "mainPicture": binaryMainPicture,
            "host_id": ObjectId(self.host_id),
            "host_name": self.host_name,
            "location": self.location,
            "property_type": self.property_type,
            "accommodates": self.accommodates,
            "bedrooms": self.bedrooms,
            "beds": self.beds,
            "price": self.price,
            "minimum_nights": self.minimum_nights,
            "number_of_reviews": self.number_of_reviews,
            "review_scores_rating": self.review_scores_rating,
            "approved": self.approved,
            "pictures": pictures,
            "reservations": self.reservations,
            "reviews": self.reviews
        }
