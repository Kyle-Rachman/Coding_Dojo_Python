from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from datetime import datetime

@app.route("/recipes/new")
def new_recipe():
    if "user_id" not in session:
        return redirect("/")
    user = User.get_one(session["user_id"])
    return render_template("new_recipe.html", user = user)

@app.route("/create", methods=['POST'])
def create():
    if not Recipe.validate_recipe(request.form):
        return redirect("/recipes/new")
    
    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "under" : request.form['under'],
        "instructions" : request.form['instructions'],
        "date_made" : request.form['date_made'],
        "user" : session['user_id']
    }
    
    Recipe.save(data)
    return redirect("/recipes")


@app.route("/recipes/<int:id>")
def view_recipe(id):
    if "user_id" not in session:
        return redirect("/")
    user = User.get_one(session["user_id"])
    recipe = Recipe.get_one(id)
    recipe.user = User.get_one(recipe.users_id)
    recipe.date_made = recipe.date_made.strftime("%B %d, %Y")
    return render_template("single_recipe.html", user = user, recipe = recipe)

@app.route("/destroy_recipe/<int:id>")
def destroy(id):
    data = {
        "id" : id
    }
    Recipe.destroy(data)
    return redirect("/recipes")

@app.route("/recipes/edit/<int:id>")
def edit_recipe(id):
    if "user_id" not in session:
        return redirect("/")
    recipe = Recipe.get_one(id)
    return render_template("edit_recipe.html", recipe = recipe)

@app.route("/edit", methods=['POST'])
def edit():
    if not Recipe.validate_recipe(request.form):
        return redirect(url_for('edit_recipe', id=request.form['id']))
    
    data = {
        "id" : request.form['id'],
        "name" : request.form['name'],
        "description" : request.form['description'],
        "under" : request.form['under'],
        "instructions" : request.form['instructions'],
        "date_made" : request.form['date_made'],
        "user" : session['user_id']
    }
    
    Recipe.edit(data)
    return redirect("/recipes")