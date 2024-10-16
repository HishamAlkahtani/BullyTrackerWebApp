from bullytracker import app
from bullytracker.user import User

import uuid
from flask_login import LoginManager, login_user
from flask import redirect, request, render_template

import firebase_admin
from firebase_admin import auth, credentials

# cred.json is NOT included in the repo!
cred = credentials.Certificate("cred.json")
firebase_admin_app = firebase_admin.initialize_app(cred)

app.secret_key = uuid.uuid4().hex

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login?next=" + request.path)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        idtoken = form["idtoken"]

        user = load_user(idtoken)
        if user is None:
            print("user is none")
            return render_template("login.html", failed=True)
        else:
            login_user(user)
            return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        email = form["email"]

        user_data = {"uid": username, "password": password, "email": email}

        auth.create_user(**user_data)

        return redirect("/login")
    else:
        return render_template("register.html")
