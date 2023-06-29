from flask_app import app
from flask import render_template, redirect, request, session, url_for
from flask_app.models import recipe

# CREATE - Controller Recipes

@app.route("/recipes/create", methods=['POST'])
def create_recipe():
    data = request.form
    if not recipe.Recipe.create_recipe(data):
        return redirect("/recipes/new")
    return redirect("/recipes")

@app.route("/recipes/new")
def new_recipe():
    if "user_id" not in session:
        return redirect("/")
    return render_template("new_recipe.html")

# READ - Controller Recipes

@app.route("/recipes")
def recipes():
    if "user_id" not in session:
        return redirect("/")
    recipes = recipe.Recipe.get_all_recipes_with_chefs()
    return render_template("recipes.html", recipes = recipes)

@app.route("/recipes/<int:recipe_id>")
def view_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/")
    current_recipe = recipe.Recipe.get_recipe_with_chef_by_id(recipe_id)
    current_recipe.date_made = current_recipe.date_made.strftime("%B %d, %Y")
    if not current_recipe:
        return redirect("/recipes")
    return render_template("single_recipe.html", recipe = current_recipe)

# UPDATE - Controller Recipes

@app.route("/recipes/edit/<int:recipe_id>")
def edit_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/")
    current_recipe = recipe.Recipe.get_recipe_by_id(recipe_id)
    if not current_recipe:
        return redirect("/recipes")
    if current_recipe.users_id != session["user_id"]:
        return redirect("/recipes")
    return render_template("edit_recipe.html", recipe = current_recipe)

@app.route("/recipes/edit", methods=['POST'])
def update_recipe():
    data = request.form
    if not recipe.Recipe.update_recipe(data):
        return redirect(url_for('edit_recipe', recipe_id=data['recipe_id']))
    return redirect("/recipes")

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
    return redirect("/recipes")