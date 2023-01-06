from managers.reviewManager import ReviewManager

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
            result = ReviewManager.deleteReview(reviewID, destinationID, destinationType, user)
            return result
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def checkIfCanReview(destinationID, destinationType, user):
        try:
            return ReviewManager.checkIfCanReview(str(destinationID), destinationType, user)
        except Exception as e:
            raise Exception(str(e))