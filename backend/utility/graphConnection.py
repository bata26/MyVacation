from neo4j import GraphDatabase
import os
from dotenv import load_dotenv


load_dotenv()


# Singleton client per le connesioni al DB
class GraphManager:
     __instance = None

     @staticmethod
     def getInstance():
         if GraphManager.__instance == None:
            GraphManager()
         return GraphManager.__instance

     def __init__(self):
        try:
            global server , pickedPort
           
            myclient = GraphDatabase.driver(
                os.getenv("GRAPH_LOCAL_ADDRESS"), 
                auth = (os.getenv("GRAPH_USER") , os.getenv("GRAPH_PASSWORD")))
            GraphManager.__instance = myclient

        except Exception as e:
            print(f"IMPOSSIBILE CONNETTERSI AL GRAPH DB:{e} ")
            GraphManager.__instance = None
