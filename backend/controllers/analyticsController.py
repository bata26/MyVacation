from managers.analyticsManager import AnalyticsManager

# This class contains methods reguarding the Analytics behavior. Methods described here 
# are responsible for calling the underlay layer (Manager) and retrive informations
# reguarding statistics of the application.
class AnalyticsController:

    @staticmethod
    def getBestCities():
        try:
            result = AnalyticsManager.getTopCities()
            return result
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def getTopAdv():
        try:
            result = AnalyticsManager.getTopAdv()
            return result
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def getMonthReservations(user={}):
        try:
            result = AnalyticsManager.getReservationByMonth(user)
            return result
        except Exception as e:
            return str(e), 500
    
    @staticmethod
    def getUsersForMonth():
        try:
            res = AnalyticsManager.getUsersForMonth()
            return res
        except Exception as e:
            return str(e), 500

    @staticmethod
    def getAccommodationsAverageCost(user={}):
        try:
            res = AnalyticsManager.getAccommodationAverageCost(user)
            return res
        except Exception as e:
            return str(e), 500

    @staticmethod
    def getActivitiesAverageCost(user={}):
        try:
            res = AnalyticsManager.getActivityAverageCost(user)
            return res
        except Exception as e:
            return str(e), 500

    @staticmethod
    def getTotalReservations(user={}):
        try:
            return AnalyticsManager.getTotReservations(user)
            return res
        except Exception as e:
            return str(e), 500

    @staticmethod
    def getTotalAdvs(user={}):
        try:
            res = AnalyticsManager.getTotAdvs(user)
            return res
        except Exception as e:
            return str(e), 500