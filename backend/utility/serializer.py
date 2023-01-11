
class Serializer:

    @staticmethod
    def serializeActivity(activity):
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
        if(activity.mainPicture is not None):
            decodedMainPic = activity.mainPicture.decode('utf-8')

        return {
            "_id" : str(activity._id),
            "hostID" : str(activity.hostID),
            "hostName" : activity.hostName ,
            "location" : activity.location ,
            "description" : activity.description ,
            "duration" : activity.duration ,
            "price" : activity.price ,
            "mainPicture" : decodedMainPic,
            "name" : activity.name,
            "approved" : activity.approved,
            "reviews" : serializedReviews,
        }
    
    @staticmethod
    def serializeAccommodation(accommodation):
        pictures = []
        for picture in accommodation.pictures:
            pictures.append(picture.decode('utf-8'))

        serializedReviews = []
        for review in accommodation.reviews:
            serializedReviews.append({
                "userID" : str(review['userID']),
                "score" : review['score'],
                "description" : review['description'],
                "reviewer" : review['reviewer'],
                "_id" : str(review['_id'])
            })
        decodedMainPic = None
        if(accommodation.mainPicture is not None):
            decodedMainPic = accommodation.mainPicture.decode('utf-8')
        return {
            "_id" : str(accommodation._id) ,
            "name" : accommodation.name ,
            "description" : accommodation.description ,
            "pictures" : pictures,
            "hostID" : str(accommodation.hostID) ,
            "hostName" : accommodation.hostName ,
            "location" : accommodation.location,
            "propertyType" : accommodation.propertyType ,
            "guests" : accommodation.guests ,
            "bedrooms" : accommodation.bedrooms ,
            "beds" : accommodation.beds ,
            "price" : accommodation.price ,
            "mainPicture" : decodedMainPic ,
            "approved" : accommodation.approved,
            "reviews" : serializedReviews ,
        }


    @staticmethod
    def serializeReview(review):
        return {
            "_id" : str(review._id),
            "userID" : str(review.userID),
            "destinationID" : str(review.destinationID),
            "score" : review.score ,
            "description" : review.description ,
            "reviewer" : review.reviewer
        }


    @staticmethod
    def serializeUser(user):
        serializedReservations = []
        for reservation in user.reservations:
            tmpReservation = {
                "destinationID" : str(reservation['destinationID']),
                "startDate" : reservation['startDate'],
                "totalExpense" : reservation['totalExpense'],
                "destinationType" : reservation['destinationType'],
                "_id" : str(reservation['_id'])
            }
            if reservation["destinationType"] == "accommodation":
                tmpReservation["endDate"] = reservation["endDate"]
            serializedReservations.append(tmpReservation)
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
        if reservation.destinationType == "accommodation":
            result["endDate"] = reservation.endDate 
        return result
    
    @staticmethod
    def serializeAccommodationNode(accommodationNode):
        return {
            "accommodationID" : accommodationNode.accommodationID,
            "name" : accommodationNode.name,            
            "approved" : accommodationNode.approved,
        }

    @staticmethod
    def serializeActivityNode(activityNode):
        return {
            "activityID" : activityNode.activityID,
            "name" : activityNode.name,            
            "approved" : activityNode.approved,
        }
    
    @staticmethod
    def serializeUserNode(userNode):
        return {
            "userID" : userNode.userID,
            "username" : userNode.username,
        }