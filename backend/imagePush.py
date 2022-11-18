import base64
from controllers.connection import MongoManager

base64Imgs = []

for i in range(1 , 5):
    with open(f"utility/testImg/casa{i}.jpg", "rb") as img_file:
        base64Imgs.append(base64.b64encode(img_file.read()))
print(len(base64Imgs))
client = MongoManager.getInstance()
db = client["myvacation"]
collection = db["accomodations"]

accomodationsList = list(collection.find({}))
counter = 0 
for accomodation in accomodationsList:
    actualImgs = base64Imgs
    #actualImgs.append(accomodation["picture"])
    for img in actualImgs:
        collection.update_one({"_id" : accomodation["_id"]} ,{"$push" :{"pictures" : img}})
    print(f"Effettuato aggiornamento {counter}")
    counter += 1
collection.update_one({} ,{"$unset" :{"picture" : 1}})
