import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, initialize_app

# cred.json is NOT included in the repo!
cred = credentials.Certificate("cred.json")
firebase_admin_app = initialize_app(cred)

db = firestore.client()

school_collection = db.collection("schools")
watch_collection = db.collection("watches")

def add_user(user):
    school_exists = school_collection.document(user["schoolName"]).get().exists
    # If account creator is an admin, add a new school to the list
    # (every admin has one school and every school has one admin)
    if user["accountType"] == "schoolAdmin":

        # An admin accounts creates a school, so school name must not be taken!
        if school_exists:
            return False

        response = school_collection.document(user["schoolName"]).set(
            {"adminAccount": user["username"]}
        )

    elif user["accountType"] == "parentAccount":
        # A parent only signs up to an existing school
        if not school_exists:
            return False

    user_collection = db.collection("users")
    user_data = user.copy()
    user_data.pop("username")

    user_collection.document(user["username"]).set(user_data)

    return True

def get_watch(watch_id):
    return watch_collection.document(watch_id).get()

def check_if_watch_exists(watch_id):
    return get_watch(watch_id).exists

def set_watch(watch_id, dict):
    watch_collection.document(watch_id).set(dict)

def add_watch(watch_id):
    watch_collection.document(watch_id).set({
        "isActive": False
    })
