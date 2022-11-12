from controllers.accomodationsManager import AccomodationsManager
from flask import Flask, abort, request, jsonify, Response
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
import datetime
from datetime import timedelta , datetime
import logging
from markupsafe import escape

load_dotenv()
application = Flask(__name__)


if __name__ == "__main__":
    application.run(threaded=True , debug=True , use_reloader=False)