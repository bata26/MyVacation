from .graphConnection import GraphManager
from models.followRelation import FollowRelation

class FollowRelationManager:

    @staticmethod
    def addFollowRelation(followRelation):
        client = GraphManager.getInstance()

        try:
            query = "MATCH (u:User {userID: '%s'}) MATCH (u1: User{userID : '%s'}) CREATE (u)-[:FOLLOW]->(u1)" %(followRelation.user.userID , followRelation.followedUser.userID)
            with client.session() as session:
                session.run(query)

        except Exception as e:
            raise Exception("Impossibile inserire la relazione: " + str(e))

    @staticmethod
    def removeFollowRelation(followRelation):
        client = GraphManager.getInstance()

        try:
            query = "MATCH (u: User {userID : '%s' })-[r:FOLLOW]->(u1:User {userID: '%s'}) DELETE r" %(followRelation.user.userID , followRelation.followedUser.userID)
            with client.session() as session:
                session.run(query)

        except Exception as e:
            raise Exception("Impossibile eliminare: " + str(e))
