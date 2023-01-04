from controllers.connection import MongoManager
import pandas as pd
from random import randint

client = MongoManager.getInstance()
db = client["myvacation"]
usersCollection = db["users"]
accommodationsCollection = db["accommodations"]
activitiesCollection = db["activities"]

usersList = list(usersCollection.find({} , {"_id" : 1 , "username" : 1}))
print(usersList)
accommodationsList = list(accommodationsCollection.find({} , {"_id" : 1 , "name" : 1 , "type" : "accommodation"}))
activitiesList = list(activitiesCollection.find({} , {"_id" : 1 , "name" : 1 , "type" : "activity"}))

suggestionAccommodationResult = []
suggestionActivityResult = []
followResult = []

for user in usersList:
    if(user["username"] == "admin" or user["username"] == "unregistered"):
        continue
    # follower setup
    for i in range(3):
        randomUser = usersList[randint(0 , len(usersList) - 1)]
        if str(randomUser["_id"]) == str(user["_id"]):
            i = i-1
        else:
            obj = {
                "userID" : str(user["_id"]),
                "username": user["username"],
                "followedID" : str(randomUser["_id"]),
                "followedUsername" : randomUser["username"]
            }

            followResult.append(obj)
    # like setup
    for i in range(11):
        obj = {
            "userID": str(user["_id"]),
            "username" : user["username"]
        }
        # i < 7 accommodation
        if i < 7:
            print("accommodation")
            accommodation = accommodationsList[randint(0 , len(accommodationsList) - 1)]
            obj["accommodationID"] = str(accommodation["_id"])
            obj["accommodationName"] = str(accommodation["name"])
            suggestionAccommodationResult.append(obj)
        else:
            activity = activitiesList[randint(0 , len(activitiesList) - 1)]
            obj["activityID"] = str(activity["_id"])
            obj["activityName"] = str(activity["name"])
            suggestionActivityResult.append(obj)


accommodationDF = pd.DataFrame.from_dict(suggestionAccommodationResult)
activityDF = pd.DataFrame.from_dict(suggestionActivityResult)
usersDF = pd.DataFrame.from_dict(followResult)
usersDF.to_csv("users.csv")
accommodationDF.to_csv("accommodation.csv")
activityDF.to_csv("activity.csv")



