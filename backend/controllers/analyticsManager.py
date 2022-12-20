from .connection import MongoManager
import os
import datetime


class AnalyticsManager:

    @staticmethod
    def getUsersForMonth():
        client = MongoManager.getInstance()
        db = client[os.getenv("DB_NAME")]
        collection = db[os.getenv("USERS_COLLECTION")]
        year = datetime.datetime.now().year
        try:
            result = list(collection.aggregate([
                {"$match":
                 {"$expr":
                  {
                      "$eq": [{"$year": "$registrationDate"}, year]
                  }
                  }
                 },
                {
                    "$group": {
                        "_id": {"$month": "$registrationDate"},
                        "users": {
                            "$count": {}
                        }
                    }
                },
                {
                    "$project": {"month": "$_id", "users": "$users", "_id": 0}
                }]))

            print(result)
        except Exception as e:
            raise Exception("Impossibile ottenere: " + str(e))
