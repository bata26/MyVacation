from .graphConnection import GraphManager
from models.activityNode import ActivityNode
from utility.serializer import Serializer

class ActivityNodeManager:

    @staticmethod
    def createActivityNode(activityNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                session.run("CREATE (a:Activity {activityID: '%s', name: '%s'})" % (
                    activityNode.userID, activityNode.name))

        except Exception as e:
            raise Exception("Impossibile inserire il nodo activity: " + str(e))

    @staticmethod
    def deleteActivityNode(activityNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH (a:Activity {activityID: '%s'}) DELETE a" % activityNode.activityID
                session.run(query)

        except Exception as e:
            raise Exception(
                "Impossibile eliminare il nodo activity: " + str(e))

    @staticmethod
    def updateActivityNode(activityNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH (a:Activity {activityID: '%s'}) SET a.name='%s'" % (
                    activityNode.activityID, activityNode.name)
                session.run(query)

        except Exception as e:
            raise Exception(
                "Impossibile aggiornare il nodo activity: " + str(e))

    @staticmethod
    def getTotalLikes(activityNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH(a: Activity)<-[r:LIKE]-(u: User) WHERE a.activityID = '%s' return COUNT(r) as total" % activityNode.activityID
                result = list(session.run(query))[0]
                return result.value("total")

        except Exception as e:
            raise Exception(
                "Impossibile ottenere i likes totali: " + str(e))

    @staticmethod
    def getCommonLikedActivity(firstUserNode, secondUserID):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH(u1: User {userID: '%s' })-[:LIKE]->(a: Activity)<-[:LIKE]-(u2: User {userID: '%s' }) return a" % (
                    firstUserNode.userID, secondUserID)
                queryResult = list(session.run(query))
                result = []
                
                for item in queryResult:
                    node = item.get("a")
                    activityNode = ActivityNode(node["accomodationID"], node["name"])
                    result.append(Serializer.serializeAccomodationNode(activityNode))
                
                return result
        except Exception as e:
            raise Exception("Impossibile eseguire la query: " + str(e))
