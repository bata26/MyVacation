from utility.serializer import Serializer
from models.accomodationNode import AccomodationNode
from .graphConnection import GraphManager


class AccomodationNodeManager:
    @staticmethod
    def createAccomodationNode(accomodationNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                session.run("CREATE (a:Accomodation {accomodationID: '%s', name: '%s'})" % (
                    accomodationNode.userID, accomodationNode.name))

        except Exception as e:
            raise Exception(
                "Impossibile inserire il nodo accomodation: " + str(e))

    @staticmethod
    def deleteAccomodationNode(accomodationNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH (a:Accomodation {accomodationID: '%s'}) DELETE a" % accomodationNode.accomodationID
                session.run(query)

        except Exception as e:
            raise Exception(
                "Impossibile eliminare il nodo accomodation: " + str(e))

    @staticmethod
    def updateAccomodationNode(accomodationNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH (a:Accomodation {accomodationID: '%s'}) SET a.name='%s'" % (
                    accomodationNode.accomodationID, accomodationNode.name)
                session.run(query)

        except Exception as e:
            raise Exception(
                "Impossibile aggiornare il nodo accomodation: " + str(e))

    @staticmethod
    def getTotalLikes(accomodationID):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH(a: Accomodation)<-[r:LIKE]-(u: User) WHERE a.accomodationID = '%s' return COUNT(r) as total" % accomodationID
                result = list(session.run(query))[0]
                return result.value("total")

        except Exception as e:
            raise Exception(
                "Impossibile ottenere totale likes: " + str(e))

    @staticmethod
    def getCommonLikedAccomodation(firstUserNode, secondUserID):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH(u1: User {userID: '%s' })-[:LIKE]->(a: Accomodation)<-[:LIKE]-(u2: User {userID: '%s' }) return a" % (
                    firstUserNode.userID, secondUserID)
                queryResult = list(session.run(query))
                result = []
                
                for item in queryResult:
                    node = item.get("a")
                    accomodationNode = AccomodationNode(node["accomodationID"], node["name"])
                    result.append(Serializer.serializeAccomodationNode(accomodationNode))
                
                return result
        except Exception as e:
            raise Exception(
                "Impossibile eseguire la query: " + str(e))