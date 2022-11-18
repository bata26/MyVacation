
class Review:
    def __init__(self , _id , reviewerID , destinationID , 
        host_name  , score , comment):
        self._id = _id 
        self.revieweID = reviewerID 
        self.destinationID = destinationID 
        self.host_name = host_name 
        self.score = score
        self.comment = comment

    def getDictToUpload(self):
        return {
            "_id" : self._id ,
            "reviewerID" : self.revieweID ,
            "destinationID" : self.destinationID ,
            "host_name" : self.host_name ,
            "score" : self.score ,
            "comment" : self.comment
        }