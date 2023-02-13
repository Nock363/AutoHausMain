from flask import Flask
from flask import render_template
import sys
sys.path.insert(0, '../')
from Handler.DatabaseHandlers import MongoHandler
app = Flask(__name__)

mongo = MongoHandler()

@app.route("/")
def main():
    sensors = list(mongo.getSensors())
    #return "<p>Hello</p>"
    return f"<p>Hello</p><p>{str(sensors)}</p>"

@app.route("/sensoren")
def sensorenSite():
    sensors = list(mongo.getSensors())
    print(sensors)
    #return "<p>Hello</p>"
    return render_template("sensoren.html",sensors=sensors)