from flask import Flask, render_template, jsonify
from twilio.rest import Client

alerts = []
numOfWatches = 0

app = Flask(__name__)


# Recieve the latest alert (to be called by client-side javascript)
@app.route("/getAlert")
def getAlert():
    response = None
    if len(alerts) > 0:
        response = jsonify({"alertExists": True, "alertText": alerts.pop(0)})
    else:
        response = jsonify({"alertExists": False})

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/")
def home():
    return render_template("main.html")


# TODO: Move all watch related functions to a separate file
# This endpoint is to be called by watch
@app.route("/alert/<name>/<location>")
def recvAlert(name, location):
    msg = "Alert Recieved from: " + name + " At location: " + location
    alerts.append(msg)
    sendSmsMessage(msg)
    return "Alert recieved"


@app.route("/getWatchId")
def assignWatchId():
    global numOfWatches
    numOfWatches = numOfWatches + 1
    return str(numOfWatches)
