class LikeRelation:

    def __init__(self , userNode , accommodationNode=None , activityNode=None):
        self.user = userNode

        if(accommodationNode is not None):
            self.accommodation = accommodationNode
        elif(activityNode is not None):
            self.activity = activityNode

            