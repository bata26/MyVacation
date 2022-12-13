from bson.objectid import ObjectId
class ActivityReservation:
    def __init__(self , userID , destinationID , destinationType  , startDate , totalExpense, _id=""):
        self.userID = userID
        self.destinationID = destinationID
        self.destinationType = destinationType
        self.startDate = startDate
        self.totalExpense = totalExpense
        if not(_id == ""):
            self._id = _id
    
    def getDictToUpload(self):
        result = {
            "userID" : ObjectId(self.userID),
            "destinationID" : ObjectId(self.destinationID),
            "destinationType" : self.destinationType,
            "startDate" : self.startDate,
            "totalExpense" : self.totalExpense
        }

        if hasattr(self , "_id"):
            result["_id"] = ObjectId(self._id)
        
        return result
    
    def getDictForAdvertisement(self):
        return {
            "userID" : ObjectId(self.userID),
            "startDate" : self.startDate,
            "totalExpense" : self.totalExpense,
            "_id" : self._id,
        }