from bson.objectid import ObjectId
class Reservation:
    def __init__(self , userID , destinationID , destinationType  , startDate , totalExpense, city, hostID, endDate="", _id=""):
        self.userID = userID
        self.destinationID = destinationID
        self.destinationType = destinationType
        self.startDate = startDate
        self.totalExpense = totalExpense
        self.city = city
        self.hostID = hostID
        if not(_id == ""):
            self._id = _id
        if not(endDate == ""):
            self.endDate = endDate
    
    def getDictToUpload(self):
        result = {
            "userID" : ObjectId(self.userID),
            "destinationID" : ObjectId(self.destinationID),
            "destinationType" : self.destinationType,
            "startDate" : self.startDate,
            "totalExpense" : self.totalExpense,
            "city" : self.city,
            "hostID" : ObjectId(self.hostID),
        }
        if hasattr(self , "_id"):
            result["_id"] = ObjectId(self._id)
        if hasattr(self , "endDate"):
            result["endDate"] = self.endDate
        
        return result
    
    def getDictForAdvertisement(self):
        result = {
            "userID" : ObjectId(self.userID),
            "startDate" : self.startDate,
            "totalExpense" : self.totalExpense
        }
        if hasattr(self , "_id"):
            result["_id"] = ObjectId(self._id)
        if hasattr(self , "endDate"):
            result["endDate"] = self.endDate
        return result

    def getDictForUser(self):
        result = {
            "destinationID" : ObjectId(self.destinationID),
            "destinationType" : self.destinationType,
            "startDate" : self.startDate,
            "totalExpense" : self.totalExpense
        }
        if hasattr(self , "_id"):
            result["_id"] = ObjectId(self._id)
        if hasattr(self , "endDate"):
            result["endDate"] = self.endDate
        return result