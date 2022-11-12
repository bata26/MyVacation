from controllers.accomodationsManager import AccomodationsManager
from flask import Flask, abort, request, jsonify, Response
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
import datetime
from datetime import timedelta , datetime
import logging
from markupsafe import escape

@application.route('/accomodations/<accomodation_id>' , methods = ['DELETE'])
def deleteAccomodationById (accomodation_id):
    accomodationId = escape(accomodation_id)
    user = {
        "type" : "admin"
    }
    result = AccomodationsManager.deleteAccomodation(accomodationId , user)
    print(f"delete result : {result}")
    return "" , 200

@application.route('/accomodations/<accomodation_id>' , methods = ['GET'])
def getAccomodationById (accomodation_id):
    accomodationId = escape(accomodation_id)
    result = AccomodationsManager.getAccomodationsFromId(accomodationId)
    return result , 200

@application.route('/accomodations' , methods = ['GET'])
def getAccomodations():
    args = request.args
    city = args.get("city")
    guests = args.get("guests")
    start_date = args.get("start_date")
    end_date = args.get("end_date")
    result = AccomodationsManager.getFilteredAccomodation(start_date  , end_date  , city , guests)
    print(f"result : {result}")
    result["_id"] = str(result["_id"])
    return result , 200