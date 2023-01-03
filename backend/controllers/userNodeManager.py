from .graphConnection import GraphManager
from models.userNode import UserNode
from models.activityNode import ActivityNode
from models.accomodationNode import AccomodationNode
from utility.serializer import Serializer


class UserNodeManager:

    @staticmethod
    def createUserNode(userNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "CREATE (u:User {userID: '%s', username: '%s'})" % (
                    userNode.userID, userNode.username)
                session.run(query)

        except Exception as e:
            raise Exception("Impossibile inserire il nodo utente: " + str(e))

    @staticmethod
    def deleteUserNode(userNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH (u:User {userID: '%s'}) DETACH DELETE u" % userNode.userID
                session.run(query)

        except Exception as e:
            raise Exception("Impossibile eliminare il nodo utente: " + str(e))

    @staticmethod
    def getFollowedUser(userNodeID):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH(u:User {userID: '%s' })-[:FOLLOW]->(followed: User) return followed" % userNodeID
                queryResult = list(session.run(query))

                result = []

                for item in queryResult:
                    node = item.get("followed")
                    resultUserNode = UserNode(node["userID"], node["username"])
                    result.append(Serializer.serializeUserNode(resultUserNode))
                return result

        except Exception as e:
            raise Exception("Impossibile ottenere lista follower: " + str(e))

    @staticmethod
    def getLikedAdvs(userNode, destinationType):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                if (destinationType == "accomodation"):
                    query = "MATCH(u:User {userID: '%s' })-[:LIKE]->(liked: Accomodation) return liked" % userNode.userID
                else:
                    query = "MATCH(u:User {userID: '%s' })-[:LIKE]->(liked: Activity) return liked" % userNode.userID

                queryResult = list(session.run(query))
                
                result = []
                for item in queryResult:
                    node = item.get("liked")
                    if (destinationType == "accomodation"):
                        resultAccomodationNode = AccomodationNode(node["accomodationID"], node["name"])
                        result.append(Serializer.serializeAccomodationNode(resultAccomodationNode))
                    else:
                        resultActivityNode = ActivityNode(node["activityID"], node["name"])
                        result.append(Serializer.serializeActivityNode(resultActivityNode))
                return result

        except Exception as e:
            raise Exception("Impossibile ottenere annunci: " + str(e))

    # recommended adv: annunci che non piacciono a noi ma che piacciono ad account che seguiamo
    @staticmethod
    def getRecommendedAdvs(userNode, destinationType):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                if (destinationType == "accomodation"):
                    query = "MATCH (u:User {userID: '%s'})-[:FOLLOW]->(u2:User) MATCH (u2)-[:LIKE]->(a:Accomodation) WHERE NOT (u)-[:LIKE]->(a) return a" % userNode.userID
                else:
                    query = "MATCH (u:User {userID: '%s'})-[:FOLLOW]->(u2:User) MATCH (u2)-[:LIKE]->(a:Activity) WHERE NOT (u)-[:LIKE]->(a) return a" % userNode.userID
                queryResult = list(session.run(query))
                result = []

                for item in queryResult:
                    node = item.get("a")
                    if (destinationType == "accomodation"):
                        resultAccomodationNode = AccomodationNode(
                            node["accomodationID"], node["name"])
                        result.append(Serializer.serializeAccomodationNode(
                            resultAccomodationNode))
                    else:
                        resultActivityNode = ActivityNode(
                            node["activityID"], node["name"])
                        result.append(
                            Serializer.serializeActivityNode(resultActivityNode))

                return result

        except Exception as e:
            raise Exception("Impossibile ottenere lista annunci: " + str(e))

    # Utenti raccomandati: Utenti che non seguiamo ma che vengono seguiti da utenti che seguiamo

    @staticmethod
    def getRecommendedUsers(userNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                queryTotalFollowed = "MATCH (u:User {userID: '%s'})-[r:FOLLOW]->(:User) return COUNT(r) as total" % userNode.userID
                totalFollowed = list(session.run(queryTotalFollowed))[0].value("total")
                
                if(totalFollowed == 0):
                    query = "MATCH (u3 : User) WHERE NOT u3.userID = '%s' return u3 LIMIT 3"  % userNode.userID
                else:
                    query = "MATCH (u:User {userID: '%s'})-[:FOLLOW]->(u2:User) MATCH (u2)-[:FOLLOW]->(u3:User) WHERE NOT (u)-[:FOLLOW]->(u3) return u3 LIMIT 3" % userNode.userID
                
                queryResult = list(session.run(query))
                result = []

                for item in queryResult:
                    node = item.get("u3")
                    resultUserNode = UserNode(node["userID"], node["username"])
                    result.append(Serializer.serializeUserNode(resultUserNode))
                return result
        except Exception as e:
            raise Exception("Impossibile ottenere lista utenti: " + str(e))
