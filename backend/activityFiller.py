from utility.connection import MongoManager
import random
from bson.objectid import ObjectId
import base64
import pandas as pd
import dateparser
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
imgPath = "utility/testImg/art.jpg"

def getHostList():
    client = MongoManager.getInstance()
    db = client["myvacation"]
    collection = db["users"]

    hostList = list(collection.find({"type" : "host"} , {"_id" : 1 , "name" : 1}))
    return hostList


def getCitiesList():
    client = MongoManager.getInstance()
    db = client["myvacation"]
    collection = db["accommodations"]

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
    collection = db["accommodations"]
    hostID = hostList[random.randint(0 , len(hostList) - 1)]
    cursor = dict(collection.find_one({"_id" : hostID}))
    activity = categories[random.randint(0 , len(categories) - 1)]
    duration = durations[random.randint(0 , len(durations) - 1)]
    price = prices[random.randint(0 , len(prices) - 1)]

    base64Picture = encodeBase64Image(activity["img_path"])

    activity = {
        "hostID" : hostID,
        "hostName" : cursor["hostName"],
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
print(f"hostList ottenuta : {hostList}")
cityList = getCitiesList()
print("cityList ottenuta")
client = MongoManager.getInstance()
db = client["myvacation"]
collection = db["activities"]
activities = []

photos = []

filePath = "/Users/lorenzobataloni/Downloads/activities.csv"
dataframe = pd.read_csv(filePath ,  on_bad_lines='skip' , sep=";")
print(dataframe)


EVENT = 1
START_DATE = 2
END_DATE = 3
DESC = 4
ADDRESS = 5
counter = 0

activities = []
for row in dataframe.iterrows():
    if counter == 1200:
        break
    counter += 1
    
    row = row[EVENT].to_dict()
    print(row)
    host = hostList[random.randint(0  ,len(hostList) - 1)]
    duration = dateparser.parse(row["END_DATE_T"]) - dateparser.parse(row["START_DATE"])
    activity = {
        "name" : row["EVENT"],
        "description" : row["EVENT_DESC"],
        "location" : {
            "address" : row["FULLADDRES"],
            "city" : cityList[random.randint(0  ,len(cityList) - 1)],
            "country" : "Italy",
        },
        "price" : prices[random.randint(0 , len(prices) - 1)],
        "duration" : durations[random.randint(0 , len(durations) - 1)],
        "hostID"  :str(host["_id"]),
        "hostName" : host["name"],
        "reviews" : [],
        "approved"  :True,
        "mainPicture":encodeBase64Image(imgPath)
    }
    activities.append(activity)

collection.insert_many(activities)



#print(f"post inserimento : {res}")

    