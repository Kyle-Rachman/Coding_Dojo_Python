from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, redirect
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import recipe

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    # CREATE - MODELS

    @classmethod
    def create_user(cls, data):
        query = """
            INSERT INTO users(first_name, last_name, email, password)
            VALUES (%(fname)s, %(lname)s, %(email)s, %(pword)s)
        ;"""
        if not User.validate_user(data):
            return redirect("/")
        data["pword"] = bcrypt.generate_password_hash(data["pword"])
        return connectToMySQL('recipes_schema').query_db(query, data)

    # READ - MODELS

    @classmethod
    def get_all_users(cls):
        query = """
            SELECT *
            FROM users
        ;"""
        results = connectToMySQL('recipes_schema').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_user_by_id(cls, user_id):
        query = """
            SELECT *
            FROM users
            WHERE id = %(id)s
        ;"""
        data = {"id" : user_id}
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_user_by_email(cls, data):
        query = """
            SELECT *
            FROM users
            WHERE email = %(email)s
        ;"""
        results = connectToMySQL('recipes_schema').query_db(query, data)
        if not results:
            return False
        return cls(results[0])
    
    @classmethod
    def get_user_by_id_with_recipes(cls, user_id):
        query = """
            SELECT *
            FROM users
            LEFT JOIN recipes
            ON recipes.users_id = users.id
            WHERE users.id = %(id)s
        ;"""
        data = {"id" : user_id}
        results = connectToMySQL('recipes_schema').query_db(query, data)
        user = cls(results[0])
        if results[0]["description"]:
            for row_from_db in results:
                recipe_data = {
                    "id" : row_from_db["recipes.id"],
                    "name" : row_from_db["name"],
                    "description" : row_from_db["description"],
                    "under" : row_from_db["under"],
                    "instructions" : row_from_db["instructions"],
                    "date_made" : row_from_db["date_made"],
                    "created_at" : row_from_db["recipes.created_at"],
                    "updated_at" : row_from_db["recipes.updated_at"],
                    "users_id" : row_from_db["users_id"]
                }
            user.recipes.append(recipe.Recipe(recipe_data))
        return cls(results[0])
    
    # VALIDATIONS

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user["fname"]) < 2:
            is_valid = False
            flash("First name too short!", "registration")
        if len(user["lname"]) < 2:
            is_valid = False
            flash("Last name too short!" , "registration")
        if not user["email"]:
            is_valid = False
            flash("Please submit an email!" , "registration")
        else:
            EMAIL_REGEX = re.compile(r"^[a-zA-z0-9.+_-]+@[a-zA-z0-9.-]+\.[a-zA-z]+$")
            if not EMAIL_REGEX.match(user["email"]):
                is_valid = False
                flash("Invalid email!" , "registration")
            else:
                if User.get_user_by_email(user["email"]):
                    is_valid = False
                    flash("Duplicate email!", "registration")
        if not user["pword"]:
            is_valid = False
            flash("Please choose a password!", "registration")
        else:
            if len(user["pword"]) < 8:
                is_valid = False
                flash("Password not long enough!", "registration")
            else:
                if user['pword'] != user['confirm']:
                    is_valid = False
                    flash("Passwords don't match", "registration")
                if user["pword"].islower():
                    is_valid = False
                    flash("Password must contain an uppercase letter", "registration")
                if not [char for char in user["pword"] if char.isdigit()]:
                    is_valid = False
                    flash("Password must contain a number", "registration")
        return is_valid
    
    # LOGIN

    @staticmethod
    def login(data):
        user_in_db = User.get_user_by_email(data)
        if not user_in_db:
            flash("Incorrect email/password!", "login")
            return redirect("/")
        if not bcrypt.check_password_hash(user_in_db.password, data["password"]):
            flash("Incorrect email/password!", "login")
            return redirect("/")
        return user_in_db.id