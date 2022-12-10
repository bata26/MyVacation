
class Review:
    def __init__(self , userID , destinationID , 
                    score , description):
        self.userID = userID 
        self.destinationID = destinationID 
        self.score = score
        self.description = description

    def getDictToUpload(self):
        return {
            "userID" : self.userID ,
            "destinationID" : self.destinationID ,
            "score" : self.score ,
            "description" : self.description
        }