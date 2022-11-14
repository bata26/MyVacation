import base64
class Serializer:

    @staticmethod
    def serializeActivity(activity):
        return {
            "_id" : activity._id ,
            "host_id" : activity.host_id ,
            "host_url" : activity.host_url ,
            "host_name" : activity.host_name ,
            "host_picture" : activity.host_picture.decode("utf-8") ,
            "location" : activity.location ,
            "description" : activity.description ,
            "prenotations" : activity.prenotations ,
            "duration" : activity.duration ,
            "pricePerPerson" : activity.pricePerPerson ,
            "number_of_reviews" : activity.number_of_reviews ,
            "review_scores_rating" : activity.review_scores_rating
        }
    
    @staticmethod
    def serializeAccomodation(accomodation):
        return {
            "_id" : accomodation._id ,
            "name" : accomodation.name ,
            "description" : accomodation.description ,
            "picture" : accomodation.picture.decode('utf-8'),
            "host_id" : accomodation.host_id ,
            "host_url" : accomodation.host_url ,
            "host_name" : accomodation.host_name ,
            "host_picture" : accomodation.host_picture.decode("utf-8") ,
            "location" : accomodation.location,
            "property_type" : accomodation.property_type ,
            "accommodates" : accomodation.accommodates ,
            "bedrooms" : accomodation.bedrooms ,
            "beds" : accomodation.beds ,
            "price" : accomodation.price ,
            "minimum_nights" : accomodation.minimum_nights ,
            "number_of_reviews" : accomodation.number_of_reviews ,
            "review_scores_rating" : accomodation.review_scores_rating ,
        }