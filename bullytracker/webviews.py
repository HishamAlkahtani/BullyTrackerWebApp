# Contains all the views for the frontend

from flask import render_template
from bullytracker import app
from bullytracker.watchendpoints import alerts
from flask_login import login_required


@app.route("/")
@login_required
def home():
    return render_template("dashboard.html", alertList=alerts)


@app.route("/clearAlerts")
@login_required  # ??? Stuff are horrible right now!
def clear_alerts():
    alerts.clear()
    return "List Cleared"


@app.route("/manageWhatsappList")
@login_required
def get_manage_whatsapp_page():
    return render_template("manageWhatsappList.html", numbers=[])
