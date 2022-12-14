from controllers.connection import MongoManager
import random
from bson.objectid import ObjectId
import base64
categories = [
    {
        "type" : "kayak",
        "img_path" :"utility/testImg/kayak.jpg" ,  
        "description" : "Immergiti nella natura ed esplora grazie ad un'esperienza in kayak"
    }, 
    {
        "type" : "climbing" ,
        "img_path" :"utility/testImg/climbing.jpg" , 
        "description" : "Sfida i tuoi limiti scoprendo l'arrampicata sportiva" 
    }, 
    {
        "type" : "art show" ,
        "img_path" :"utility/testImg/art.jpg" ,  
        "description" : "Catapultati in un mondo a regola d'arte grazie alla nostra mostra!"
    },
    {
        "type" : "museum" ,
        "img_path" :"utility/testImg/museum.jpg" , 
        "description" : "Visita uno dei musei più premiati al mondo" 
    }, 
    {
        "type" : "food",
        "img_path" :"utility/testImg/food.jpg" ,
        "description" : "Vivi un'esperienza culinaria indimenticabile presso un ristorante stellato!"
    }]

prices = [10 , 15 , 25 , 32 , 50 , 80 , 100]
durations = [1 , 2 , 4 , 3.5 , 6]
hostList = []
cityList = []

def getHostList():
    client = MongoManager.getInstance()
    db = client["myvacation"]
    collection = db["accomodations"]

    hostList = collection.distinct("_id" , {})
    return hostList


def getCitiesList():
    client = MongoManager.getInstance()
    db = client["myvacation"]
    collection = db["accomodations"]

    hostList = collection.distinct("location.city" , {})
    return hostList

def encodeBase64Image(imagePath):
    res = None
    with open(imagePath, "rb") as img_file:
        res = base64.b64encode(img_file.read())
    return res

def generateRandomActivity():
    global hostList , cityList

    client = MongoManager.getInstance()
    db = client["myvacation"]
    collection = db["accomodations"]
    hostID = hostList[random.randint(0 , len(hostList) - 1)]
    cursor = dict(collection.find_one({"_id" : hostID}))
    activity = categories[random.randint(0 , len(categories) - 1)]
    duration = durations[random.randint(0 , len(durations) - 1)]
    price = prices[random.randint(0 , len(prices) - 1)]

    base64Picture = encodeBase64Image(activity["img_path"])

    activity = {
        "host_id" : hostID,
        "host_name" : cursor["host_name"],
        "location" : {
         "address" :cursor["location"]["address"],
         "city" : cursor["location"]["city"],
         "country" :cursor["location"]["country"],
        },
        "description" : activity["description"],
        "picture" : base64Picture,
        "category" : activity["type"],
        "reservations" : [],
        "duration" : duration , 
        "price" : price,
        "number_of_reviews" : random.randint(0 , 20),
        "review_scores_rating" : random.randint(0 , 5)
    }

    return activity


hostList = getHostList()
print(f"hostList ottenuta")
cityList = getCitiesList()
print("cityList ottenuta")
client = MongoManager.getInstance()
db = client["myvacation"]
collection = db["activities"]
activities = []
for i in range(0 , 150):
    activity = generateRandomActivity()
    activities.append(activity)

res = collection.insert_many(activities)
print(f"post inserimento : {res}")

    