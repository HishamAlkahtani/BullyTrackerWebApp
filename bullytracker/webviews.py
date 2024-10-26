# Contains all the views for the frontend

from flask import render_template, request, jsonify, abort
from bullytracker import app
from bullytracker.watchendpoints import alerts
from bullytracker import firestoredb
from flask_login import login_required, current_user


@app.route("/")
@login_required
def home():
    # TODO: put relative stuff...
    return render_template("dashboard.html", alertList=alerts)


@app.route("/clearAlerts")
@login_required
def clear_alerts():
    alerts.clear()
    return "List Cleared"


@app.route("/manageWhatsappList")
@login_required
def get_manage_whatsapp_page():
    return render_template("manageWhatsappList.html", numbers=[])


@app.route("/manageStudentWatches")
@login_required
def manage_student_watches_page():
    if current_user.user_data["accountType"] != "schoolAdmin":
        return abort(401)

    watches = firestoredb.get_watches_by_school_name(
        current_user.user_data["schoolName"]
    )
    return render_template("manageStudentWatches.html", watch_list=watches)


@app.route("/addWatch/<watch_id>")
@login_required
def add_watch(watch_id):
    # Only school admins can add watches
    if current_user.user_data["accountType"] != "schoolAdmin":
        return abort(401)

    if not firestoredb.check_if_watch_exists(watch_id):
        return jsonify({"requestReceived": False, "msg": "Watch does not exist"})

    watch = firestoredb.get_watch(watch_id).to_dict()

    if watch.get("schoolName"):
        return jsonify(
            {
                "requestReceived": False,
                "msg": "Watch is unavailable",
            }
        )

    # We now know watch exists, and hasn't been linked to a school
    firestoredb.set_watch(
        watch_id,
        {
            "isActive": watch["isActive"],
            "schoolName": current_user.user_data["schoolName"],
        },
    )

    return jsonify(
        {
            "requestReceived": True,
            "msg": "Setup request sent to watch, click accept on the watch up to continue the setup process...",
        }
    )


@app.route("/getWatchSetupStatus/<watch_id>")
@login_required
def get_watch_setup_status(watch_id):
    if current_user.user_data["accountType"] != "schoolAdmin":
        return abort(401)

    watch = firestoredb.get_watch(watch_id).to_dict()

    if not watch.get("schoolName"):
        return jsonify(
            {"complete": True, "sucess": False, "msg": "Watch rejected setup"}
        )

    if watch["schoolName"] != current_user.user_data["schoolName"]:
        return jsonify(
            {
                "complete": True,
                "success": False,
                "msg": "An unexpected error has occurred",
            }
        )

    if watch["isActive"]:
        return jsonify(
            {"complete": True, "success": True, "msg": "Watch added successfully!"}
        )

    return jsonify({"complete": False})


@app.route("/cancelWatchSetupRequest/<watch_id>")
@login_required
def cancel_watch_setup_process(watch_id):
    # TODO
    pass


@app.route("/removeWatch/<watch_id>")
@login_required
def remove_watch(watch_id):
    # TODO
    pass


# Recieve the latest alert (to be called by client-side javascript)
# @app.route("/getAlert")
# def getAlert():
#     response = None
#     if len(alerts) > 0:
#         response = jsonify({"alertExists": True, "alertText": alerts.pop(0)})
#     else:
#         response = jsonify({"alertExists": False})

#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
