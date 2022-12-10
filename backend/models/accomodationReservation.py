class AccomodationReservation:
    def __init__(self , userID , destinationID , destinationType  , startDate , endDate , totalExpense, _id=""):
        self.userID = userID
        self.destinationID = destinationID
        self.destinationType = destinationType
        self.startDate = startDate
        self.endDate = endDate
        self.totalExpense = totalExpense
        if not(_id == ""):
            self._id = _id
    
    def getDictToUpload(self):
        return{
            "userID" : self.userID,
            "destinationID" : self.destinationID,
            "destinationType" : self.destinationType,
            "startDate" : self.startDate,
            "endDate" : self.endDate,
            "totalExpense" : self.totalExpense
        }