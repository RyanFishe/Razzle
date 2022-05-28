from flask_app import app
from flask import session
from flask_app.controllers import products, users, categories, orders
app.secret_key = "Shhhh"
if __name__=="__main__":
    app.run(debug=True)