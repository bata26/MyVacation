import logging
from datetime import datetime
import json
class Logger:
    __instance = None

    @staticmethod
    def getInstance():
         if Logger.__instance == None:
            Logger()
         return Logger.__instance
    
    def __init__(self):
        name = "main"
        #log_format = '%(asctime)s  %(name)3s  %(levelname)8s  %(message)s'
        log_format = '%(message)s'
        now = datetime.now()
        logging.basicConfig(level=logging.DEBUG,
                            format=log_format,
                            filename=now.strftime("./logs/%Y-%m-%d") + '.log',
                            filemode='a+')
        logging.getLogger(name).handlers = []
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(logging.Formatter(log_format))
        logging.getLogger(name).addHandler(console)
        logging.getLogger('apscheduler.scheduler').propagate = False
        logging.getLogger('werkzeug').propagate = False
        logging.getLogger('root').propagate = False
        Logger.__instance = logging.getLogger(name)
        Logger.__instance.info("[")
        

    @staticmethod
    def writeOnFile(msg):
        logger = Logger.getInstance()
        logger.info(msg + ",")

    @staticmethod
    def addNodeToFile(destinationType , destinationID , operation="" , username = ""):
        logger = Logger.getInstance()
        messageDict = {"type" : destinationType ,"_id" : destinationID , "operation" : operation , "username" : username}
        msg = json.dumps(messageDict)
        logger.info(msg + ",")
    
    @staticmethod
    def logWorkerError(msg):
        logger = Logger.getInstance()
        logger.warning("[WARNING] " + msg)