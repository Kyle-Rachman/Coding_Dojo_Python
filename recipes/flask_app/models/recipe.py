from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.under = bool(data['under'])
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.chef = None


    # CREATE - MODELS
    @classmethod
    def save_recipe(cls, data):
        query = "INSERT INTO recipes(name, description, under, instructions, date_made, users_id) VALUES (%(name)s, %(description)s, %(under)s, %(instructions)s, %(date_made)s, %(user)s)"
        recipe_id = connectToMySQL('recipes_schema').query_db(query, data)
        return recipe_id

    # READ - MODELS

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes_schema').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def get_recipe_by_id(cls, id):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        data = {"id" : id}
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_recipe_with_chef_by_recipe_id(cls, id):
        query = "SELECT * FROM users LEFT JOIN recipes ON recipes.users_id = users.id WHERE recipes.id = %(id)s;"
        data = {"id" : id}
        results = connectToMySQL('recipes_schema').query_db(query, data)
        recipe = cls(results[0])
        recipe.chef = results[0]["first_name"] + " " + results[0]["last_name"]
        return recipe

    # UPDATE - MODELS

    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, under = %(under)s, instructions = %(instructions)s, date_made = %(date_made)s where id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query, data)
    
    # DELETE - MODELS

    @classmethod
    def destroy_recipe(cls, data):
        query = "DELETE FROM recipes where id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query, data)

    # VALIDATIONS

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if not recipe["name"]:
            flash("Name must not be blank", "recipe")
            is_valid = False
        else:
            if len(recipe["name"]) < 3:
                flash("Name must be at least three characters", "recipe")
                is_valid = False

        if not recipe["description"]:
            flash("Description must not be blank", "recipe")
            is_valid = False
        else:
            if len(recipe["description"]) < 3:
                flash("Description must be at least three characters", "recipe")
                is_valid = False

        if not recipe["instructions"]:
            flash("Instructions must not be blank", "recipe")
            is_valid = False
        else:
            if len(recipe["instructions"]) < 3:
                flash("Instructions must be at least three characters", "recipe")
                is_valid = False

        if not recipe["date_made"]:
            flash("Recipe needs a date cooked/made", "recipe")
            is_valid = False

        if "under" not in recipe:
            flash("Was the recipe made in under 30 minutes?", "recipe")
            is_valid = False

        return is_valid