from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash

class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts_id = data['posts_id']
        self.users_id = data['users_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO comments(content, created_at, updated_at, posts_id, users_id) VALUES (%(content)s, NOW(), NOW(), %(post)s, %(user)s)"
        return connectToMySQL('walls_schema').query_db(query, data)
    
    @staticmethod
    def validate_comment(comment):
        is_valid = True
        if not comment["content"]:
            is_valid = False
            flash("Comment content must not be blank")
        return is_valid
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM comments WHERE id=%(id)s"
        connectToMySQL('walls_schema').query_db(query, data)
        return connectToMySQL('walls_schema').query_db(query, data)