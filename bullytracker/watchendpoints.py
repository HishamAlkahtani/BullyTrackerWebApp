# Contains all the endpoints that the watch will make requests to

from bullytracker import app
from bullytracker.firestoredb import check_if_watch_exists, add_watch
from flask import jsonify
import uuid


# NOT THREAD SAFE! Change later, use firestore?
alerts = []


# The app recieves alerts from the watch on this endpoint
@app.route("/alert/<name>/<location>")
def recv_alert(name, location):
    msg = "Alert Recieved from: " + name + " At location: " + location
    alerts.append(msg)
    print(msg)
    return "Alert recieved"


# Tries to assign the shortest id possible (for readability)
@app.route("/getWatchId")
def assign_watch_id():
    watch_id_length = 4
    attempt = 0
    short_id = None

    while watch_id_length <= 32:
        full_uuid = uuid.uuid4().hex
        short_id = full_uuid[-watch_id_length:]

        if not check_if_watch_exists(short_id):
            break

        attempt += 1
        if attempt % 3 == 0:
            watch_id_length += 1
        short_id = None

    add_watch(short_id)
    return jsonify({
        "watchId": short_id
    })
