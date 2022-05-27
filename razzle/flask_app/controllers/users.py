# from unicodedata import category
from pprint import pprint

from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models import user, category, product
# from flask_app.models import Message
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)



@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register',methods=['POST'])
def create_account():
        data = { "email" : request.form["email"] }
        if request.form['password'] != request.form['confirm']:
            flash("Passwords don't match!")
            return redirect('/')

        if not user.User.validate_register(request.form):
            return redirect('/')

            #hashes the requested password if the form is validated 
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        # put the pw_hash into the data dictionary
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password" : pw_hash
        }
        # Call the save @classmethod on User
        session['user_id'] = user.User.save(data)
        session['user_name'] = request.form['first_name']
        session['full_name'] = request.form['first_name'] + ' ' + request.form['last_name']

        # store user id into session
        return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def process_login(): 
            # see if the username provided exists in the database
        data = { "email" : request.form["email"] }
        user_in_db = user.User.get_by_email(data)
        # user is not registered in the db
        if not user_in_db:
            flash("Invalid Email/Password")
            return redirect("/")
        if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            # if we get False after checking the password
            flash("Invalid Email/Password")
            return redirect('/')
        # if the passwords matched, we set the user_id into session
        session['user_id'] = user_in_db.id
        session['user_name'] = user_in_db.first_name
        session['full_name'] = user_in_db.first_name + ' ' + user_in_db.last_name
        print(session['full_name'])
        # never render on a post!!!
        return redirect("/dashboard")

@app.route('/dashboard')
def show_dashboard():  
    if 'user_id' not in session:
        flash('Not logged in!')
        return render_template('/index.html')
    data = { 
        "id": session['user_id'] 
        }
    
    # user =  user.User.get_one(data)
    # all_users = user.User.get_all()
    all_products = product.Product.get_all()

    # pprint(purchases[0].this_purchase)
    
    return render_template("dashboard.html", all_products = all_products )
    # return render_template("/dashboard.html")
@app.route("/view_cart")
def show_cart():
    return render_template("cart.html")
    
@app.route('/join/product',methods=['POST'])
def join_product():
    new_quantity = int(request.form['quantity']) - 1
    data = {
        'user_id': request.form['user_id'],
        'product_id': request.form['product_id'],
        'quantity': new_quantity
    }
    user.User.update_quantity(data)
    user.User.make_purchase(data)
    return redirect("/dashboard ")

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')
