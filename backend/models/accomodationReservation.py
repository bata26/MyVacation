class AccomodationReservation:
    def __init__(self , userID , destinationID , destinationType  , startDate , endDate , totalExpense):
        self.userID = userID
        self.destinationID = destinationID
        self.destinationType = destinationType
        self.startDate = startDate
        self.endDate = endDate
        self.totalExpense = totalExpense
    
    def getDictToUpload(self):
        return{
            "userID" : self.userID,
            "destinationID" : self.destinationID,
            "destinationType" : self.destinationType,
            "startDate" : self.startDate,
            "endDate" : self.endDate,
            "totalExpense" : self.totalExpense
        }