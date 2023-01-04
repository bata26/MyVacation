import pymongo
import os
from dotenv import load_dotenv
from socket import socket


load_dotenv()

##print(os.getenv("LOCATION"))

# trova una porta libera e si connette
def getFreePort():
    with socket() as s:
        s.bind(('',0))
        port = s.getsockname()[1]
        #print(f"Selezionata la porta {port}")
        return port

# Singleton client per le connesioni al DB
class MongoManager:
     __instance = None

     @staticmethod
     def getInstance():
         if MongoManager.__instance == None:
            MongoManager()
         return MongoManager.__instance
 
    
     def OpenSSHTunnel():
        global server , pickedPort
        pickedPort = getFreePort()

     def __init__(self):
        #print("MONGO MANAGER INIT")
        try:
            global server , pickedPort
            if(os.getenv("LOCATION") == "remote"):
                MongoManager.OpenSSHTunnel()

                if(server == None):
                    #logging.warning("IMPOSSIBILE APRIRE IL TUNNEL SSH")
                    raise Exception

                # start ssh tunnel
                server.start()
                myclient = pymongo.MongoClient("127.0.0.1",
                                        pickedPort,
                                        username= os.getenv("USERNAME_DB"),
                                        password=os.getenv("PWD_DB"),
                                        ssl=True,
                                        ssl_ca_certs=os.getenv("SSL_CA_CERTS"),
                                        ssl_match_hostname=False,
                                        retryWrites=False)
                #print("CONNESSIONE AL DB RIUSCITA")
            else:
                #print("CONNESSO AL DB LOCALE")
                myclient = pymongo.MongoClient(
                    os.getenv("LOCAL_BIND_ADDRESS"), 
                    serverSelectionTimeoutMS=5000)
            MongoManager.__instance = myclient

        except Exception as e:
            #print(f"IMPOSSIBILE CONNETTERSI AL DB:{e} ")
            MongoManager.__instance = None
