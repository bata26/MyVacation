from managers.activityManager import ActivityManager
from managers.activityNodeManager import ActivityNodeManager
from managers.userManager import UserManager
from managers.reviewManager import ReviewManager
from managers.likeRelationManager import LikeRelationManager
from models.review import Review
from models.activity import Activity
from models.userNode import UserNode
from models.activityNode import ActivityNode
from models.likeRelation import LikeRelation

# This class contains methods reguarding the Activities behavior. Methods described here 
# are responsible for calling the underlay layer (Manager) and perform
# different kind of operations like: CRUD, statistic and so on.
class ActivityController:

    @staticmethod
    def getTopAdvInfo(activitiesID):
        try:
            result = ActivityManager.getActivitiesFromIdList(activitiesID)
            return result
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def deleteActivityById(activityID , user):
        try:
            ActivityManager.deleteActivity(activityID, user)
        except Exception as e:
            raise Exception(str(e))
        try:
            ActivityNodeManager.deleteActivityNode(activityID)
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def updateActivity(activityID, formData, user):
        try:
            ActivityManager.updateActivity(activityID, formData, user)
        except Exception as e:
            raise Exception(str(e))
        try:
            activityNode = ActivityNode(
                activityID,
                formData["name"],
                formData["approved"]
            )
            ActivityNodeManager.updateActivityNode(activityNode)
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def getActivityByID(activityID):
        try:
            res = ActivityManager.getActivityFromID(activityID)
            return res
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def getActivities(start_date, city, index, direction):
        try:
            res = ActivityManager.getFilteredActivities(start_date, city, index, direction)
            return res
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def insertActivity(formData , user):
        try:
            host = UserManager.getUserFromID(user["_id"])
            location = {
                "address": formData["address"],
                "city": formData["city"],
                "country": formData["country"],
            }
            activity = Activity(
                host["_id"],
                host["name"],
                location,
                formData["description"],
                formData["duration"],
                formData["price"],
                formData["img"][0],
                formData["name"],
                False
            )
            activityID = ActivityManager.insertNewActivity(activity)
            if user["role"] != "host":
                updatedRole = {"type": "host"}
                UserManager.updateUser(updatedRole, host["_id"])
            return {"activityID": str(activityID)}
        except Exception as e:
            return str(e), 500
    
    @staticmethod
    def insertReview(requestBody , user):
        try:
            destinationID =  requestBody["destinationID"]
            review = Review(
                user["_id"],
                destinationID,
                requestBody["score"],
                requestBody["description"],
                requestBody["reviewer"],
            )
            ReviewManager.insertNewReview(review , destinationID , "activity")
        except Exception as e:
            return str(e), 200
    
    @staticmethod
    def refuseActivity(activityID , user):
        try:
            ActivityManager.deleteActivity(activityID, user)
        except Exception as e:
            return str(e), 200
        try:
            ActivityNodeManager.deleteActivityNode(activityID)
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def getActivityByUserID(userID):
        try:
            res = ActivityManager.getActivityByUserID(userID)
            return res
        except Exception as e:
            return str(e), 200

    @staticmethod
    def likeActivity(requestBody , user):
        try:
            activityNode = ActivityNode(requestBody["likedAdvID"], requestBody["likedAdvName"])
            userNode = UserNode(user["_id"], user["username"])
            likeRelation = LikeRelation(userNode, activityNode=activityNode)
            LikeRelationManager.addLikeRelation(likeRelation)
        except Exception as e:
            return str(e), 200
    
    @staticmethod
    def dislikeActivity(requestBody , user):
        try:
            userNode = UserNode(user["_id"], user["username"])
            activityNode = ActivityNode(requestBody["unlikedAdvID"], requestBody["unlikedAdvName"])
            likeRelation = LikeRelation(userNode, activityNode=activityNode )
            LikeRelationManager.removeLikeRelation(likeRelation)
        except Exception as e:
            return str(e), 200

    @staticmethod
    def getCommonActivity(user , userID):
        try:
            userNode = UserNode(user["_id"], user["username"])
            res = ActivityNodeManager.getCommonLikedActivity(userNode, userID)
            return res
        except Exception as e:
            return str(e), 200
    
    @staticmethod
    def getTotalLikes(destinationID):
        try:
            res =  ActivityNodeManager.getTotalLikes(destinationID)
            return {"likes" : res}
        except Exception as e:
            return str(e), 200