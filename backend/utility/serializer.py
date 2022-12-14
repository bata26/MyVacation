from bson.objectid import ObjectId
class Serializer:

    @staticmethod
    def serializeActivity(activity):
        return {
            "_id" : str(activity._id),
            "host_id" : str(activity.host_id),
            "host_name" : activity.host_name ,
            "location" : activity.location ,
            "description" : activity.description ,
            "reservations" : activity.reservations ,
            "duration" : activity.duration ,
            "price" : activity.price ,
            "number_of_reviews" : activity.number_of_reviews ,
            "review_scores_rating" : activity.review_scores_rating,
            "mainPicture" : activity.mainPicture.decode("utf-8"),
            "name" : activity.name,
            "reviews" : activity.reviews,
        }
    
    @staticmethod
    def serializeAccomodation(accomodation):
        pictures = []
        for picture in accomodation.pictures:
            pictures.append(picture.decode('utf-8'))
        return {
            "_id" : str(accomodation._id) ,
            "name" : accomodation.name ,
            "description" : accomodation.description ,
            "pictures" : pictures, # accomodation.pictures,#.decode('utf-8'),
            "host_id" : str(accomodation.host_id) ,
            "host_name" : accomodation.host_name ,
            "location" : accomodation.location,
            "property_type" : accomodation.property_type ,
            "accommodates" : accomodation.accommodates ,
            "bedrooms" : accomodation.bedrooms ,
            "beds" : accomodation.beds ,
            "price" : accomodation.price ,
            "minimum_nights" : accomodation.minimum_nights ,
            "number_of_reviews" : accomodation.number_of_reviews ,
            "review_scores_rating" : accomodation.review_scores_rating ,
            "mainPicture" : accomodation.mainPicture.decode('utf-8') ,
            "reservations" : accomodation.reservations ,
            "reviews" : accomodation.reviews ,
        }


    @staticmethod
    def serializeReview(review):
        return {
            "_id" : str(review._id),
            "reviewerID" : str(review.reviewerID),
            "destinationID" : str(review.destinationID),
            "host_name" : review.host_name ,
            "score" : review.score ,
            "comment" : review.comment 
        }


    @staticmethod
    def serializeUser(user):
        return {
            "_id" : str(user._id),
            "username" : user.username ,
            "name" : user.name,
            "surname" : user.surname ,
            "type" : user.type ,
            "gender" : user.gender ,
            "dateOfBirth" : user.dateOfBirth,
            "nationality" : user.nationality ,
            "knownLanguages" : user.knownLanguages ,
            "reservations" : user.reservations 
        }

    @staticmethod
    def serializeToApprove(toApprove):
        return {
            "_id" : str(toApprove._id),
            "name" : toApprove.name,
            "host_id" : str(toApprove.host_id),
            "location" : toApprove.location,
            "type" : toApprove.type
        }

    @staticmethod
    def serializeReservation(reservation):
        if reservation.destinationType == "activity":
            return {
            "_id" : str(reservation._id) ,
            "userID" : str(reservation.userID) ,
            "destinationID" : str(reservation.destinationID),
            "destinationType" : reservation.destinationType ,
            "startDate" : reservation.startDate ,
            "totalExpense" : reservation.totalExpense,
            }
        else:
            return {
            "_id" : str(reservation._id) ,
            "userID" : str(reservation.userID) ,
            "destinationID" : str(reservation.destinationID),
            "destinationType" : reservation.destinationType ,
            "startDate" : reservation.startDate ,
            "endDate" : reservation.endDate ,
            "totalExpense" : reservation.totalExpense,
            }
            