import pymongo
import os
from dotenv import load_dotenv


load_dotenv()

# Singleton client per le connesioni al DB
class MongoManager:
     __instance = None

     @staticmethod
     def getInstance():
         if MongoManager.__instance == None:
            MongoManager()
         return MongoManager.__instance

     def __init__(self):
        try:
            myclient = pymongo.MongoClient(
                os.getenv("LOCAL_BIND_ADDRESS"), 
                serverSelectionTimeoutMS=5000)
            MongoManager.__instance = myclient

        except Exception as e:
            print(f"IMPOSSIBILE CONNETTERSI AL DB:{e} ")
            MongoManager.__instance = None
