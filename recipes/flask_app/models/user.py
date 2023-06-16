from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
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

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('recipes_schema').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {"id" : id}
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(email)s, %(pword)s, NOW(), NOW())"
        return connectToMySQL('recipes_schema').query_db(query, data)

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
                accounts = User.get_all()
                account_emails = []
                for account in accounts:
                    account_emails.append(account.email)
                if user["email"] in account_emails:
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
                if user["pword"] != user["confirm"]:
                    is_valid = False
                    flash("Passwords don't match", "registration")
                if user["pword"].islower():
                    is_valid = False
                    flash("Password must contain an uppercase letter", "registration")
                if not any(char.isdigit() for char in user["pword"]):
                    is_valid = False
                    flash("Password must contain a number", "registration")

        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_user_recipes(cls, id):
        query = "SELECT * from users LEFT JOIN recipes on recipes.users_id = users.id WHERE users.id = %(id)s=;"
        data = {"id" : id}
        results = connectToMySQL('recipes_schema').query_db(query, data)
        post = cls(results[0])

        for row_from_db in results:
            recipe_data = {
                "id" : row_from_db["recipes.id"],
                "name" : row_from_db["recipes.name"],
                "description" : row_from_db["recipes.description"],
                "under" : row_from_db["recipes.under"],
                "instructions" : row_from_db["recipes.instructions"],
                "date_made" : row_from_db["recipes.date_made"],
                "created_at" : row_from_db["recipes.created_at"],
                "updated_at" : row_from_db["recipes.updated_at"],
                "users_id" : row_from_db["recipes.users_id"]
            }

            post.recipes.append(recipe.Recipe(recipe_data))
        
        return post.recipes