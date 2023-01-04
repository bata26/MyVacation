import base64
from bson.objectid import ObjectId


class Activity:
    def __init__(self , hostID  , 
        hostName  , location , description , 
        duration , price , mainPicture , name , approved, reviews=[], _id=""):
        self.hostID = hostID 
        self.hostName = hostName 
        self.location = {}
        self.location["address"] = location["address"]
        self.location["city"] = location["city"]
        self.location["country"] = location["country"]
        self.description = description 
        self.duration = duration 
        self.price = price 
        self.mainPicture = mainPicture
        self.name = name
        self.approved = approved
        self.reviews = reviews
        if(_id != ""):
            self._id = _id 

    def getDictToUpload(self):
        return {
            "hostID" : ObjectId(self.hostID) ,
            "hostName" : self.hostName ,
            "location" : self.location ,
            "description" : self.description ,
            "duration" : self.duration ,
            "price" : self.price ,
            "mainPicture" : self.mainPicture.encode('utf-8'),
            "name" : self.name,
            "reviews": self.reviews,
            "approved": self.approved
        }