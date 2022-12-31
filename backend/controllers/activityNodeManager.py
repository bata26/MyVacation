from .graphConnection import GraphManager


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
    def getActivityLikedByUser(userNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH(u:User {userID: '%s' })-[:LIKE]->(a: Activity) return a" % userNode.userID
                session.run(query)

        except Exception as e:
            raise Exception(
                "Impossibile eseguire la query: " + str(e))

    @staticmethod
    def getTotalLikes(activityNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH(a: Activity)<-[r:LIKE]-(u: User) WHERE a.activityID = '%s' return COUNT(r)" % activityNode.activityID
                session.run(query)

        except Exception as e:
            raise Exception(
                "Impossibile ottenere i likes totali: " + str(e))

    @staticmethod
    def getCommonLikedActivity(firstUserNode, secondUserNode):
        client = GraphManager.getInstance()
        try:
            with client.session() as session:
                query = "MATCH(u1: User {userID: '%s' })-[:LIKE]->(a: Activity)<-[:LIKE]-(u2: User {userID: '%s' }) return a" % (
                    firstUserNode.userID, secondUserNode.userID)
                result = session.run(query)
                return result
        except Exception as e:
            raise Exception("Impossibile eseguire la query: " + str(e))
