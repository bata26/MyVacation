from bson.objectid import ObjectId
class Review:
    def __init__(self , userID , destinationID , score , description, _id = ""):
        self.userID = userID 
        self.destinationID = destinationID 
        self.score = score
        self.description = description
        if(_id != ""):
            self._id = _id

    def getDictToUpload(self):
        result = {
            "userID" : ObjectId(self.userID),
            "destinationID" : ObjectId(self.destinationID),
            "score" : self.score ,
            "description" : self.description,
        }

        if hasattr(self , "_id"):
            result["_id"] = ObjectId(self._id)
        
        return result
    
    def getDictForAdvertisement(self):
        return {
            "userID" : ObjectId(self.userID),
            "score" : self.score ,
            "description" : self.description,
            "_id" : self._id,
        }