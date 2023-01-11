from managers.adminManager import AdminManager
from managers.accommodationNodeManager import AccommodationNodeManager
from managers.activityNodeManager import ActivityNodeManager
from models.accommodationNode import AccommodationNode
from models.activityNode import ActivityNode
from managers.userNodeManager import UserNodeManager

# This class contains methods reguarding the Admin behavior. Methods described here 
# are responsible for calling the underlay layer (Manager) and perform
# different kind of administrative operations like: delete of a specific user,
# approve of an Accommodation/Activity and so on. 
class AdminController:

    @staticmethod
    def approveAnnouncement(announcementID , destinationType , destinationName , user):
        try:
            try:
                AdminManager.approveAnnouncement(announcementID, user, destinationType)
            except Exception as e:
                raise Exception(str(e))
            try:
                if destinationType == "accommodation":
                    accommodationNode = AccommodationNode(announcementID, destinationName , approved=True)
                    AccommodationNodeManager.createAccommodationNode(accommodationNode)
                else:
                    activityNode = ActivityNode(announcementID, destinationName , approved=True)
                    ActivityNodeManager.createActivityNode(activityNode)
            except Exception as e:
                AdminManager.removeApprovalAnnouncement(announcementID, user, destinationType)
                raise Exception(str(e))
            return "", 200
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def deleteUser(userID , user):
        try:
            AdminManager.deleteUser(userID, user)
        except Exception as e:
            raise Exception(str(e))
        try:
            UserNodeManager.deleteUserNode(userID)
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def getUsers(user, username, name, surname, index, direction):
        try:
            result = AdminManager.getFilteredUsers(
            user, username, name, surname, index, direction
        )
            return result
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def getAnnouncementsToBeApproved(index , direction , destinationType):
        try:
            result = AdminManager.getAnnouncementsToApprove(
                index, direction, destinationType
            )
            return result
        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    def getAnnouncementToBeApprovedByID(announcementID, destinationType):
        try:
            result = AdminManager.getAnnouncementToApproveByID(announcementID, destinationType)
            return result
        except Exception as e:
            raise Exception(str(e))