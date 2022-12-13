
class User:
    def __init__(self ,username , password ,
        name , surname , type , gender ,
        dateOfBirth , nationality , knownLanguages ,
        reservations , _id=""):
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
        }