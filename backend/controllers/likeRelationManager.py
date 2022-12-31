from .graphConnection import GraphManager


class LikeRelationManager:

    @staticmethod
    def addLikeRelation(likeRelation):
        client = GraphManager.getInstance()

        try:
            query = "MATCH (u:User {userID: '%s'}) " %likeRelation.user.userID
            if(hasattr(likeRelation  , "accomodation")):
                query = query + "MATCH (a: Accomodation{accomodationID : '%s'}) " &likeRelation.accomodation.accomodationID
            elif(hasattr(likeRelation  , "activity")):
                query = query + "MATCH (a: Activity{activityID : '%s'}) " &likeRelation.activity.activityID
            else:
                raise Exception("invalid likeRelation")
            query = query + "CREATE (u)-[:LIKE]->(a)"

            with client.session() as session:
                session.run(query)

        except Exception as e:
            raise Exception("Impossibile inserire la relazione: " + str(e))

    @staticmethod
    def removeLikeRelation(likeRelation):
        client = GraphManager.getInstance()

        try:
            query = "MATCH (u:User {userID: '%s'})-[r:LIKE]->" %likeRelation.user.userID
            if(hasattr(likeRelation  , "accomodation")):
                query = query + "(a: Accomodation{accomodationID : '%s'}) " &likeRelation.accomodation.accomodationID
            elif(hasattr(likeRelation  , "activity")):
                query = query + "(a: Activity{activityID : '%s'}) " &likeRelation.activity.activityID
            else:
                raise Exception("invalid likeRelation")
            query = query + "DELETE r"

            with client.session() as session:
                session.run(query)

        except Exception as e:
            raise Exception("Impossibile eliminare la relazione: " + str(e))
