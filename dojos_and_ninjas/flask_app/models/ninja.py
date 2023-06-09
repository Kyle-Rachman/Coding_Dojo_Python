from flask_app.config.mysqlconnection import connectToMySQL

class Ninja:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.dojos_id = data['dojos_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_ninja(cls, data):
        query = "INSERT INTO ninjas(first_name, last_name, age, created_at, updated_at, dojos_id) VALUES (%(fname)s, %(lname)s, %(age)s, NOW(), NOW(), %(dojo)s)"
        return connectToMySQL('dojos_and_ninjas_schema').query_db(query, data)