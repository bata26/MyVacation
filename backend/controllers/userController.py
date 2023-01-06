from managers.userManager import UserManager
import bcrypt
import dateparser
from datetime import datetime
from models.user import User
from models.userNode import UserNode
from managers.userNodeManager import UserNodeManager
from models.followRelation import FollowRelation
from managers.followRelationManager import FollowRelationManager
class UserController:
    
    @staticmethod
    def updateUser(updatedData , userID):
        try:
            UserManager.updateUser(updatedData, userID)
        except Exception as e:
           raise Exception(str(e))
    
    @staticmethod
    def checkIfIsFollowing(userID , followindID):
        try:
            res = UserNodeManager.checkIfIsFollowing(userID , followindID)
            return {"following" : res}
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def getFollowedUser(userID):
        try:
            res = UserNodeManager.getFollowedUser(userID)
            return res
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def checkIfLike(userID , destinationID , destinationType):
        try:
            res = UserNodeManager.checkIfUserLikesDestination(userID , destinationID , destinationType)
            return {"liked" : res}
        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    def getRecommendedUsers(user):
        try:
            userNode = UserNode(user["_id"], user["username"])
            res = UserNodeManager.getRecommendedUsers(userNode)
            return res
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def getRecommendedAdvs(destinationType , user):
        try:
            userNode = UserNode(user["_id"], user["username"])
            result = UserNodeManager.getRecommendedAdvs(userNode, destinationType)
            return result
        except Exception as e:
            raise Exception(str(e))
    
    
    @staticmethod
    def getLikedAdvs(userID ,  destinationType):
        try:
            res = UserNodeManager.getLikedAdvs(userID ,destinationType)
            return res
        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    def getUserByID(userID):
        try:
            res = UserManager.getUserFromID(userID)
            return res
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def authenticateUser(username, password):
        try:
            userID, userType, username, name = UserManager.authenticateUser(username, password)
            return {
                "userID": userID,
                "role": userType,
                "name": name,
                "username": username,
            }
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def followUser(requestBody , user):
        try:
            followerNode = UserNode(user["_id"], user["username"])
            followedNode = UserNode(requestBody["userID"] , requestBody["username"])
            followRelation = FollowRelation(followerNode , followedNode)
            FollowRelationManager.addFollowRelation(followRelation)
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def unfollowUser(requestBody , user):
        try:
            userNode = UserNode(user["_id"], user["username"])
            unfollowedUserNode = UserNode(requestBody["userID"], requestBody["username"])
            followRelation = FollowRelation(userNode,unfollowedUserNode)
            FollowRelationManager.removeFollowRelation(followRelation)
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def registerUser(requestBody):
        try:
            username = requestBody["username"]
            password = requestBody["password"]
            name = requestBody["name"]
            surname = requestBody["surname"]
            gender = requestBody["gender"]
            dateOfBirth = requestBody["dateOfBirth"]
            nationality = requestBody["nationality"]
            knownLanguages = requestBody["knownLanguages"]

            if(UserManager.checkIfUserExists(username) > 0):
                raise Exception("Username already picked")

            salt = bcrypt.gensalt(12)
            dbHash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
            user = User(
                username,
                dbHash,
                name,
                surname,
                "user",
                gender,
                dateparser.parse(dateOfBirth),
                nationality,
                knownLanguages,
                [],
                datetime.today().replace(microsecond=0, second=0, hour=0, minute=0),
            )
            try:
                insertedID = UserManager.insertNewUser(user)
            except Exception as e:
                raise Exception(str(e))

            try:
                userNode = UserNode(insertedID, username)
                UserNodeManager.createUserNode(userNode)
                return insertedID , True
            except Exception as e:
                return insertedID  , False
        except Exception as e:
            raise Exception(str(e))
    