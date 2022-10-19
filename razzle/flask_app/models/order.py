from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, order, product
from flask import flash
from pprint import pprint


class Order:
    def __init__(self, data):
        self.id = data['id']
        self.total_price = data['total_price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO orders (total_price ,user_id) VALUES (%(total_price)s,%(user_id)s);"
        return connectToMySQL('razz').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE orders SET total_price = %(total_price)s, updated_at = NOW(), user_id = %(user_id)s WHERE id = %(id)s;"
        return connectToMySQL('razz').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders;"
        results = connectToMySQL('razz').query_db(query)
        # Create an empty list to append our instances of orders
        orders = []
        # Iterate over the db results and create instances of orders with cls.
        for order in results:
            orders.append(cls(order))
        return orders

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM orders WHERE id = %(id)s;"
        results = connectToMySQL('razz').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one_by_user(cls, data):
        query = "SELECT * FROM orders WHERE user_id = %(user_id)s;"
        results = connectToMySQL('razz').query_db(query, data)
        if (results) == False:
            return ("No Orders")
        orders = []
        # Iterate over the db results and create instances of orders with cls.
        for order in results:
            orders.append(cls(order))
        return orders

    @classmethod
    def getOrderId(cls):
        query = "SELECT max(id) from orders;"
        results = connectToMySQL('razz').query_db(query)
        if len(results) < 1:
            return False
        return (results[0])

    @classmethod
    def saveDetails(cls, data):
        query = "INSERT INTO order_details (quantity, order_id, product_id) VALUES (%(quantity)s,%(order_id)s,%(product_id)s);"
        return connectToMySQL('razz').query_db(query, data)

    @classmethod
    def get_products_in_orders(cls, data):
        query = "SELECT product_id, quantity from order_details where order_id = %(id)s;"
        results = connectToMySQL('razz').query_db(query, data)
        return results
    


    @classmethod
    def delete(cls, id):
        query = f"DELETE FROM orders WHERE id = {id};"
        return connectToMySQL('razz').query_db(query)



    # @staticmethod
    # def validate_Order(Order):
    #     is_valid = True
    #     # test whether a field matches the pattern
    #     if len(Order['total_price']) < 3:
    #         flash("total_price must be at least 3 characters.")
    #         is_valid = False
    #     if len(Order['user_id']) < 10:
    #         flash("user_id must be at least 10 characters.")
    #         is_valid = False
    #     if float(Order['price']) < 1:
    #         flash("Price must be more than $0.")
    #         is_valid = False
    #     if int(Order['quantity']) < 0:
    #         flash("Must Have quantity")
    #         is_valid = False

    #     return is_valid
