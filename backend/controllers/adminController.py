

@application.route('/admin/annuncements' , methods = ['GET'])
#@required_token
def getAnnouncementToBeApproved():
    result = AdminManager.getAnnouncementToApprove()
    return result , 200


@application.route('/admin/annuncements/<announcementID>' , methods = ['POST'])
#@required_token
def getAnnouncementToBeApproved(announcementID):
    #print(announcementID)
    return result , 200
