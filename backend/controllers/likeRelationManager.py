from .graphConnection import GraphManager


class LikeRelationManager:

    @staticmethod
    def checkIfExists(likeRelation):
        client = GraphManager.getInstance()

        try:
            query = "MATCH (u:User {userID: '%s'})-[r:LIKE]->" %likeRelation.user.userID
            if(hasattr(likeRelation  , "accommodation")):
                query = query + "(a: Accommodation{accommodationID : '%s'}) " %likeRelation.accommodation.accommodationID
            elif(hasattr(likeRelation  , "activity")):
                query = query + "(a: Activity{activityID : '%s'}) " %likeRelation.activity.activityID
            else:
                raise Exception("invalid likeRelation")
            query = query + "return COUNT(r) as total"
            
            print(query)
            with client.session() as session:
                result = list(session.run(query))[0].value("total")
            
            return result == 0

        except Exception as e:
            raise Exception("Impossibile inserire la relazione: " + str(e))

    @staticmethod
    def addLikeRelation(likeRelation):
        client = GraphManager.getInstance()
        print("sono dentro")
        try:
            if(not(LikeRelationManager.checkIfExists(likeRelation))):
                raise Exception("Già messo like")

            query = "MATCH (u:User {userID: '%s'}) " %likeRelation.user.userID
            if(hasattr(likeRelation  , "accommodation")):
                query = query + "MATCH (a: Accommodation{accommodationID : '%s'}) " %likeRelation.accommodation.accommodationID
            elif(hasattr(likeRelation  , "activity")):
                query = query + "MATCH (a: Activity{activityID : '%s'}) " %likeRelation.activity.activityID
            else:
                raise Exception("invalid likeRelation")
            query = query + "CREATE (u)-[:LIKE]->(a)"
            print(query)
            with client.session() as session:
                session.run(query)

        except Exception as e:
            raise Exception("Impossibile inserire la relazione: " + str(e))

    @staticmethod
    def removeLikeRelation(likeRelation):
        client = GraphManager.getInstance()

        try:
            
            query = "MATCH (u:User {userID: '%s'})-[r:LIKE]->" %likeRelation.user.userID
            if(hasattr(likeRelation  , "accommodation")):
                query = query + "(a: Accommodation{accommodationID : '%s'}) " %likeRelation.accommodation.accommodationID
            elif(hasattr(likeRelation  , "activity")):
                query = query + "(a: Activity{activityID : '%s'}) " %likeRelation.activity.activityID
            else:
                raise Exception("invalid likeRelation")
            query = query + "DELETE r"

            with client.session() as session:
                session.run(query)

        except Exception as e:
            raise Exception("Impossibile eliminare la relazione: " + str(e))
