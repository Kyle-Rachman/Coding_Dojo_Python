from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recipes")
def recipes():
    if "user_id" not in session:
        return redirect("/")
    user = User.get_one(session["user_id"])
    recipes = Recipe.get_all()
    for recipe in recipes:
        recipe.user = User.get_one(recipe.users_id)
        if recipe.under:
            recipe.under = "Yes"
        else:
            recipe.under = "No"
    return render_template("recipes.html", user = user, recipes = recipes)

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

    return redirect("/recipes")

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

    return redirect("/recipes")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")