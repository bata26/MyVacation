
class User:
    def __init__(self , _id , username , password ,
        name , type , surname , gender ,
        dateOfBirth , nationality , knownLanguages ,
        prenotations , reviews, plaHistory, actHistory):
        self._id = _id
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.type = type
        self.description = description
        self.gender = gender
        self.dateOfBirth = dateOfBirth
        self.nationality = nationality
        self.knownLanguages = knownLanguages
        self.prenotations = prenotations
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
            "type" : type,
            "description" : self.description ,
            "gender" : self.gender ,
            "dateOfBirth" : self.dateOfBirth ,
            "nationality" : self.nationality ,
            "knownLanguages" : self.knownLanguages ,
            "prenotations" : self.prenotations ,
            "reviews" : self.reviews ,
            "plaHistory" : self.plaHistory ,
            "actHistory" : self.actHistory
        }