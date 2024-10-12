from bullytracker import app
from bullytracker.user import User

import uuid
from flask_login import LoginManager, login_user
from flask import redirect, request, render_template

app.secret_key = uuid.uuid4().hex

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.init_app(app)

# Temporary in memory user dict, for testing...
users = {"user": User("user", "user")}


@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login?next=" + request.path)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = str(form["password"])
        user = load_user(username)
        if user is None:
            print("user is none")
            return render_template("login.html", failed=True)
        elif user.validatePassword(password):
            login_user(user)
            return redirect("/")
        else:
            print("wrong password")
            return render_template("login.html", failed=True)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        users.update({username: User(username, password)})
        return redirect("/login")
    else:
        return render_template("register.html")
