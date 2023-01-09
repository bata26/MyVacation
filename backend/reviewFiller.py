from utility.connection import MongoManager
from random import randint
from datetime import datetime , timedelta
from bson.objectid import ObjectId
import random


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
    reservationList = list(reservationCollection.find({} , {"_id" : 1 , "price" : 1 , "city" : "$location.city" , "hostID" : 1}))
    print("Fetch delle accommodations eseguito")    
except Exception as e:
    print("Impossibile ottenere utenti: " + str(e))
for i in range(0 , 1200):
   


try:
    with client.start_session() as session:
        with session.start_transaction():
except Exception as e:
    print("Impossibile inserire tutte : " + str(e))

