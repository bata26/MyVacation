from controllers.userManager import UserManager
from flask import Flask, abort, request, jsonify, Response
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
import datetime
from datetime import timedelta , datetime
import logging
from markupsafe import escape

@application.route('/users/<user_id>' , methods = ['DELETE'])
def deleteUserById (user_id):
    userId = escape(user_id)
    user = {
        "type" : "admin"
    }
    result = UserManager.deleteUser(userId , user)
    print(f"delete result : {result}")
    return "" , 200

@application.route('/users/<user_id>' , methods = ['GET'])
def getUserById (user_id):
    userId = escape(user_id)
    result = UserManager.getUserFromId(userId)
    return result , 200

@application.route('/users' , methods = ['GET'])
def getUsers():
    args = request.args
    name = args.get("name")
    surname = args.get("surname")
    user = {
            "type" : "admin"
        }
    result = UserManager.getFilteredUsers(user, name , surname)
    print(f"result : {result}")
    result["_id"] = str(result["_id"])
    return result , 200