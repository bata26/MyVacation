#import bcrypt
#
#clienthash = "$2b$12$S0JsqH4t87pLBM1AWTXeTOPMh2/fSskcygTF171Ro8MgdOtyLpbEu"
#pwd = "AdminAdmin"
#salt = bcrypt.gensalt(12)
#dbHash = bcrypt.hashpw(pwd.encode('utf-8'), salt).decode('utf-8')
#print(dbHash)
#print(bcrypt.checkpw(pwd.encode('utf-8'), dbHash.encode('utf8')))
from controllers.connection import MongoManager
from random import randint
import pymongo
from bson.objectid import ObjectId

users = [
{
	"_id" : "637ce1a04ed62608566c5fa7",
	"name" : "Luca"
},
{
	"_id" : "637ce1a04ed62608566c5fa8",
	"name" : "Lucia"
},
{
	"_id" : "637ce1a04ed62608566c5fa9",
	"name" : "Anna"
},
{
	"_id" : "637ce1a04ed62608566c5faa",
	"name" : "Giovanni"
},
{
	"_id" : "637ce1a04ed62608566c5fab",
	"name" : "Valeria"
},
{
	"_id" : "637ce1a04ed62608566c5fac",
	"name" : "Angela"
},
{
	"_id" : "637ce1a04ed62608566c5fad",
	"name" : "Rosa"
},
{
	"_id" : "637ce1a04ed62608566c5fae",
	"name" : "Valentina"
}]

client = MongoManager.getInstance()
db = client["myvacation"]
accommodationCollection = db["activities"]
cursor = list(accommodationCollection.find())

counter = 0
for accommodation in cursor:
    user = users[randint(0 , len(users)- 1)]
    try:
        accommodationCollection.update_one({"_id" : accommodation["_id"]} , {"$set" : {"hostID" : ObjectId(user["_id"]) , "hostName" : user["name"]}})
        print(f"Inserito correttamente: {counter}")
    except Exception as e:
        print(f"Impossibile aggiornare : {e}" )