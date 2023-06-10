from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_app.models.user import User
from datetime import datetime

@app.route("/")
def index():
    return redirect("/users")

@app.route("/users")
def read():
    session.clear()
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
    if session:
        fname = session["fname"]
        lname = session["lname"]
        email = session["email"]
    else:
        fname = ""
        lname = ""
        email = ""
    print(fname,lname,email)
    return render_template("create.html", fname = fname, lname = lname, email = email)

@app.route("/process", methods=["POST"])
def create():
    session.clear()
    if not User.validate_user(request.form):
        session["fname"] = request.form["first_name"]
        session["lname"] = request.form["last_name"]
        session["email"] = request.form["email"]
        return redirect('/users/new')
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