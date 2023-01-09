from utility.graphConnection import GraphManager
from utility.connection import MongoManager
import pandas as pd

graphClient = GraphManager.getInstance()

mongoclient = MongoManager.getInstance()
db = mongoclient["myvacation"]
accommodationCollection = db["accommodations"]
activitiesCollection = db["activities"]
usersCollection = db["users"]

accommodationsList = list(accommodationCollection.find({} , {"_id" : 1 , "name" : 1}))
print(" accommodationsList ottenuta")
activitiesList = list(activitiesCollection.find({} , {"_id" : 1 , "name" : 1}))
print(" activitiesList ottenuta")
usersList = list(usersCollection.find({"username" : {"$nin" : ["admin" , "unregistered"] }} , {"_id" : 1 , "username"  :1}))
print(" usersList ottenuta")


userDF = pd.DataFrame(usersList) 
accommodationDF = pd.DataFrame(accommodationsList) 
activitieDF = pd.DataFrame(activitiesList) 

userDF.to_csv("userDF.csv")
accommodationDF.to_csv("accommodationDF.csv")
activitieDF.to_csv("activitieDF.csv")

"""
with graphClient.session() as session:
    for user in usersList:
        try:
            query = "CREATE (u:User {userID : '%s' , username: '%s'})"  %(str(user["_id"]) , user["username"])
            session.run(query)
        except Exception as e:
            print("_id : " + str(user["_id"]))
            continue

    print("user inseriti")
    

    for accommodation in accommodationsList:
        try:
            name = f"{accommodation['name']}".replace('"' , "'")
            name = name.replace("'" , " ")
            id = str(accommodation["_id"])
            #query = "CREATE (a:Accommodation {accommodationID: "
            #query = query +  "'" + id + "' ,  name: " + '"{name}"'.format(id=id , name = accommodation['name'])
            #query = query + "})"
            parameters = {
                "activityID" : id,
                "name" : name
            }
           
            query = "CREATE (a:Accommodation {{ {parameters} }})"
            properties = ', '.join('{0}: ${0}'.format(n) for n in parameters)
            query2 = query.format(properties=properties)
            print(query2)
            #break
            session.run(query , parameters=parameters)
        except Exception as e:
            print(str(e))
            print("_id : " + str(accommodation["_id"]))
            continue
    print("accommodation inseriti")
    
    for activity in activitiesList:
        break
        try:
            name = activity['name'].replace('"' , "'")
            name = name.replace("'" , "")
            id = str(activity["_id"])
            obj = {
                "activityID" : id,
                "name" : name
            }
            #query = "CREATE (a:Activity {activityID: "
            #query = query +  "'" + id + "' ,  name: " + '"{name}"'.format(id=id , name = activity['name'])
            #query = query + "})"
            query = "CREATE (a:Activity {obj})".format(obj)
            print(query)
            session.run(query)
        except Exception as e:
            print(str(e))
            print("_id : " + str(activity["_id"]))
            continue
    print("activity inseriti")
"""
