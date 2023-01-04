from controllers.accommodationManager import AccommodationManager
from flask import Flask, abort, request, jsonify, Response
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
import datetime
from datetime import timedelta , datetime
import logging
from markupsafe import escape

@application.route('/accommodations/<accommodation_id>' , methods = ['DELETE'])
def deleteAccommodationById (accommodation_id):
    accommodationId = escape(accommodation_id)
    user = {
        "type" : "admin"
    }
    result = AccommodationManager.deleteAccommodation(accommodationId , user)
    return "" , 200

@application.route('/accommodations/<accommodation_id>' , methods = ['GET'])
def getAccommodationById (accommodation_id):
    accommodationId = escape(accommodation_id)
    result = AccommodationManager.getAccommodationsFromId(accommodationId)
    return result , 200

@application.route('/accommodations' , methods = ['GET'])
def getAccommodations():
    args = request.args
    city = args.get("city")
    guests = args.get("guests")
    start_date = args.get("start_date")
    end_date = args.get("end_date")
    result = AccommodationManager.getFilteredAccommodation(start_date  , end_date  , city , guests)
    result["_id"] = str(result["_id"])
    return result , 200