from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import comment

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.comments = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts;"
        results = connectToMySQL('walls_schema').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def get_all_date_sorted(cls):
        query = "SELECT * FROM posts ORDER BY created_at DESC;"
        results = connectToMySQL('walls_schema').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        data = {"id" : id}
        results = connectToMySQL('walls_schema').query_db(query, data)
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts(content, created_at, updated_at, users_id) VALUES (%(content)s, NOW(), NOW(), %(user)s)"
        return connectToMySQL('walls_schema').query_db(query, data)

    @classmethod
    def get_post_comments_date_sorted(cls, id):
        query = "SELECT * from posts LEFT JOIN comments on comments.posts_id = posts.id WHERE posts.id = %(id)s ORDER BY comments.created_at;"
        data = {"id" : id}
        results = connectToMySQL('walls_schema').query_db(query, data)
        post = cls(results[0])

        for row_from_db in results:
            comment_data = {
                "id" : row_from_db["comments.id"],
                "content" : row_from_db["comments.content"],
                "created_at" : row_from_db["comments.created_at"],
                "updated_at" : row_from_db["comments.updated_at"],
                "posts_id" : row_from_db["posts_id"],
                "users_id" : row_from_db["comments.users_id"]
            }

            post.comments.append(comment.Comment(comment_data))
        
        return post.comments

    @staticmethod
    def validate_post(post):
        is_valid = True
        if not post["content"]:
            is_valid = False
            flash("Post content must not be blank")
        return is_valid
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM comments WHERE posts_id=%(id)s"
        connectToMySQL('walls_schema').query_db(query, data) # This first deletes all comments as foreign keys
        query = "DELETE FROM posts WHERE id=%(id)s"
        return connectToMySQL('walls_schema').query_db(query, data) # Now we can actually delete the post