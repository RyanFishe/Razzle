from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
from pprint import pprint

class Product:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.price = data['price']
        self.quantity = data['quantity']
        self.image_url = data['image_url']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls, data):
        query = "INSERT INTO products (name ,description, artist, price, quantity, image_url) VALUES (%(name)s,%(description)s,%(artist)s,%(price)s,%(quantity)s,%(image_url)s);"
        return connectToMySQL('razz').query_db(query,data)

    @classmethod
    def update(cls, data):
        query = "UPDATE products SET name = %(name)s, description = %(description)s, price = %(price)s, quantity = %(quantity)s,image_url = %(image_url)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('razz').query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM products;"
        results = connectToMySQL('razz').query_db(query)
        # Create an empty list to append our instances of products
        products = []
        # Iterate over the db results and create instances of products with cls.
        for product in results:
            products.append( cls(product) )
        return products

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM products WHERE id = %(id)s;"
        results = connectToMySQL('razz').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0]) 

    @classmethod
    def delete(cls, id):
        query  = f"DELETE FROM products WHERE id = {id};"
        return connectToMySQL('razz').query_db(query)

    @staticmethod
    def validate_product( product ):
        is_valid = True
        # test whether a field matches the pattern
        if len(product['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(product['description']) < 10:
            flash("Description must be at least 10 characters.")
            is_valid = False
        if int(product['price']) < 1:
            flash("Price must be more than $0.")
            is_valid = False


        return is_valid
    
