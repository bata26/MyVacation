

@application.route('/admin/annuncements' , methods = ['GET'])
@required_token
def getAnnouncementToBeApproved():
    result = AdminManager.getItemToApprove()
    return result , 200