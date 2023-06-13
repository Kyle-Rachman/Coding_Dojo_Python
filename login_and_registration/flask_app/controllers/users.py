from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if not session:
        return redirect("/")
    user = User.get_one(session["user_id"])
    return render_template("dashboard.html", user = user)

@app.route("/register", methods=['POST'])
def register():
    data = {
        "fname" : request.form["first_name"],
        "lname" : request.form["last_name"],
        "email" : request.form["email"],
        "pword" : request.form["password"],
        "confirm" : request.form["confirm"]
    }
    if not User.validate_user(data):
        return redirect("/")
    data["pword"] = bcrypt.generate_password_hash(data["pword"])
    user_id = User.save(data)
    session["user_id"] = user_id

    return redirect("/dashboard")

@app.route("/login", methods=['POST'])
def login():
    data = {
        "email" : request.form["email"]
    }

    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid email", "login")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user_in_db.password,request.form["password"]):
        flash("Incorrect password!", "login")
        return redirect("/")

    session["user_id"] = user_in_db.id

    return redirect("/dashboard")

@app.route("/logout", methods=['POST'])
def logout():
    session.clear()
    return redirect("/")