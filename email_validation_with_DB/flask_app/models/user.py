from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users_schema').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {'id': id}
        results = connectToMySQL('users_schema').query_db(query, data)
        user = cls(results[0])
        return user
    
    @classmethod
    def get_last(cls):
        query = "SELECT * FROM users ORDER BY id DESC LIMIT 1;"
        results = connectToMySQL('users_schema').query_db(query)
        user = cls(results[0])
        return user
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, created_at, updated_at) VALUES (%(fname)s,%(lname)s, %(email)s, NOW(), NOW());"
        return connectToMySQL('users_schema').query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(fname)s, last_name = %(lname)s, email = %(email)s, updated_at = %(updated_at)s WHERE id = %(id)s;"
        return connectToMySQL('users_schema').query_db(query, data)
    
    @classmethod
    def destroy(cls, id):
        query = "DELETE FROM users WHERE id = %(id)s;"
        data = {'id': id}
        return connectToMySQL('users_schema').query_db(query, data)
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user["first_name"]) < 1:
            is_valid = False
            flash("First name is required!")
        if len(user["last_name"]) < 1:
            is_valid = False
            flash("Last name is required!")
        if len(user["email"]) < 1:
            is_valid = False
            flash("Email is required!")
        else:
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(user["email"]):
                is_valid = False
                flash("Invalid email address!")
            query = "SELECT email FROM users;"
            results = connectToMySQL('users_schema').query_db(query)
            emails = []
            for address in results:
                emails.append(address["email"])
            print(emails)
            if user["email"] in emails:
                is_valid = False
                flash("Duplicate email address!")

        return is_valid