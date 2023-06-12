from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Order:
    def __init__(self, data):
        self.id = data['id']
        self.customer_name = data['customer_name']
        self.type = data['type']
        self.number = data['number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders;"
        results = connectToMySQL('cookieorders_schema').query_db(query)
        orders = []
        for order in results:
            orders.append(cls(order))
        return orders

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM orders WHERE id = %(id)s;"
        data = {"id" : id}
        results = connectToMySQL('cookieorders_schema').query_db(query, data)
        order = cls(results[0])
        return order

    @classmethod
    def save(cls, data):
        query = "INSERT INTO orders(customer_name, type, number, created_at, updated_at) VALUES (%(name)s, %(type)s, %(number)s, NOW(), NOW())"
        return connectToMySQL('cookieorders_schema').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE orders SET customer_name = %(name)s, type = %(type)s, number = %(number)s WHERE id = %(id)s"
        return connectToMySQL('cookieorders_schema').query_db(query, data)

    @staticmethod
    def validate_order(order):
        is_valid = True
        if not order["name"] or not order["type"] or not order["number"]:
            is_valid = False
            flash("All fields required")
        else:
            if len(order["name"]) < 2:
                is_valid = False
                flash("Name must be at least two characters")
            if len(order["type"]) < 2:
                is_valid = False
                flash("Cookie type must be at least two characters")
            if int(order["number"]) <= 0:
                is_valid = False
                flash("Please enter a valid number of boxes")
        return is_valid