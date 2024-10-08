from flask import render_template, jsonify
from bullytracker import app
from bullytracker.watchendpoints import alerts


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
