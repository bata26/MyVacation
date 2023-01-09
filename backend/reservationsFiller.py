from utility.connection import MongoManager
from random import randint
from datetime import datetime , timedelta
from bson.objectid import ObjectId
import random


client = MongoManager.getInstance()
db = client["myvacation"]
reservationCollection = db["reservations"]
userCollection = db["users"]
accommodationCollection = db["accommodations"]
activityCollection = db["activities"]

START_TIMESTAMP = 1577869341
END_TIMESTAMP = 1704099741
try:
    usersList = list(userCollection.distinct("_id" , {"type" : {"$nin" : ["unregistered" , "admin"]}}))
    print("Fetch degli utenti eseguito")    
except Exception as e:
    print("Impossibile ottenere utenti: " + str(e))


try:
    accommodationList = list(accommodationCollection.find({} , {"_id" : 1 , "price" : 1 , "city" : "$location.city" , "hostID" : 1}))
    print("Fetch delle accommodations eseguito")    
except Exception as e:
    print("Impossibile ottenere utenti: " + str(e))

try:
    activityList = list(activityCollection.find({} , {"_id" : 1 , "price" : 1 , "city" : "$location.city" , "hostID" : 1}))
    print("Fetch delle accommodations eseguito")    
except Exception as e:
    print("Impossibile ottenere utenti: " + str(e))

reservationList = []
lastTimestamp = START_TIMESTAMP
for i in range(0 , 1200):
    startTimestamp = lastTimestamp + 86400 # aggiungo un giorno
    startDatetime = datetime.fromtimestamp(startTimestamp).replace(hour=0, minute=0, second=0)

    reservation = {}
    reservation = {
        "userID" : usersList[randint(0 , len(usersList) - 1)],
        "startDate" : startDatetime
    }

    if(i % 5 == 0): #activity
        activity = activityList[randint(0 , len(activityList) - 1)]
        destinationID = activity["_id"]
        totalExpense = activity["price"]
        city = activity["city"]
        type = "activity"
        hostID = activity["hostID"]
    else:
        numberOfDays = randint(0 , 20)
        endDatetime = startDatetime + timedelta(days=numberOfDays)
        lastTimestamp = endDatetime.timestamp()
        accommodation = accommodationList[randint(0 , len(accommodationList) - 1)]
        destinationID = accommodation["_id"]
        totalExpense = accommodation["price"] * (numberOfDays - 1)
        reservation["endDate"] = endDatetime
        city = accommodation["city"]
        type = "accommodation"
        hostID = accommodation["hostID"]
    
    reservation["totalExpense"] = totalExpense
    reservation["destinationID"] = destinationID
    reservation["city"] = city
    reservation["destinationType"] = type
    reservation["hostID"] = hostID

    userID = str(hostID)
    while(str(userID) == str(hostID)):
        userID = usersList[random.randint( 0 , len(usersList) - 1)]
    reservation["userID"] = userID
    print(reservation)
    reservationList.append(reservation)


try:
    with client.start_session() as session:
        with session.start_transaction():
            reservationCollection.insert_many(reservationList , session=session)
            
            
            for reservation in reservationList:
                userID = str(reservation["userID"])
                toInsertReservation = reservation
                toInsertReservation.pop("userID")
                
                userCollection.update_one({"_id" : ObjectId(userID)} ,  {"$push" : {"reservations" : toInsertReservation}} , session=session)
except Exception as e:
    print("Impossibile inserire tutte : " + str(e))

