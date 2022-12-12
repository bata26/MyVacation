
class User:
    def __init__(self , _id , username , password ,
        name , surname , type , gender ,
        dateOfBirth , nationality , knownLanguages ,
        reservations , reviews, plaHistory, actHistory):
        self._id = _id
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.type = type
        self.gender = gender
        self.dateOfBirth = dateOfBirth
        self.nationality = nationality
        self.knownLanguages = knownLanguages
        self.reservations = reservations
        self.reviews = reviews
        self.plaHistory = plaHistory
        self.actHistory = actHistory

    def getDictToUpload(self):
        return {
            "_id" : self._id ,
            "username" : self.username ,
            "password" : self.password ,
            "name" : self.name ,
            "surname" : self.surname ,
            "type" : self.type,
            "gender" : self.gender ,
            "dateOfBirth" : self.dateOfBirth ,
            "nationality" : self.nationality ,
            "knownLanguages" : self.knownLanguages ,
            "reservations" : self.reservations ,
            "reviews" : self.reviews ,
            "plaHistory" : self.plaHistory ,
            "actHistory" : self.actHistory
        }