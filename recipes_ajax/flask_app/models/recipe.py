from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.under = data['under']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.chef = None

    # CREATE - MODELS Recipe

    @classmethod
    def create_recipe(cls, data):
        query = """
            INSERT INTO recipes(name, description, under, instructions, date_made, users_id)
            VALUES (%(name)s, %(description)s, %(under)s, %(instructions)s, %(date_made)s, %(users_id)s)
        ;"""
        if not Recipe.validate_recipe(data):
            return False
        return connectToMySQL('recipes_schema').query_db(query, data)

    # READ - MODELS Recipe

    @classmethod
    def get_all_recipes(cls):
        query = """
            SELECT *
            FROM recipes
        ;"""
        results = connectToMySQL('recipes_schema').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(recipe)
        return recipes
    
    @classmethod
    def get_all_recipes_with_chefs(cls):
        query = """
            SELECT *
            FROM recipes
            LEFT JOIN users
            ON users.id = recipes.users_id
        ;"""
        results = connectToMySQL('recipes_schema').query_db(query)
        recipes = []
        for recipe in results:
            recipe_with_chef = cls(recipe)
            recipe_with_chef.chef = user.User({
                'id' : results[0]['users.id'],
                'first_name' : results[0]['first_name'],
                'last_name' : results[0]['last_name'],
                'email' : results[0]['email'],
                'password' : results[0]['password'],
                'created_at' : results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at']
            })
            recipes.append(recipe_with_chef)
        return recipes
    
    @classmethod
    def get_all_recipes_with_chefs_serializable(cls):
        query = """
            SELECT *
            FROM recipes
            LEFT JOIN users
            ON users.id = recipes.users_id
        ;"""
        results = connectToMySQL('recipes_schema').query_db(query)
        recipes = []
        for recipe in results:
            recipe_with_chef = cls(recipe)
            recipe_with_chef.chef = user.User({
                'id' : recipe['users.id'],
                'first_name' : recipe['first_name'],
                'last_name' : recipe['last_name'],
                'email' : recipe['email'],
                'password' : recipe['password'],
                'created_at' : recipe['users.created_at'],
                'updated_at' : recipe['users.updated_at']
            }).__dict__
            recipes.append(recipe_with_chef.__dict__)
        return recipes
    
    @classmethod
    def get_newest_recipe_with_chef_serializable(cls):
        query = """
            SELECT *
            FROM recipes
            LEFT JOIN users
            ON users.id = recipes.users_id
            ORDER BY recipes.updated_at DESC
            LIMIT 1
        ;"""
        results = connectToMySQL('recipes_schema').query_db(query)
        recipe_with_chef = cls(results[0])
        recipe_with_chef.date_made = recipe_with_chef.date_made.strftime("%B %d, %Y")
        recipe_with_chef.chef = user.User({
                'id' : results[0]['users.id'],
                'first_name' : results[0]['first_name'],
                'last_name' : results[0]['last_name'],
                'email' : results[0]['email'],
                'password' : results[0]['password'],
                'created_at' : results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at']
            }).__dict__
        return recipe_with_chef.__dict__

    @classmethod
    def get_recipe_by_id(cls, recipe_id):
        query = """
            SELECT *
            FROM recipes
            WHERE id = %(id)s
        ;"""
        data = {"id" : recipe_id}
        results = connectToMySQL('recipes_schema').query_db(query, data)
        if not results:
            return None
        return cls(results[0])
    
    @classmethod
    def get_recipe_with_chef_by_id(cls, recipe_id):
        query = """
            SELECT *
            FROM recipes
            LEFT JOIN users
            ON users.id = recipes.users_id
            WHERE recipes.id = %(id)s
        ;"""
        data = {"id" : recipe_id}
        results = connectToMySQL('recipes_schema').query_db(query, data)
        if not results:
            return None
        recipe = cls(results[0])
        recipe.chef = user.User({
            'id' : results[0]['users.id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'password' : results[0]['password'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at']
        })
        return recipe
    
    # UPDATE - MODELS Recipe

    @classmethod
    def update_recipe(cls, data):
        query = """
                UPDATE recipes
                SET name = %(name)s, description = %(description)s, under = %(under)s, instructions = %(instructions)s, date_made = %(date_made)s
                WHERE id = %(recipe_id)s
            ;"""
        if not Recipe.validate_recipe(data):
            return False
        connectToMySQL('recipes_schema').query_db(query, data)
        return True
    
    # DELETE - MODELS Recipe

    @classmethod
    def destroy_recipe_by_id(cls, recipe_id):
        query = """
                DELETE FROM recipes
                WHERE id = %(id)s
            ;"""
        data = {"id" : recipe_id}
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