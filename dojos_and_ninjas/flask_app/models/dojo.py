from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import ninja

class Dojo:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query)
        dojos = []
        for dojo in results:
            dojos.append(cls(dojo))
        return dojos
    
    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM dojos WHERE id = %(id)s"
        data = {"id" : id}
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query, data)
        dojo = cls(results[0])
        return dojo
    
    @classmethod
    def save_dojo(cls, data):
        query = "INSERT INTO dojos(name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW())"
        return connectToMySQL('dojos_and_ninjas_schema').query_db(query, data)
    
    @classmethod
    def get_dojo_ninjas(cls, data):
        query = "SELECT * from dojos LEFT JOIN ninjas on ninjas.dojos_id = dojos.id WHERE dojos.id = %(id)s;"
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query, data)
        dojo = cls(results[0])

        for row_from_db in results:
            ninja_data = {
                "id" : row_from_db["ninjas.id"],
                "first_name" : row_from_db["first_name"],
                "last_name" : row_from_db["last_name"],
                "age" : row_from_db["age"],
                "created_at" : row_from_db["ninjas.created_at"],
                "updated_at" : row_from_db["ninjas.updated_at"],
                "dojos_id" : row_from_db["dojos_id"]
            }

            dojo.ninjas.append(ninja.Ninja(ninja_data))
        
        return dojo.ninjas
    
    @classmethod
    def edit_dojo_ninja(cls, data):
        query = "UPDATE dojos LEFT JOIN ninjas on ninjas.dojos_id = dojos.id SET first_name = %(fname)s, last_name = %(lname)s, age = %(age)s WHERE dojos.id = %(dojo)s AND ninjas.id = %(id)s;"
        return connectToMySQL('dojos_and_ninjas_schema').query_db(query, data)