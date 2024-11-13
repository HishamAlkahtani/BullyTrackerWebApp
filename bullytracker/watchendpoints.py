# Contains all the endpoints that the watch will make requests to

from bullytracker import app, firestoredb, messaging, alerts
from flask import jsonify, request, make_response
import uuid


# NOT THREAD SAFE! Change later, use firestore...? maybe cache active alerts?
# alerts = []


# The app recieves alerts from the watch on this endpoint
@app.route("/watchAPI/alert/<watch_id>/<lat>/<long>")
def recv_alert(watch_id, lat, long):
    if alerts.process_alert(watch_id, float(lat), float(long)):
        return "Alert recieved"
    else:
        return make_response("Alert failed", 400)


# Tries to assign the shortest id possible (for readability)
@app.route("/watchAPI/getWatchId")
def assign_watch_id():
    watch_id_length = 4
    attempt = 0
    short_id = None

    while watch_id_length <= 32:
        full_uuid = uuid.uuid4().hex
        short_id = full_uuid[-watch_id_length:]

        if not firestoredb.check_if_watch_exists(short_id):
            break

        attempt += 1
        if attempt % 3 == 0:
            watch_id_length += 1
        short_id = None

    if not short_id is None:
        firestoredb.add_watch(short_id)
        return jsonify({"watchId": short_id})


# The watch calls this endpoint to check whether it has been linked to a school yet or not
# If the school admin tries to link the watch to a school, this endpoint will return the
# name of the school and the school admin...
@app.route("/watchAPI/checkSetupStatus/<watch_id>", methods=["GET", "POST"])
def check_setup_status(watch_id):
    if request.method == "GET":
        watch = firestoredb.get_watch(watch_id).to_dict()
        return jsonify(watch)

    elif request.method == "POST":
        watch_response = request.json
        not_active_empty_watch = {"isActive": False}

        # Only the watch can set the isActive field to true!
        # So, if the watch responds with isActive = true, the watch accepts
        # the setup request.
        if watch_response["isActive"] == True:
            prev_watch_info = firestoredb.get_watch(watch_id).to_dict()

            if watch_response["schoolName"] != prev_watch_info.get("schoolName"):
                # This should never happen but just in case.
                # The watch acccepts to be set up but agreed
                # to a different school than the one in db.
                firestoredb.set_watch(watch_id, not_active_empty_watch)
                print("Watch accepts set up but schoolName mismatch!!")
                return jsonify(not_active_empty_watch)

            firestoredb.set_watch(watch_id, watch_response)
            return watch_response

        else:

            # remove old school name, thereby canceling the setup request
            firestoredb.set_watch(watch_id, not_active_empty_watch)
            return jsonify(not_active_empty_watch)
