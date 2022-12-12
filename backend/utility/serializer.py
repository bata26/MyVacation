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
            "reservations" : activity.reservations ,
            "duration" : activity.duration ,
            "price" : activity.price ,
            "number_of_reviews" : activity.number_of_reviews ,
            "review_scores_rating" : activity.review_scores_rating,
            "mainPicture" : activity.mainPicture.decode("utf-8"),
            "name" : activity.name,
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
            "mainPicture" : accomodation.mainPicture.decode('utf-8') ,
        }


    @staticmethod
    def serializeReview(review):
        return {
            "_id" : str(review._id),
            "reviewerID" : review.reviewerID ,
            "destinationID" : review.destinationID ,
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
            "reservations" : user.reservations ,
            "reviews" : user.reviews ,
            "plaHistory" : user.plaHistory ,
            "actHistory" : user.actHistory,
            "picture" : user.picture.decode("utf-8") if hasattr(user , "picture") else "",
        }

    @staticmethod
    def serializeToApprove(toApprove):
        return {
            "_id" : toApprove._id ,
            "name" : toApprove.name,
            "host_id" : toApprove.host_id ,
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
            