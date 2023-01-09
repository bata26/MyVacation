from utility.connection import MongoManager
from random import randint
from datetime import datetime , timedelta
from bson.objectid import ObjectId
from random import randint


client = MongoManager.getInstance()
db = client["myvacation"]
reviewCollection = db["reviews"]
userCollection = db["users"]
accommodationCollection = db["accommodations"]
activityCollection = db["activities"]
reservationCollection = db["reservations"]

START_TIMESTAMP = 1577869341
END_TIMESTAMP = 1704099741
try:
    usersList = list(userCollection.find({"type" : {"$nin" : ["unregistered" , "admin"]}} , {"_id" : 1 , "username" : 1}))
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

try:
    reservationList = list(reservationCollection.find({} , {"_id" : 1 , "price" : 1 , "city" : "$location.city" , "hostID" : 1 , "userID" : 1 , "destinationID"  :1 , "destinationType" : 1}))
    print("Fetch delle accommodations eseguito")    
except Exception as e:
    print("Impossibile ottenere utenti: " + str(e))

def getUsernameFromID(userID):
    global usersList
    for user in usersList:
        if(str(user["_id"]) == userID):
            return user["username"]

comments = [
{
    "score" : 0.5,
    "comment" : "Terrible"

},
{
    "score" : 1,
    "comment" : "So Bad"
    
},
{
    "score" : 1.5,
    "comment" : "Bad"

},
{
    "score" : 2,
    "comment" : "Do not like"
    
},
{
    "score" : 2.5,
    "comment" : "Not Bad"

},
{
    "score" : 3,
    "comment" : "Not Bad"
    
},
{
    "score" : 3.5,
    "comment" : "Good"

},
{
    "score" : 4,
    "comment" : "Very Good"
    
},
{
    "score" : 4.5,
    "comment" : "Great!"

},
{
    "score" : 5,
    "comment" : "Excellent"
    
}]

reviewList = []
for reservation in reservationList:
    vote = comments[randint(0 , len(comments) - 1)]
    review = {
     "score" : vote["score"],
     "description"  :vote["comment"],
     "userID" : str(reservation["userID"]),
     "destinationID" : str(reservation["destinationID"]),
     "reviewer" : getUsernameFromID(str(reservation["userID"]))
    }
    reviewList.append(review)
    try:
        with client.start_session() as session:
            with session.start_transaction():
                reviewCollection.insert_one(review , session=session)
                if reservation["destinationType"] == "accommodation":
                    accommodationCollection.update_one({"_id" : ObjectId(str(reservation["destinationID"]))} , { "$push" : {"reviews" : review}} , session=session)
                    accommodationCollection.update_one({"_id" : ObjectId(str(reservation["destinationID"]))} , {"$push" : {"reviews" :{"$each" : []  , "$slice" : -15}}} , session=session)
                else:
                    activityCollection.update_one({"_id" : ObjectId(str(reservation["destinationID"]))} , { "$push" : {"reviews" : review}} , session=session)
                    activityCollection.update_one({"_id" : ObjectId(str(reservation["destinationID"]))} , {"$push" : {"reviews" :{"$each" : []  , "$slice" : -15}}}, session=session)

    except Exception as e:
        print("Impossibile inserire tutte : " + str(e))




