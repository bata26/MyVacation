class LikeRelation:

    def __init__(self , userNode , accommodationNode=None , activityNode=None):
        self.user = userNode

        if(accommodationNode != None):
            self.accommodation = accommodationNode
        elif(activityNode != None):
            self.activity = activityNode

            