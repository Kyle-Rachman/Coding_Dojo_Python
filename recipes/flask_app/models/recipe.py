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

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes_schema').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        data = {"id" : id}
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes(name, description, under, instructions, date_made, created_at, updated_at, users_id) VALUES (%(name)s, %(description)s, %(under)s, %(instructions)s, %(date_made)s, NOW(), NOW(), %(user)s)"
        return connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def edit(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, under = %(under)s, instructions = %(instructions)s, date_made = %(date_made)s where id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM recipes where id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query, data)
    
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