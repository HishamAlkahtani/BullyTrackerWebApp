# for Processing incoming SOS alerts from the watch
# Also, handles geofencing features, mainly transforming a location (coordinates), to a string
# representing the location at the coordinates (where the student is in the school,
# room number for example, or general whereabouts)

from bullytracker import messaging, firestoredb, geofencing
from datetime import datetime


def process_alert(watch_id, lat, long):
    watch = firestoredb.get_watch(watch_id).to_dict()

    if not watch.get("isActive"):
        return False

    school_name = watch.get("schoolName")

    school = firestoredb.get_school(school_name)

    if not school.exists:
        return False

    list_of_boundaries = school.to_dict().get("boundaries")

    if not list_of_boundaries:
        list_of_boundaries = []

    location = geofencing.determine_location(lat, long, list_of_boundaries)

    if not firestoredb.add_active_alert(watch_id, datetime.now(), location):
        return False

    # add_active_alert checks that the watch is active and assigned to a school
    # if it is a active, adds the alert to the school and returns true.
    watch_data = firestoredb.get_watch(watch_id).to_dict()
    messaging_list = firestoredb.get_messaging_list(watch_data["schoolName"])

    name = watch_data.get("studentName")

    if not name:
        name = "Name not set! watchId: " + watch_id

    for contact in messaging_list:
        messaging.send_sms_alert(contact["phoneNumber"], name, location)

    return True
