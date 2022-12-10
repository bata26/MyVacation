class ActivityReservation:
    def __init__(self , userID , destinationID , destinationType  , startDate , totalExpense):
        self.userID = userID
        self.destinationID = destinationID
        self.destinationType = destinationType
        self.startDate = startDate
        self.totalExpense = totalExpense
    
    def getDictToUpload(self):
        return{
            "userID" : self.userID,
            "destinationID" : self.destinationID,
            "destinationType" : self.destinationType,
            "startDate" : self.startDate,
            "totalExpense" : self.totalExpense
        }