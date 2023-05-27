from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users")
def read():
    users = User.get_all()
    return render_template("read.html", all_users = users)

@app.route("/users/new")
def entry():
    return render_template("create.html")

@app.route("/process", methods=["POST"])
def create():
    data = {
        "fname" : request.form["first_name"],
        "lname" : request.form["last_name"],
        "email" : request.form["email"]
    }
    User.save(data)
    return redirect("/users")