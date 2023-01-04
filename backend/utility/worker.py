from datetime import datetime , timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import json
import os
from controllers.graphConnection import GraphManager
from controllers.accommodationNodeManager import AccommodationNodeManager
from controllers.activityNodeManager import ActivityNodeManager
from controllers.userNodeManager import UserNodeManager
from models.userNode import UserNode
from logger import Logger

def worker():
    sched = BackgroundScheduler(job_defaults={'misfire_grace_time': 5})
    main()
    sched.add_job(main , trigger="interval" , days = 1 )
    sched.start()

# funzione di startup iniziale, fa partire lo scheduler per il processo principale (schedule)
# in modo che parta sempre dopo le 45 e non cancelli la coda inutilmente
def startup():
    sched = BackgroundScheduler(job_defaults={'misfire_grace_time': 5})
    now = datetime.now().replace(hour=0,second=0)
    scheduledTimestamp = now + timedelta(days=1)

    sched.add_job(worker , 'date' , run_date = scheduledTimestamp  ) 
    

def main():
    fileName = datetime.now().strftime("%Y-%m-%d") + '.log'
    
    with open(f'../logs/{fileName}', 'rb+') as file:
        file.seek(-1, os.SEEK_END)
        file.truncate()

    with open(f'../logs/{fileName}' , 'a+') as file:
        file.write("\n]")
    
    with open(f'../logs/{fileName}' , 'r+') as file:
        file_contents = file.read()
    
    parsed_json = json.loads(file_contents)

    for item in parsed_json:
        try:
            if item["type"] == "activity":
                id = item["_id"]
                ActivityNodeManager.deleteActivityNode(id)
            elif item["type"] == "accommodation":
                id = item["_id"]
                AccommodationNodeManager.deleteAccommodationNode(id)
            elif item["type"] == "user":
                id = item["_id"]
                if item["operation"] == "CREATE":
                    userNode = UserNode(id , item["username"])
                    UserNodeManager.createUserNode(userNode)
        except Exception as e:
            Logger.logWorkerError(f"Impossibile eseguire operazione su {item['_id']}")
            #print(str(e))    

if __name__ == "__main__":
    main()
