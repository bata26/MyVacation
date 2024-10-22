from utility.graphConnection import GraphManager
from models.userNode import UserNode
from models.activityNode import ActivityNode
from models.accommodationNode import AccommodationNode
from utility.serializer import Serializer


class UserNodeManager:
#Checks if the logged user is following the viewed user
    @staticmethod
    def checkIfIsFollowing(userID , followedID):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH (u:User {userID : '%s'})-[r:FOLLOW]->(u2:User {userID : '%s'}) " \
                        "return COUNT(r) as total" % (userID , followedID)
                result = list(session.run(query))[0].value("total")

                if(result == 0):
                    return False
                else:
                    return True

        except Exception as e:
            raise Exception("Impossibile inserire il nodo utente: " + str(e))

#Creates a UserNode after the SignUp
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

#Deletes a UserNode
    @staticmethod
    def deleteUserNode(userNodeID):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH (u:User {userID: '%s'}) DETACH DELETE u" % userNodeID
                session.run(query)

        except Exception as e:
            raise Exception("Impossibile eliminare il nodo utente: " + str(e))

#Gets all the users followed by the checked user
    @staticmethod
    def getFollowedUser(userNodeID):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH(u:User {userID: '%s' })-[:FOLLOW]->(followed: User) " \
                        "return followed" % userNodeID
                queryResult = list(session.run(query))

                result = []

                for item in queryResult:
                    node = item.get("followed")
                    resultUserNode = UserNode(node["userID"], node["username"])
                    result.append(Serializer.serializeUserNode(resultUserNode))
                return result

        except Exception as e:
            raise Exception("Impossibile ottenere lista follower: " + str(e))

#Checks if the logged user already likes the viewed accommodation/activity
    @staticmethod
    def checkIfUserLikesDestination(userNodeID, destinationID, destinationType):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                if (destinationType == "accommodation"):
                    query = "MATCH(u:User {userID: '%s' })-[r:LIKE]->(liked: Accommodation { accommodationID: '%s'}) " \
                            "return COUNT(r) as total" % (userNodeID, destinationID)
                else:
                    query = "MATCH(u:User {userID: '%s' })-[r:LIKE]->(liked: Activity { activityID: '%s'}) " \
                            "return COUNT(r) as total" % (userNodeID, destinationID)
                #print(query)
                queryResult = list(session.run(query))[0].value("total")
                #print(queryResult)
                
                if(queryResult > 0):
                    return True
                elif (queryResult == 0):
                    return False
        except Exception as e:
            raise Exception("Impossibile ottenere annunci: " + str(e))

#Gets all the liked accommodations/activities by the logged user
    @staticmethod
    def getLikedAdvs(userNodeID, destinationType):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                if (destinationType == "accommodation"):
                    query = "MATCH(u:User {userID: '%s' })-[:LIKE]->(liked: Accommodation) " \
                            "WHERE liked.approved = True " \
                            "return liked" % userNodeID
                else:
                    query = "MATCH(u:User {userID: '%s' })-[:LIKE]->(liked: Activity) " \
                            "WHERE liked.approved = True " \
                            "return liked" % userNodeID

                queryResult = list(session.run(query))
                
                result = []
                for item in queryResult:
                    node = item.get("liked")
                    if (destinationType == "accommodation"):
                        resultAccommodationNode = AccommodationNode(node["accommodationID"], node["name"])
                        result.append(Serializer.serializeAccommodationNode(resultAccommodationNode))
                    else:
                        resultActivityNode = ActivityNode(node["activityID"], node["name"])
                        result.append(Serializer.serializeActivityNode(resultActivityNode))
                return result

        except Exception as e:
            raise Exception("Impossibile ottenere annunci: " + str(e))

