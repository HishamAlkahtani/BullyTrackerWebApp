# Contains all the views for the frontend

from flask import render_template, request, jsonify, abort, make_response, redirect
from bullytracker import app
from bullytracker import firestoredb, geofencing
from flask_login import login_required, current_user
import json


@app.route("/getActiveAlerts")
@login_required
def get_active_alerts():
    return jsonify(firestoredb.get_active_alerts(current_user.user_data["schoolName"]))


@app.route("/")
@login_required
def home():
    if current_user.user_data["accountType"] == "schoolAdmin":
        # Fetch active alerts
        alerts = firestoredb.get_active_alerts(current_user.user_data["schoolName"])
        if not alerts:
            alerts = []

        # Fetch and process student locations

        list_of_boundaries = (
            firestoredb.get_school(current_user.user_data["schoolName"])
            .to_dict()
            .get("boundaries")
        )

        if not list_of_boundaries:
            list_of_boundaries = []

        watches = firestoredb.get_watches_by_school_name(
            current_user.user_data["schoolName"]
        )

        locations = []

        for watch in watches:
            last_location = watch.get("lastLocation")

            if last_location:
                location = geofencing.determine_location(
                    last_location.get("lat"),
                    last_location.get("long"),
                    list_of_boundaries,
                )

                watch.update({"location": location})
                watch.update({"lastSeen": last_location.get("timestamp")})

                if location != "Unavailable":
                    watch.update(
                        {
                            "locationLink": geofencing.get_google_maps_link(
                                last_location.get("lat"), last_location.get("long")
                            )
                        }
                    )
            else:
                watch.update({"location": "Unavailable"})
                watch.update({"lastSeen": ""})

            if not watch.get("studentName"):
                watch.update(
                    {"studentName": "Name not set! watch id: " + watch["watchId"]}
                )

            locations.append(watch)

        return render_template(
            "adminDashboard.html", alertList=alerts, studentLocations=locations
        )

    elif current_user.user_data["accountType"] == "parentAccount":
        return render_template("parentDashboard.html")


@app.route("/clearAlerts")
@login_required
def clear_alerts():
    firestoredb.clear_active_alerts(current_user.user_data["schoolName"])
    return "List Cleared"


@app.route("/manageWhatsappList", methods=["GET", "POST"])
@login_required
def get_manage_whatsapp_page():
    school_name = current_user.user_data["schoolName"]

    if request.method == "POST":
        form = request.form
        contact = {
            "teacherName": form["teacherName"],
            "phoneNumber": form["phoneNumber"],
        }

        firestoredb.add_to_messaging_list(school_name, contact)

    messaging_list = firestoredb.get_messaging_list(school_name)

    if not messaging_list:
        messaging_list = []

    return render_template("manageWhatsappList.html", messaging_list=messaging_list)


@app.route("/removeContact/<phone_number>")
@login_required
def remove_contact(phone_number):
    school_name = current_user.user_data["schoolName"]
    firestoredb.remove_contact(school_name, phone_number)
    return redirect("/manageWhatsappList")


@app.route("/manageStudentWatches")
@login_required
def manage_student_watches_page():
    if current_user.user_data["accountType"] != "schoolAdmin":
        return abort(401)

    watches = firestoredb.get_watches_by_school_name(
        current_user.user_data["schoolName"]
    )
    return render_template("manageStudentWatches.html", watch_list=watches)


@app.route("/manageSchoolBoundaries")
@login_required
def manage_school_boundaries():
    if current_user.user_data["accountType"] != "schoolAdmin":
        return abort(401)

    school_name = current_user.user_data["schoolName"]
    school = firestoredb.get_school(school_name).to_dict()
    boundaries = school.get("boundaries")

    if not boundaries:
        boundaries = []

    return render_template("manageSchoolBoundaries.html", boundaries=boundaries)


@app.route("/manageSchoolBoundaries/clearBoundaries", methods=["POST"])
@login_required
def clear_school_boundaries():
    school_name = current_user.user_data["schoolName"]

    school = firestoredb.get_school(school_name).to_dict()

    school.update({"boundaries": []})

    firestoredb.set_school(school_name, school)

    return redirect("/manageSchoolBoundaries")


@app.route("/setCoordinates", methods=["POST", "GET"])
@login_required
def add_room_to_school_boundaries():
    if not current_user.user_data["accountType"] == "schoolAdmin":
        return abort(401)

    boundary = request.json
    print(boundary)

    school_name = current_user.user_data["schoolName"]

    firestoredb.add_boundary_to_school(school_name, boundary)

    response = jsonify({"msg": "success"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# Initiates the setup process by setting the appropriate fields
# The watch then will read the data from firestore, and communicate
# it's response by setting the appropriate fields
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


# To be called periodically by client-side javacsript
# while waiting for the watch to accept setup request
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


# Changes the student data associated with the watch_id...
# It should be noted that the current design is that the students have no collection
# of their own, once a watch is added, the student data is stored with the watch data...
# So the number of students the school can add equals the number of watches available...
@app.route("/editStudentData/<watch_id>", methods=["GET", "POST"])
@login_required
def editStudentData(watch_id):
    if current_user.user_data["accountType"] != "schoolAdmin":
        return abort(401)

    watch = firestoredb.get_watch(watch_id).to_dict()

    if not watch.get("schoolName"):
        return make_response("Watch is not active", 400)

    if not watch["schoolName"] == current_user.user_data["schoolName"]:
        return abort(401)

    if request.method == "GET":
        return render_template("editStudentData.html", watchId=watch_id)

    elif request.method == "POST":
        form = request.form

        watch["studentName"] = form["studentName"]
        watch["grade"] = form["grade"]

        firestoredb.set_watch(watch_id, watch)

        return redirect("/manageStudentWatches")


@app.route("/cancelWatchSetupRequest/<watch_id>")
@login_required
def cancel_watch_setup_process(watch_id):
    # This is the same as remove_watch()... so might should be removed, depends on how the
    # front end will look like. If the setup process includes waiting for the watch to accept
    # or it just shows up in the list but with an inactive status...
    pass


@app.route("/removeWatch/<watch_id>")
@login_required
def remove_watch(watch_id):
    watch = firestoredb.get_watch(watch_id).to_dict()

    school_name = watch.get("schoolName")

    if not school_name:
        return make_response("Error while fetching watch", 400)

    if (
        school_name != current_user.user_data["schoolName"]
        or current_user.user_data["accountType"] != "schoolAdmin"
    ):
        return abort(401)

    firestoredb.set_watch(watch_id, {"isActive": False})

    return redirect("/manageStudentWatches")


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
