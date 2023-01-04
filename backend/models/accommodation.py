import base64
from bson.objectid import ObjectId
class Accommodation:
    def __init__(self, name, description,
                 hostID, hostName, mainPicture,
                 location, propertyType, guests,
                 bedrooms, beds, price, approved, reviews = [], _id="" , pictures=[]):
        self.name = name
        self.description = description
        self.pictures = pictures
        self.hostID = hostID
        self.hostName = hostName
        self.mainPicture = mainPicture
        self.location = {}
        self.location["address"] = location["address"]
        self.location["city"] = location["city"]
        self.location["country"] = location["country"]
        self.propertyType = propertyType
        self.guests = guests
        self.bedrooms = bedrooms
        self.beds = beds
        self.price = price
        self.approved = approved
        self.reviews = reviews
        if (_id != ""):
            self._id = _id

    def getDictToUpload(self):
        binaryMainPicture = self.mainPicture.encode("utf-8")
        pictures = []
        for picture in self.pictures:
            binaryPicture = picture.encode("utf-8")
            pictures.append(binaryPicture)
        return {
            "name": self.name,
            "description": self.description,
            "mainPicture": binaryMainPicture,
            "hostID": ObjectId(self.hostID),
            "hostName": self.hostName,
            "location": self.location,
            "propertyType": self.propertyType,
            "guests": self.guests,
            "bedrooms": self.bedrooms,
            "beds": self.beds,
            "price": self.price,
            "approved": self.approved,
            "pictures": pictures,
            "reservations": self.reservations,
            "reviews": self.reviews
        }
