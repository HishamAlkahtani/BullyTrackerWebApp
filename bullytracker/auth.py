from bullytracker import app
from bullytracker.user import User

from bullytracker import firestoredb

import uuid
from flask_login import LoginManager, login_user, logout_user
from flask import redirect, request, render_template

from firebase_admin import auth

# cred = credentials.Certificate("cred.json")
# firebase_admin_app = initialize_app(cred)


app.secret_key = uuid.uuid4().hex

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # This thing is ridiculous, it makes every single request slower!
    # This MUST be cached. currently it fetches ALL the data related to the user
    # with EVERY request!!
    return User(user_id)


# TODO: Redirect to the previously request page through cookies
@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        idtoken = form["idtoken"]

        login_user(load_user(idtoken))
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            form = request.form
            user = {
                "username": form["username"],
                "email": form["email"],
                "password": form["password"],
                "accountType": form["accountType"],
                "schoolName": form["schoolName"],
            }

            # Register the user to firebase authentication
            auth.create_user(
                **{
                    "uid": user["username"],
                    "password": user["password"],
                    "email": user["email"],
                }
            )

            # Store relevant user information in firestore
            user.pop("password")  # Password not needed in db, remove it
            if not firestoredb.add_user(user):
                auth.delete_user(user["username"])
                return render_template(
                    "register.html",
                    failed=True,
                    failure_message="An unexpected error has occurred",
                )

            return redirect("/login")

        except Exception as e:
            return render_template("register.html", failed=True, failure_message=str(e))
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")