#Recommended adv:gets accommodations/activities that we don't like but, accounts that we follow, like
    @staticmethod
    def getRecommendedAdvs(userNode, destinationType):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                queryTotalFollowed = "MATCH (u:User {userID: '%s'})-[r:FOLLOW]->(:User) " \
                                     "return COUNT(r) as total" % userNode.userID
                totalFollowed = list(session.run(queryTotalFollowed))[0].value("total")
                if destinationType == "accommodation":
                    if totalFollowed == 0:
                        query = "MATCH (u:User)-[r:LIKE]->(a:Accommodation) " \
                                "MATCH (u2:User {userID: '%s'})  " \
                                "WHERE NOT (u2)-[:LIKE]->(a)  "\
                                "AND a.approved=True " \
                                "return a , " \
                                "COUNT(r) as liked " \
                                "ORDER BY liked DESC " \
                                "LIMIT 3" % userNode.userID
                    else:
                        query = "MATCH (u:User {userID: '%s'})-[:FOLLOW]->(u2:User) " \
                                "MATCH (u2)-[:LIKE]->(a:Accommodation) " \
                                "MATCH (u3:User)-[r:LIKE]->(a)  " \
                                "WHERE NOT (u)-[:LIKE]->(a)  " \
                                "AND a.approved=True "\
                                "return a , " \
                                "COUNT(r) as liked " \
                                "ORDER BY liked DESC " \
                                "LIMIT 3" % userNode.userID
                else:
                    if totalFollowed == 0:
                        query = "MATCH (u:User)-[r:LIKE]->(a:Activity) " \
                                "MATCH (u2:User {userID: '%s'})  " \
                                "WHERE NOT (u2)-[:LIKE]->(a) " \
                                "AND a.approved=True "\
                                "return a , " \
                                "COUNT(r) as liked " \
                                "ORDER BY liked DESC " \
                                "LIMIT 3" % userNode.userID
                    else:
                        query = "MATCH (u:User {userID: '%s'})-[:FOLLOW]->(u2:User) " \
                                "MATCH (u2)-[:LIKE]->(a:Activity) " \
                                "MATCH (u3:User)-[r:LIKE]->(a)  " \
                                "WHERE NOT (u)-[:LIKE]->(a)  " \
                                "AND a.approved=True "\
                                "return a , " \
                                "COUNT(r) as liked " \
                                "ORDER BY liked DESC " \
                                "LIMIT 3" % userNode.userID

                queryResult = list(session.run(query))
                result = []

                for item in queryResult:
                    node = item.get("a")
                    if destinationType == "accommodation":
                        resultAccommodationNode = AccommodationNode(
                            node["accommodationID"], node["name"])
                        result.append(Serializer.serializeAccommodationNode(
                            resultAccommodationNode))
                    else:
                        resultActivityNode = ActivityNode(
                            node["activityID"], node["name"])
                        result.append(
                            Serializer.serializeActivityNode(resultActivityNode))

                return result

        except Exception as e:
            raise Exception("Impossibile ottenere lista annunci: " + str(e))

#Recommended Users: gets users we don't follow, but are followed by users we follow
    @staticmethod
    def getRecommendedUsers(userNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                queryTotalFollowed = "MATCH (u:User {userID: '%s'})-[r:FOLLOW]->(:User) " \
                                     "return COUNT(r) as total" % userNode.userID
                totalFollowed = list(session.run(queryTotalFollowed))[0].value("total")
                
                if totalFollowed == 0:
                    query = "MATCH (u3:User) " \
                            "MATCH (u2:User)-[r:FOLLOW]->(u3)  " \
                            "WHERE NOT u3.userID = '%s' AND NOT u2.userID='%s' " \
                            "return u3 , " \
                            "COUNT(r) as followed " \
                            "ORDER BY followed DESC " \
                            "LIMIT 3" % (userNode.userID , userNode.userID)
                else:
                    query = "MATCH (u:User {userID: '%s'})-[:FOLLOW]->(u2:User) " \
                            "MATCH (u2)-[:FOLLOW]->(u3:User) " \
                            "MATCH (u4)-[r:FOLLOW]->(u3)  " \
                            "WHERE NOT (u)-[:FOLLOW]->(u3) " \
                            "return u3 , " \
                            "COUNT(r) as followed " \
                            "ORDER BY followed DESC " \
                            "LIMIT 3" % userNode.userID
                
                queryResult = list(session.run(query))
                result = []

                for item in queryResult:
                    node = item.get("u3")
                    resultUserNode = UserNode(node["userID"], node["username"])
                    result.append(Serializer.serializeUserNode(resultUserNode))
                return result
        except Exception as e:
            raise Exception("Impossibile ottenere lista utenti: " + str(e))
