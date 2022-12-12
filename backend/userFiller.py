from datetime import datetime
import base64
import bcrypt 
from controllers.connection import MongoManager

imgList = []
psw = [
"LucaRossi" ,
"LuciaVerdi" ,
"AnnaBianchi" ,
"GiovanniRana" ,
"ValeriaNeri" ,
"AngelaPeri" ,
"RosaGialli" ,
"ValentinaRosa",
"AdminAdmin"]
hashed_psw = []

for i in range(1 , 10):
    if i != 9:
        with open(f"utility/testImg/user{i}.jpg" , "rb") as fileImg:
            imgList.append(base64.b64encode(fileImg.read()))

    # converting password to array of bytes
    bytes = psw[i-1].encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt).decode('utf-8')
    hashed_psw.append(hash)
  
    
users = [{

    "username" : "Luca",
    "password" : hashed_psw[0], 
    "name" : "Luca",
    "type" : "host",
    "surname" : "Rossi",
    "picture" : imgList[0],
    "gender" : "Male",
    "dateOfBirth" : datetime(1990 , 1 , 1),
    "nationality" : "IT",
    "knownLanguages" : ["italiano" , "inglese"],
    "reservations" : [],
    "reviews" : [],
    "plaHistory" : [],
    "actHistory" : [],
},
{

    "username" : "Lucia",
    "password" : hashed_psw[1], 
    "name" : "Lucia",
    "type" : "host",
    "surname" : "Verdi",
    "picture" : imgList[1],
    "gender" : "Female",
    "dateOfBirth" : datetime(1990 , 1 , 1),
    "nationality" : "IT",
    "knownLanguages" : ["italiano" , "inglese"],
    "reservations" : [],
    "reviews" : [],
    "plaHistory" : [],
    "actHistory" : [],
},
{

    "username" : "Anna",
    "password" : hashed_psw[2], 
    "name" : "Anna",
    "type" : "host",
    "surname" : "Bianchi",
    "picture" : imgList[2],
    "gender" : "Female",
    "dateOfBirth" : datetime(1990 , 1 , 1),
    "nationality" : "IT",
    "knownLanguages" : ["italiano" , "inglese"],
    "reservations" : [],
    "reviews" : [],
    "plaHistory" : [],
    "actHistory" : [],
},
{

    "username" : "Giovanni",
    "password" : hashed_psw[3], 
    "name" : "Giovanni",
    "type" : "host",
    "surname" : "Rana",
    "picture" : imgList[3],
    "gender" : "Male",
    "dateOfBirth" : datetime(1990 , 1 , 1),
    "nationality" : "IT",
    "knownLanguages" : ["italiano" , "inglese"],
    "reservations" : [],
    "reviews" : [],
    "plaHistory" : [],
    "actHistory" : [],
},
{

    "username" : "Valeria",
    "password" : hashed_psw[4], 
    "name" : "Valeria",
    "type" : "host",
    "surname" : "Neri",
    "picture" : imgList[4],
    "gender" : "Female",
    "dateOfBirth" : datetime(1990 , 1 , 1),
    "nationality" : "IT",
    "knownLanguages" : ["italiano" , "inglese"],
    "reservations" : [],
    "reviews" : [],
    "plaHistory" : [],
    "actHistory" : [],
},
{

    "username" : "Angela",
    "password" : hashed_psw[5], 
    "name" : "Angela",
    "type" : "host",
    "surname" : "Peri",
    "picture" : imgList[5],
    "gender" : "Female",
    "dateOfBirth" : datetime(1990 , 1 , 1),
    "nationality" : "IT",
    "knownLanguages" : ["italiano" , "inglese"],
    "reservations" : [],
    "reviews" : [],
    "plaHistory" : [],
    "actHistory" : [],
},
{

    "username" : "Rosa",
    "password" : hashed_psw[6], 
    "name" : "Rosa",
    "type" : "host",
    "surname" : "Gialli",
    "picture" : imgList[6],
    "gender" : "Female",
    "dateOfBirth" : datetime(1990 , 1 , 1),
    "nationality" : "IT",
    "knownLanguages" : ["italiano" , "inglese"],
    "reservations" : [],
    "reviews" : [],
    "plaHistory" : [],
    "actHistory" : [],
},
{

    "username" : "Valentina",
    "password" : hashed_psw[7], 
    "name" : "Valentina",
    "type" : "host",
    "surname" : "Rosa",
    "picture" : imgList[7],
    "gender" : "Female",
    "dateOfBirth" : datetime(1990 , 1 , 1),
    "nationality" : "IT",
    "knownLanguages" : ["italiano" , "inglese"],
    "reservations" : [],
    "reviews" : [],
    "plaHistory" : [],
    "actHistory" : [],
},
{

    "username" : "admin",
    "password" : hashed_psw[8], 
    "name" : "admin",
    "type" : "admin",
    "surname" : "admin",
    "picture" : None,
    "gender" : "male",
    "dateOfBirth" : datetime(1990 , 1 , 1),
    "nationality" : "IT",
    "knownLanguages" : ["italiano" , "inglese"],
    "reservations" : [],
    "reviews" : [],
    "plaHistory" : [],
    "actHistory" : [],
},
{

    "username" : "unregistered",
    "password" : None, 
    "name" : "unregistered",
    "type" : "unregistered",
    "surname" : "unregistered",
    "picture" : None,
    "gender" : "male",
    "dateOfBirth" : datetime(1990 , 1 , 1),
    "nationality" : "IT",
    "knownLanguages" : ["italiano" , "inglese"],
    "reservations" : [],
    "reviews" : [],
    "plaHistory" : [],
    "actHistory" : [],
}]

client = MongoManager.getInstance()
db = client["myvacation"]
collection = db["users"]
collection.insert_many(users)
