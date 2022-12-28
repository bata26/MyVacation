from bson.objectid import ObjectId
class Serializer:

    @staticmethod
    def serializeActivity(activity):
        serializedReservations = []
        for reservation in activity.reservations:
            serializedReservations.append({
                "userID" : str(reservation['userID']),
                "startDate" : reservation['startDate'],
                "totalExpense" : reservation['totalExpense'],
                "_id" : str(reservation['_id'])
            })

        serializedReviews = []
        for review in activity.reviews:
            serializedReviews.append({
                "userID" : str(review['userID']),
                "score" : review['score'],
                "description" : review['description'],
                "reviewer" : review['reviewer'],
                "_id" : str(review['_id'])
            })
        decodedMainPic = None
        if(activity.mainPicture != None):
            decodedMainPic = activity.mainPicture.decode('utf-8')

        return {
            "_id" : str(activity._id),
            "host_id" : str(activity.host_id),
            "host_name" : activity.host_name ,
            "location" : activity.location ,
            "description" : activity.description ,
            "reservations" : serializedReservations ,
            "duration" : activity.duration ,
            "price" : activity.price ,
            "number_of_reviews" : activity.number_of_reviews ,
            "review_scores_rating" : activity.review_scores_rating,
            "mainPicture" : decodedMainPic,
            "name" : activity.name,
            "approved" : activity.approved,
            "reviews" : serializedReviews,
        }
    
    @staticmethod
    def serializeAccomodation(accomodation):
        pictures = []
        for picture in accomodation.pictures:
            pictures.append(picture.decode('utf-8'))

        serializedReservations = []
        for reservation in accomodation.reservations:
            serializedReservations.append({
                "userID" : str(reservation['userID']),
                "startDate" : reservation['startDate'],
                "endDate" : reservation['endDate'],
                "totalExpense" : reservation['totalExpense'],
                "_id" : str(reservation['_id'])
            })

        serializedReviews = []
        for review in accomodation.reviews:
            serializedReviews.append({
                "userID" : str(review['userID']),
                "score" : review['score'],
                "description" : review['description'],
                "reviewer" : review['reviewer'],
                "_id" : str(review['_id'])
            })
        decodedMainPic = None
        if(accomodation.mainPicture != None):
            decodedMainPic = accomodation.mainPicture.decode('utf-8')
        return {
            "_id" : str(accomodation._id) ,
            "name" : accomodation.name ,
            "description" : accomodation.description ,
            "pictures" : pictures,
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
            "mainPicture" : decodedMainPic ,
            "approved" : accomodation.approved,
            "reservations" : serializedReservations ,
            "reviews" : serializedReviews ,
        }


    @staticmethod
    def serializeReview(review):
        return {
            "_id" : str(review._id),
            "reviewerID" : str(review.userID),
            "destinationID" : str(review.destinationID),
            "score" : review.score ,
            "description" : review.description ,
            "reviewer" : review.reviewer
        }


    @staticmethod
    def serializeUser(user):
        serializedReservations = []
        for reservation in user.reservations:
            serializedReservations.append({
                "destinationID" : str(reservation['destinationID']),
                "startDate" : reservation['startDate'],
                "totalExpense" : reservation['totalExpense'],
                "_id" : str(reservation['_id'])
            })
            if hasattr(reservation , "endDate"):
                serializedReservations['endDate'] = reservation['endDate']
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
            "reservations" : serializedReservations,
            "registrationDate" : user.registrationDate
        }

    @staticmethod
    def serializeReservation(reservation):
        result = {
            "_id" : str(reservation._id) ,
            "userID" : str(reservation.userID) ,
            "destinationID" : str(reservation.destinationID),
            "destinationType" : reservation.destinationType ,
            "startDate" : reservation.startDate ,
            "totalExpense" : reservation.totalExpense,
            "city" : reservation.city,
            "hostID" : str(reservation.hostID),
        }
        if reservation.destinationType == "accomodation":
            result["endDate"] = reservation.endDate 
        return result
            