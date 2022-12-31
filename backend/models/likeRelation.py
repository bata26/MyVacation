class LikeRelation:

    def __init__(self , userNode , accomodationNode=None , activityNode=None):
        self.user = userNode

        if(accomodationNode != None):
            self.accomodation = accomodationNode
        elif(activityNode != None):
            self.activity = activityNode

            