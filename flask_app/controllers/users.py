from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# CREATE - Controller Users

@app.route("/register", methods=['POST'])
def register():
    data = request.form.copy()
    session["user_id"] = user.User.create_user(data)
    if not session["user_id"]:
        return redirect("/")
    session["user_name"] = user.User.get_user_by_id(session["user_id"]).first_name
    return redirect("/recipes")

# READ - Controller Users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    data = request.form
    session["user_id"] = user.User.login(data)
    if not session["user_id"]:
        return redirect("/")
    session["user_name"] = user.User.get_user_by_id(session["user_id"]).first_name
    return redirect("/recipes")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")