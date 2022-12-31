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
                query = "MATCH (a:Accomodation {accomodationID: '%s'}) DELETE a" %accomodationNode.accomodationID
                session.run(query)

        except Exception as e:
            raise Exception(
                "Impossibile eliminare il nodo accomodation: " + str(e))
    
    @staticmethod
    def updateAccomodationNode(accomodationNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH (a:Accomodation {accomodationID: '%s'}) SET a.name='%s'" %(accomodationNode.accomodationID , accomodationNode.name)
                session.run(query)

        except Exception as e:
            raise Exception(
                "Impossibile aggiornare il nodo accomodation: " + str(e))

    @staticmethod
    def getAccomodationLikedByUser(userNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH(u:User {userID: '%s' })-[:LIKE]->(a: Accomodation) return a" %userNode.userID
                session.run(query)

        except Exception as e:
            raise Exception(
                "Impossibile eseguire la query: " + str(e))


    @staticmethod
    def getTotalLikes(accomodationNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH(a: Accomodation)<-[r:LIKE]-(u: User) WHERE a.activityID = '%s' return COUNT(r)" %accomodationNode.activityID
                session.run(query)

        except Exception as e:
            raise Exception(
                "Impossibile ottenere totale likes: " + str(e))
    
    @staticmethod
    def getCommonLikedAccomodation(firstUserNode , secondUserNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH(u1: User {userID: '%s' })-[:LIKE]->(a: Accomodation)<-[:LIKE]-(u2: User {userID: '%s' }) return a" %(firstUserNode.userID , secondUserNode.userID)
                session.run(query)

        except Exception as e:
            raise Exception(
                "Impossibile eseguire la query: " + str(e))