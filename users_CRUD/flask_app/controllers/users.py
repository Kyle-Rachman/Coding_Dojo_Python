from flask_app import app
from flask import render_template, redirect, request, session, url_for
from flask_app.models.user import User
from datetime import datetime

@app.route("/")
def index():
    return redirect("/users")

@app.route("/users")
def read():
    users = User.get_all()
    return render_template("read.html", all_users = users)

@app.route("/users/<int:x>")
def read_one(x):
    user = User.get_one(x)
    user.created_at = user.created_at.strftime('%B %d, %Y')
    user.updated_at = user.updated_at.strftime('%B %d, %Y at %#I:%M %p')
    return render_template("read_one.html", user = user)

@app.route("/users/<int:x>/edit")
def edit(x):
    user = User.get_one(x)
    return render_template("edit.html", user = user)

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
    id = User.get_last().id
    return redirect(url_for('read_one', x = id))

@app.route("/update", methods=["POST"])
def update():
    data = {
        "id" : request.form["id"],
        "fname" : request.form["first_name"],
        "lname" : request.form["last_name"],
        "email" : request.form["email"],
        "updated_at": datetime.now()
    }
    User.update(data)
    id = request.form["id"]
    return redirect(url_for('read_one', x = id))

@app.route("/users/<int:x>/destroy")
def destroy(x):
    User.destroy(x)
    return redirect("/users")