from utility.graphConnection import GraphManager
from models.activityNode import ActivityNode
from utility.serializer import Serializer

# Class that represents the manager for the activity node stored in graph database. 
# Methods implements query and serialization of object.
class ActivityNodeManager:

    # method that creates a node if it doesn't exists or update his property if it exists.
    @staticmethod
    def createActivityNode(activityNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                checkQuery = "MATCH (a:Activity {activityID : '%s'}) return COUNT(a) as total" %activityNode.activityID
                checkResult = list(session.run(checkQuery))[0]

                if checkResult.value("total") == 0:
                    query = "CREATE (a:Activity {activityID: '%s', name: '%s'})" % ( activityNode.activityID, activityNode.name)
                    session.run(query)
                
                else:
                    ActivityNodeManager.updateActivityNode(activityNode)


        except Exception as e:
            raise Exception("Impossibile inserire il nodo activity: " + str(e))

    @staticmethod
    def deleteActivityNode(activityNodeID):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH (a:Activity {activityID: '%s'}) DELETE a" % activityNodeID
                session.run(query)

        except Exception as e:
            raise Exception(
                "Impossibile eliminare il nodo activity: " + str(e))

    @staticmethod
    def updateActivityNode(activityNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH (a:Activity {activityID: '%s'}) SET a.name='%s' , a.approved = %s" % (
                    activityNode.activityID, activityNode.name , activityNode.approved)
                session.run(query)

        except Exception as e:
            raise Exception(
                "Impossibile aggiornare il nodo activity: " + str(e))

        # method that returns the total number of likes received by a specific activity
    @staticmethod
    def getTotalLikes(activityNodeID):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH(a: Activity)<-[r:LIKE]-(u:User) WHERE a.activityID = '%s' return  COUNT(r) as total" % activityNodeID
                result = list(session.run(query))[0]
                
                return result.value("total")

        except Exception as e:
            raise Exception(
                "Impossibile ottenere i likes totali: " + str(e))

        # method that from two userNode, returns a list of activities that both users like
    @staticmethod
    def getCommonLikedActivity(firstUserNode, secondUserID):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH(u1: User {userID: '%s' })-[:LIKE]->(a: Activity)<-[:LIKE]-(u2: User {userID: '%s' }) WHERE a.approved=True return a" % (
                    firstUserNode.userID, secondUserID)
                queryResult = list(session.run(query))
                result = []
                
                for item in queryResult:
                    node = item.get("a")
                    activityNode = ActivityNode(node["activityID"], node["name"])
                    result.append(Serializer.serializeAccommodationNode(activityNode))
                
                return result
        except Exception as e:
            raise Exception("Impossibile eseguire la query: " + str(e))
