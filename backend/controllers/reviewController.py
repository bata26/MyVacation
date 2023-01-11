from managers.reviewManager import ReviewManager

# This class contains methods reguarding the Reviews behavior. Methods described here 
# are responsible for calling the underlay layer (Manager) and perform CRUD operations.
class ReviewController:

    @staticmethod
    def getReviewByID(reviewID):
        try:
            result = ReviewManager.getReviewFromID(reviewID)
            return result
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def getReviewByDestinationID(destinationID):
        try:
            result = ReviewManager.getReviewFromDestinationID(destinationID)
            return result
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def deleteReview(reviewID, destinationID, destinationType, user):
        try:
            ReviewManager.deleteReview(reviewID, destinationID, destinationType, user)
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def checkIfCanReview(destinationID, user):
        try:
            return ReviewManager.checkIfCanReview(str(destinationID), user)
        except Exception as e:
            raise Exception(str(e))