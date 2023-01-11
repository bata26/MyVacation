from datetime import datetime , timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import json
from managers.accommodationNodeManager import AccommodationNodeManager
from managers.accommodationNodeManager import AccommodationNodeManager
from managers.activityNodeManager import ActivityNodeManager
from managers.userNodeManager import UserNodeManager
from models.userNode import UserNode
from utility.logger import Logger
from models.activityNode import ActivityNode
from models.accommodationNode import AccommodationNode
import os


def worker():
    sched = BackgroundScheduler(job_defaults={'misfire_grace_time': 5})
    main()
    sched.add_job(main , trigger="interval" , days = 1 )
    sched.start()

def startup():
    sched = BackgroundScheduler(job_defaults={'misfire_grace_time': 5})
    now = datetime.now().replace(hour=0,second=0)
    scheduledTimestamp = now + timedelta(days=1)

    sched.add_job(worker , 'date' , run_date = scheduledTimestamp  ) 
    

def main():
    fileName = datetime.now().strftime("%Y-%m-%d") + '.log'
    
    with open(f'logs/{fileName}' , 'r+') as file:
        counter = 0
        for line in file:
            item = json.loads(line)
            try:
                if item["type"] == "activity":
                    id = item["_id"]
                    if item["operation"] == "DELETE":
                        ActivityNodeManager.deleteActivityNode(id)
                    else:
                        activityNode = ActivityNode(id , item["name"] , False)
                        ActivityNodeManager.updateActivityNode(activityNode)

                elif item["type"] == "accommodation":
                    id = item["_id"]
                    if item["operation"] == "DELETE":
                        AccommodationNodeManager.deleteAccommodationNode(id)
                    else:
                        accommodationNode = AccommodationNode(id , item["name"] , False)
                        AccommodationNodeManager.updateAccommodationNode(accommodationNode)
                    
                elif item["type"] == "user":
                    id = item["_id"]
                    if item["operation"] == "CREATE":
                        userNode = UserNode(id , item["name"])
                        UserNodeManager.createUserNode(userNode)
                    if item["operation"] == "DELETE":
                        UserNodeManager.deleteUserNode(id)
            except Exception:
                Logger.logWorkerError(f"Impossibile eseguire operazione {item}")  

if __name__ == "__main__":
    main()
