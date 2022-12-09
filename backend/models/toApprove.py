class ToApprove:
    def __init__(self , _id , name , host_id, location, type):
        self._id = _id
        self.name = name
        self.host_id = host_id
        self.location = {}
        self.location["address"] = location["address"]
        self.location["city"] = location["city"]
        self.location["country"] = location["country"]
        self.type = type

    def getDictToUpload(self):
        return {
            "_id" : self._id ,
            "name" : self.name ,
            "host_id" : self.host_id ,
            "location" : self.location,
            "type" : self.type
        }