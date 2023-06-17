from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# CREATE - Controller Users

@app.route("/register", methods=['POST'])
def register():

    data = request.form.copy()

    if not User.validate_user(data):
        return redirect("/")
    
    data["pword"] = bcrypt.generate_password_hash(data["pword"])
    
    user_id = User.save_user(data)
    session["user_id"] = user_id

    return redirect("/recipes")

# READ - Controller Users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():

    data = request.form

    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Incorrect email/password!", "login")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user_in_db.password, data["password"]):
        flash("Incorrect email/password!", "login")
        return redirect("/")

    session["user_id"] = user_in_db.id

    return redirect("/recipes")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")