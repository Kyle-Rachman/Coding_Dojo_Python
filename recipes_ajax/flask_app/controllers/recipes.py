from flask_app import app
from flask import render_template, redirect, request, session, url_for, jsonify, get_flashed_messages
from flask_app.models import recipe

# CREATE - Controller Recipes

@app.route("/recipes/create", methods=['POST'])
def create_recipe():
    data = request.form
    if not recipe.Recipe.create_recipe(data):
        return jsonify(get_flashed_messages(category_filter=["recipe"]))
    return jsonify(message="Making a new recipe!")

# READ - Controller Recipes

@app.route("/recipes")
def recipes():
    if "user_id" not in session:
        return redirect("/")
    return render_template("recipes.html")

@app.route("/read/recipes")
def read_recipes():
    return jsonify(recipe.Recipe.get_all_recipes_with_chefs_serializable())

@app.route("/read/new_recipe")
def read_new_recipe():
    return jsonify(recipe.Recipe.get_newest_recipe_with_chef_serializable())
    
# READ/UPDATE - Controller Recipes

@app.route("/recipes/<int:recipe_id>")
def view_and_edit_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/")
    current_recipe = recipe.Recipe.get_recipe_with_chef_by_id(recipe_id)
    if not current_recipe:
        return redirect("/recipes")
    if current_recipe.users_id != session["user_id"]:
        return render_template("single_recipe.html", recipe = current_recipe)
    else:
        return render_template("edit_recipe.html", recipe = current_recipe)

@app.route("/recipes/edit", methods=['POST'])
def update_recipe():
    data = request.form
    if not recipe.Recipe.update_recipe(data):
        return jsonify(get_flashed_messages(category_filter=["recipe"]))
    return jsonify(message="Updating recipe!")

# DELETE - Controller Recipes

@app.route("/recipes/destroy/<int:recipe_id>")
def destroy_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/")
    current_recipe = recipe.Recipe.get_recipe_by_id(recipe_id)
    if not current_recipe:
        return redirect("/recipes")
    if current_recipe.users_id != session["user_id"]:
        return redirect("/recipes")
    recipe.Recipe.destroy_recipe_by_id(recipe_id)
    return jsonify(message="Deleted recipe")