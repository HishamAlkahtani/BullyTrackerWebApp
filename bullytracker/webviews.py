from flask import render_template, jsonify
from bullytracker import app
from bullytracker.watchendpoints import alerts
from flask_login import login_required


@app.route("/")
@login_required
def home():
    return render_template("dashboard.html", alertList=alerts)


@app.route("/clearAlerts")
@login_required  # ??? Stuff are horrible right now!
def clearAlerts():
    alerts.clear()
    return "List Cleared"


@app.route("/manageWhatsappList")
@login_required
def getManageWhatsappPage():
    return render_template("manageWhatsappList.html", numbers=[])
