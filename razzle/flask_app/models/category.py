from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import product, user
from flask import flash
from pprint import pprint

class Category:
    def __init__( self , data ):
        self.id = data['id']
        self.category = data['category']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.categorizations = []
        self.this_categorization = data['this_categorization']


    @classmethod
    def get_products_in_categories( cls ):
        query = "SELECT * FROM categories JOIN categorizations ON categories.id = categorizations.categories_id JOIN products ON products.id = categorizations.products_id ORDER by categories_id; "
        results = connectToMySQL('razz').query_db( query )
        
        categorizations = []
        for row_from_db in results:
            
            product_data = {
                "id" : row_from_db["products.id"],
                "name" : row_from_db["name"],
                "description" : row_from_db["description"],
                "price" : row_from_db["price"],
                "quantity" : row_from_db["quantity"],
                "image_url" : row_from_db["image_url"],
                "created_at" : row_from_db["products.created_at"],
                "updated_at" : row_from_db["products.updated_at"]
            }
            new_categorization = product.Product(product_data)
            category_data = {
                "id": row_from_db['id'],
                "category": row_from_db['category'],
                "created_at" : row_from_db['created_at'],
                "updated_at" : row_from_db['updated_at'],
                "this_categorization": new_categorization
            }
            categorizations.append( cls( category_data ) )
        return categorizations
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO categories (category) VALUES (%(category)s);"
        return connectToMySQL('razz').query_db(query,data)

    @classmethod
    def update(cls, data):
        query = "UPDATE categories SET category = %(category)s WHERE id = %(id)s;"
        return connectToMySQL('razz').query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM categories;"
        results = connectToMySQL('razz').query_db(query)
        print('TEWASSS', results)
        # Create an empty list to append our instances of categories
        categories = []
        # Iterate over the db results and create instances of categories with cls.
        for category in results:
            category['this_categorization'] = None
            categories.append( cls(category) )
        pprint(categories)
        return categories

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM categories WHERE id = %(id)s;"
        results = connectToMySQL('razz').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0]) 

    @classmethod
    def delete(cls, id):
        query  = f"DELETE FROM categories WHERE id = {id};"
        return connectToMySQL('razz').query_db(query)

    @staticmethod
    def validate_category( category ):
        is_valid = True
        # test whether a field matches the pattern
        if len(category['category']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        return is_valid

    @classmethod
    def make_categorization(cls, data):
        query = "INSERT INTO categorizations (products_id,categories_id) VALUES (%(product_id)s,%(category_id)s);"
        return connectToMySQL('razz').query_db(query, data)
    
