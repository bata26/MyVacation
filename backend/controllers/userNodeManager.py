from .graphConnection import GraphManager


class UserNodeManager:
       
    @staticmethod
    def createUserNode(userNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "CREATE (u:User {userID: '%s', username: '%s'})" %(userNode.userID , userNode.username)
                session.run(query)
            
        except Exception as e:
            raise Exception("Impossibile inserire il nodo utente: " + str(e))

    @staticmethod
    def deleteUserNode(userNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH (u:User {userID: '%s'}) DETACH DELETE u" %userNode.userID
                session.run(query)
            
        except Exception as e:
            raise Exception("Impossibile eliminare il nodo utente: " + str(e))


    @staticmethod
    def getFollowedUser(userNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH(u:User {userID: '%s' })-[:FOLLOW]->(followed: User) return followed" %userNode.userID
                result = session.run(query)
            
        except Exception as e:
            raise Exception("Impossibile ottenere lista follower: " + str(e))
