import pandas as pd
import os
import http.client, urllib.parse
import json
from controllers.connection import MongoManager
import pymongo
import base64
import requests
from random import randint
DIRECTORY_NAME = "dataset"
LISTING_FILENAME = "listings.csv"
REVIEWS_FILENAME = "reviews.csv"

API_KEY = "8c58fc165e740f37081edd19d514df34"
API_URL = f"api.positionstack.com"

connection = None

headerToSave = ['name' ,'description' ,'picture_url' ,'hostID' ,'host_url' ,'hostName' ,'host_since' ,'host_picture_url' ,'latitude' ,'longitude' ,'propertyType' ,'accommodates' ,'bathrooms' ,'bedrooms' ,'beds' ,'price' ,'minimum_nights' ,'number_of_reviews' ,'review_scores_rating']
cities = [
    "Roma",
"Milano",
"Napoli",
"Torino",
"Palermo",
"Genova",
"Bologna",
"Firenze",
"Bari",
"Catania",
"Venezia",
"Verona",
"Messina",
"Padova",
"Trieste",
"Taranto",
"Brescia",
"Parma",
"Prato",
"Pisa"]
def getAddress(latitude , longitude):
    global connection , cities

    params = urllib.parse.urlencode({
        'access_key': API_KEY,
        'query': str(latitude) +","+str(longitude),
    })

    # REQUEST
    connection.request('GET', '/v1/reverse?{}'.format(params))

    #RESPONSE
    res = connection.getresponse()
    data = json.loads(res.read())
    try:
        location = {
            "address" : data["data"][0]["street"] , 
            "city" : cities[randint(0 , len(cities) - 1)] , 
            "country" : data["data"][0]["country"]
        }

        return location
    except Exception:
        return None
    #print(data["results"])

    


if __name__ == "__main__":
    connection = http.client.HTTPConnection(API_URL)
    connection.connect()
    os.chdir('../'+DIRECTORY_NAME)
    
    directoryList = os.listdir()
    for directory in directoryList:
        os.chdir(directory)

        listingDataFrame = pd.read_csv(LISTING_FILENAME)
        print("LISTING OK")
        #print(list(listingDataFrame.columns.values))
        #print("====================\n\n")
        reviewsDataFrame = pd.read_csv(REVIEWS_FILENAME)
        print("REVIEWS OK")
        #print(list(reviewsDataFrame.columns.values))
        #print("====================\n\n")
        address = []
        city = []
        country = []
        indexToDelete = []
        client = MongoManager.getInstance()
        db = client["myvacation"]
        collection = db["accommodations"]
        for index, row in listingDataFrame.iterrows():
            
            try:
                picture = base64.b64encode(requests.get(row["picture_url"]).content)
                host_picture = base64.b64encode(requests.get(row["host_picture_url"]).content)
                #print(row["host_picture_url"])
                #print(requests.get(row["host_picture_url"]).content)
                #print(base64.b64encode(requests.get(row["host_picture_url"]).content))
                id = row["id"]
                collection.update_one({"old_id" : id} , {"$set" : {"mainPicture" : picture}})
                

                location = getAddress(row["latitude"] , row["longitude"])
                if(location == None):
                    indexToDelete.append(index)
                else:
                    address.append(location["address"])
                    city.append(location["city"])
                    country.append(location["country"])
                    try:
                        obj = {
                        "old_id" : row["id"],
                        'name': row['name'] ,
                        'description': row['description'] ,
                        'hostID': row['hostID'] ,
                        'host_url': row['host_url'] ,
                        'hostName': row['hostName'] ,
                        'host_picture': host_picture ,
                        "location" : location,
                        'propertyType': row['propertyType'] ,
                        'accommodates': row['accommodates'] ,
                        'bedrooms': row['bedrooms'] ,
                        'beds': row['beds'] ,
                        'price': float(row['price'].split("$")[1]) ,
                        'minimum_nights': row['minimum_nights'] ,
                        'number_of_reviews': row['number_of_reviews'] ,
                        'review_scores_rating': row['review_scores_rating'],
                        "mainPicture" : picture
                        }


                        collection.insert_one(obj)
                        print(f"oggetto {index} inserito correttamente")
                    except Exception as e:
                        print(f"impossibile inserire : {e}")    
            except Exception as e:
                print(f"ERRORE:{e}")     
            #break
        os.chdir("..")
        break