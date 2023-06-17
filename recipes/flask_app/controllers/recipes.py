from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from datetime import datetime

# CREATE - Controller Recipes

@app.route("/recipes/create", methods=['POST'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect("/recipes/new")
    
    Recipe.save_recipe(request.form)
    
    return redirect("/recipes")

# READ - Controller Recipes

@app.route("/recipes")
def recipes():
    if "user_id" not in session:
        return redirect("/")
    user = User.get_user_by_id(session["user_id"])
    recipes = Recipe.get_all()
    for recipe in recipes:
        recipe.chef = User.get_user_by_id(recipe.users_id)
    return render_template("recipes.html", user = user, recipes = recipes)

@app.route("/recipes/new")
def new_recipe():
    if "user_id" not in session:
        return redirect("/")
    user = User.get_user_by_id(session["user_id"])
    return render_template("new_recipe.html", user = user)

@app.route("/recipes/<int:id>")
def view_recipe(id):
    if "user_id" not in session:
        return redirect("/")
    user = User.get_user_by_id(session["user_id"])
    recipe = Recipe.get_recipe_with_chef_by_recipe_id(id)
    recipe.date_made = recipe.date_made.strftime("%B %d, %Y")
    return render_template("single_recipe.html", user = user, recipe = recipe)

@app.route("/recipes/edit/<int:id>")
def edit_recipe(id):
    if "user_id" not in session:
        return redirect("/")
    
    recipe = Recipe.get_recipe_by_id(id)

    return render_template("edit_recipe.html", recipe = recipe)


# UPDATE - Controller Recipes

@app.route("/recipes/edit", methods=['POST'])
def edit():
    if not Recipe.validate_recipe(request.form):
        return redirect(url_for('edit_recipe', id=request.form['id']))
    
    Recipe.edit_recipe(request.form)
    
    return redirect("/recipes")

# DELETE - Controller Recipes

@app.route("/recipes/destroy/<int:id>")
def destroy_recipe(id):
    data = {
        "id" : id
    }
    Recipe.destroy_recipe(data)
    return redirect("/recipes")