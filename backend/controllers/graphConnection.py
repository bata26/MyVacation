from neo4j import GraphDatabase
import pymongo
import os
from dotenv import load_dotenv
from socket import socket


load_dotenv()

# trova una porta libera e si connette
def getFreePort():
    with socket() as s:
        s.bind(('',0))
        port = s.getsockname()[1]
        print(f"Selezionata la porta {port}")
        return port

# Singleton client per le connesioni al DB
class GraphManager:
     __instance = None

     @staticmethod
     def getInstance():
         if GraphManager.__instance == None:
            GraphManager()
         return GraphManager.__instance

     def __init__(self):
        print("MONGO MANAGER INIT")
        try:
            global server , pickedPort
            if(os.getenv("LOCATION") == "remote"):
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
                print("CONNESSIONE AL DB RIUSCITA")
            else:
                print("CONNESSO AL DB LOCALE")
                myclient = GraphDatabase.driver(
                    os.getenv("GRAPH_LOCAL_ADDRESS"), 
                    auth = (os.getenv("GRAPH_USER") , os.getenv("GRAPH_PASSWORD")))
            GraphManager.__instance = myclient

        except Exception as e:
            print(f"IMPOSSIBILE CONNETTERSI AL DB:{e} ")
            GraphManager.__instance = None
