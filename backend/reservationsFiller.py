from controllers.connection import MongoManager
from random import randint
from datetime import datetime , timedelta

client = MongoManager.getInstance()
db = client["myvacation"]
reservationCollection = db["reservations"]
userCollection = db["users"]
accomodationCollection = db["accomodations"]
activityCollection = db["activities"]

START_TIMESTAMP = 1577869341
END_TIMESTAMP = 1704099741
try:
    usersList = list(userCollection.distinct("_id" , {"type" : {"$nin" : ["unregistered" , "admin"]}}))
    print("Fetch degli utenti eseguito")    
except Exception as e:
    print("Impossibile ottenere utenti: " + str(e))


try:
    accomodationList = list(accomodationCollection.find({} , {"_id" : 1 , "price" : 1 , "city" : "$location.city" , "host_id" : 1}))
    print("Fetch delle accomodations eseguito")    
except Exception as e:
    print("Impossibile ottenere utenti: " + str(e))

try:
    activityList = list(activityCollection.find({} , {"_id" : 1 , "price" : 1 , "city" : "$location.city" , "host_id" : 1}))
    print("Fetch delle accomodations eseguito")    
except Exception as e:
    print("Impossibile ottenere utenti: " + str(e))

reservationList = []
for i in range(0 , 1200):
    startTimestamp = randint(START_TIMESTAMP , END_TIMESTAMP)
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
        host_id = activity["host_id"]
    else:
        numberOfDays = randint(0 , 20)
        endDatetime = startDatetime + timedelta(days=numberOfDays)
        accomodation = accomodationList[randint(0 , len(accomodationList) - 1)]
        destinationID = accomodation["_id"]
        totalExpense = accomodation["price"] * (numberOfDays - 1)
        reservation["endDate"] = endDatetime
        city = accomodation["city"]
        type = "accomodation"
        host_id = accomodation["host_id"]
    
    reservation["totalExpense"] = totalExpense
    reservation["destinationID"] = destinationID
    reservation["city"] = city
    reservation["destinationType"] = type
    reservation["hostID"] = host_id

    reservationList.append(reservation)

print("Inserisco nel db")
try:
    reservationCollection.insert_many(reservationList)
except Exception as e:
    print("Impossibile inserire tutte")




