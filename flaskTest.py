from flask import Flask, request, jsonify
from flask_cors import CORS
from Handler.DatabaseHandlers import MongoHandler
from Handler.JsonHandlers import ConfigHandler
from multiprocessing import Event
from Scheduler import Scheduler
from flask import send_from_directory
import os


app = Flask(__name__)
app.run(host="0.0.0.0")