from bson.objectid import ObjectId

class User:
    def __init__(self ,username , password ,
        name , surname , type , gender ,
        dateOfBirth , nationality , knownLanguages ,
        reservations , registrationDate, _id=""):
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
        self.registrationDate = registrationDate
        if(_id != ""):
            self._id = _id

    def getDictToUpload(self):
        result = {
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
            "registrationDate" : self.registrationDate
        }

        if hasattr(self , "_id"):
            result["_id"] = ObjectId(self._id)

        return result