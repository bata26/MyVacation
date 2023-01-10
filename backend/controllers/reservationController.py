from managers.reservationManager import ReservationManager
import dateparser
from models.reservation import Reservation
from datetime import date

class ReservationController:

    @staticmethod
    def bookAccommodation(requestBody , user):
        accommodation = requestBody["accommodation"]
        startDatetime = dateparser.parse(requestBody["startDate"])
        endDatetime = dateparser.parse(requestBody["endDate"])
        nightNumber = (endDatetime - startDatetime).days
        totalExpense = nightNumber * int(accommodation["price"])
        city = accommodation["city"]
        hostID = accommodation["hostID"]

        if startDatetime.date() < date.today():
            raise Exception("Impossibile prenotare")
        if endDatetime < startDatetime:
            raise Exception("Impossibile prenotare")

        reservation = Reservation(
            user["_id"],
            accommodation["_id"],
            "accommodation",
            startDatetime,
            totalExpense,
            city,
            hostID,
            endDate=endDatetime,
        )
        try:
            ReservationManager.book(reservation)
            return "OK", 200
        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    def bookActivity(requestBody , user):
        activity = requestBody["activity"]
        startDate = dateparser.parse(requestBody["startDate"])
        city = activity["city"]
        hostID = activity["hostID"]

        if startDate.date() < date.today():
            raise Exception("Impossibile prenotare")

        reservation = Reservation(
            user["_id"],
            activity["_id"],
            "activity",
            startDate,
            activity["price"],
            city,
            hostID,
        )
        
        try:
            ReservationManager.book(reservation)
        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    def updateReservation(requestBody , user):
        newStartDate = requestBody["startDate"]
        reservation = requestBody["reservation"]
        newEndDate = None
        if reservation["destinationType"] == "accommodation":
            newEndDate = requestBody["endDate"]
        try:
            ReservationManager.updateReservation(reservation, newStartDate, newEndDate , user)
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def getReservationsByUserID(userID):
        try:
            result = ReservationManager.getReservationsByUser(userID)
            return result
        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    def getReservationsByHostID(hostID):
        try:
            result = ReservationManager.getReservationsByHost(hostID)
            return result
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def deleteReservation(reservationID , user):
        try:
            ReservationManager.deleteReservation(reservationID , user)
        except Exception as e:
            return str(e), 500