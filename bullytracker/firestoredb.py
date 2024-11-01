import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, initialize_app

# cred.json is NOT included in the repo!
cred = credentials.Certificate("cred.json")
firebase_admin_app = initialize_app(cred)

db = firestore.client()

school_collection = db.collection("schools")
watch_collection = db.collection("watches")
user_collection = db.collection("users")


def get_school(school_name):
    return school_collection.document(school_name).get()


def get_messaging_list(school_name):
    return get_school(school_name).to_dict()["messagingList"]


def add_to_messaging_list(school_name, contact):
    school = get_school(school_name).to_dict()
    school["messagingList"].append(contact)
    set_school(school_name, school)


def remove_contact(school_name, phone_number):
    school = get_school(school_name).to_dict()
    messaging_list = school["messagingList"]

    new_messaging_list = [
        contact for contact in messaging_list if contact["phoneNumber"] != phone_number
    ]

    school["messagingList"] = new_messaging_list
    set_school(school_name, school)


def set_school(school_name, data):
    school_collection.document(school_name).set(data)


def add_user(user):
    school_exists = school_collection.document(user["schoolName"]).get().exists
    # If account creator is an admin, add a new school to the list
    # (every admin has one school and every school has one admin)
    if user["accountType"] == "schoolAdmin":

        # An admin accounts creates a school, so school name must not be taken!
        if school_exists:
            return False

        school_collection.document(user["schoolName"]).set(
            {"adminAccount": user["username"]}
        )

    elif user["accountType"] == "parentAccount":
        # A parent only signs up to an existing school
        if not school_exists:
            return False

    user_data = user.copy()
    user_data.pop("username")

    user_collection.document(user["username"]).set(user_data)

    return True


def get_user(user_id):
    return user_collection.document(user_id).get()


def get_watch(watch_id):
    return watch_collection.document(watch_id).get()


def get_watches_by_school_name(school_name):
    # list of document snapshots
    watches_list = watch_collection.where(
        filter=firestore.FieldFilter("schoolName", "==", school_name)
    ).get()

    # list of dicts containng only neccessary data
    watch_list = []
    for watch in watches_list:
        watch_list.append(
            {
                "watchId": watch.id,
                "isActive": watch.to_dict().get("isActive"),
            }
        )

    return watch_list


# Active alerts are stored directly in school document
def add_active_alert(watch_id, timestamp, location):
    alert = {
        "watchId": watch_id,
        "timestamp": timestamp,
        "location": location,
    }

    watch_doc = get_watch(watch_id)

    if not watch_doc:
        print("watch_doc failed")
        return False

    watch = watch_doc.to_dict()
    school_name = watch.get("schoolName")

    if not watch.get("isActive") or not school_name:
        print("either not active or wrong school")
        return False

    school = get_school(school_name).to_dict()

    active_alerts = school.get("activeAlerts")
    print("ACTIVE ALERTS:" + str(active_alerts))

    if not active_alerts:
        active_alerts = [alert]
    else:
        active_alerts.append(alert)

    school["activeAlerts"] = active_alerts

    set_school(school_name, school)
    return True


def get_active_alerts(school_name):
    return get_school(school_name).to_dict().get("activeAlerts")


def clear_active_alerts(school_name):
    school_dict = get_school(school_name).to_dict()
    school_dict.pop("activeAlerts")
    set_school(school_name, school_dict)


def check_if_watch_exists(watch_id):
    return get_watch(watch_id).exists


def set_watch(watch_id, dict):
    watch_collection.document(watch_id).set(dict)


def add_watch(watch_id):
    watch_collection.document(watch_id).set({"isActive": False})
