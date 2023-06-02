# from unicodedata import category
from hashlib import new
from pprint import pprint
from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models import user, category, product, order
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
        session['cart'] = []
        session['cart_total'] = 0
        session['product_cart_quantity'] = 0

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
        session['cart'] = []
        session['cart_total'] = 0
        session['product_cart_quantity'] = 0

        print(session['full_name'])

        if user_in_db.admin == True:
            session['admin'] =  True
        else:
            session['admin'] = False
        
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
    
    userIn =  user.User.get_one(data)
    if userIn.admin != None:
        print("ADMIN JUST IN")
        session['admin'] = True
    all_products = product.Product.get_all()

    
    return render_template("dashboard.html", all_products = all_products, userIn = userIn )

@app.route("/view_cart")
def show_cart():
    return render_template("cart.html")


@app.route('/add_cart', methods=['POST'])
def add_cart_item():
    cart = session['cart']


    cart_item_id = request.form['product_id']
    print(request.form['product_id'])
    cart_item_object = {
        "id": cart_item_id
    }

    cart_item_object = product.Product.get_one(cart_item_object)
    cart_item_object = {
        "name": cart_item_object.name,
        "description": cart_item_object.description,
        "price": cart_item_object.price,
        "quantity": 0,
        "image_url": cart_item_object.image_url,
        "id": cart_item_object.id
    }
# This section will check if same item is in cart, and will adjust the quantity instead of adding a "new" item.
    if(session['cart']):
        print(cart_item_object['name'])
        if next((item for item in session['cart'] if item["name"] == cart_item_object['name']), False):
            for item in session['cart']:
                if cart_item_object['name'] == item['name']:
                    print('item in cart qty',item['quantity'])
                    old_quantity = item['quantity']
                    new_quantity = old_quantity + 1
                    item['quantity'] = new_quantity

        else:
            cart_item_object['quantity'] += 1
            cart.append(cart_item_object)
            session['cart'] = cart

# This section updates the cart's total appropriately.
        new_total = 0
        for item in session['cart']:
            quantity = int(item['quantity'])
            price = float(item['price'])
            this_price = round(float(price * quantity),4)
            new_total += float(this_price)
            session['cart_total'] = round(float(new_total), 4)

    else:
        
        session['cart_total'] = round(float(cart_item_object['price']), 4)
        cart_item_object['quantity'] = 1
        cart.append(cart_item_object)
        session['cart'] = cart

    return redirect('/view_cart')



def array_merge( first_array , second_array ):
    if isinstance( first_array , list ) and isinstance( second_array , list ):
        return first_array + second_array
    elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
        return dict( list( first_array.items() ) + list( second_array.items() ) )
    elif isinstance( first_array , set ) and isinstance( second_array , set ):
        return first_array.union( second_array )
    return False	


# @app.route('/add', methods=['POST'])
# def add_product_to_cart():
# 	cursor = None
# 	try:
# 		_quantity = int(request.form['quantity'])
# 		_code = request.form['code']
# 		if _quantity and _code and request.method == 'POST':
# 			conn = mysql.connect()
# 			cursor = conn.cursor(pymysql.cursors.DictCursor)
# 			cursor.execute("SELECT * FROM product WHERE code=%s", _code)
# 			row = cursor.fetchone()
# 			if float(row['quantity']) >= float(_quantity):
# 			    itemArray = {
#                 row['code']: 
#                 {'name': row['name'], 'code': row['code'], 'quantity': _quantity,
#                             'price': row['price'], 'image': row['image_url'], 'total_price': _quantity * row['price']}
#                 };
#                 all_total_price = 0;
#                 all_total_quantity = 0;
#                 session.modified = True;
# 			if 'cart_item' in session:
# 					if row['code'] in session['cart_item']:
# 						for key, value in session['cart_item'].items():
# 							if row['code'] == key:
# 								old_quantity = session['cart_item'][key]['quantity']
# 								total_quantity = old_quantity + _quantity
# 								session['cart_item'][key]['quantity'] = total_quantity
# 								session['cart_item'][key]['total_price'] = total_quantity * row['price']
# 					else:
# 						session['cart_item'] = array_merge(session['cart_item'], itemArray)
# 					for key, value in session['cart_item'].items():
# 						individual_quantity = int(session['cart_item'][key]['quantity'])
# 						individual_price = float(session['cart_item'][key]['total_price'])
# 						all_total_quantity = all_total_quantity + individual_quantity
# 						all_total_price = all_total_price + individual_price
# 				else:
# 					session['cart_item'] = itemArray
# 					all_total_quantity = all_total_quantity + _quantity
# 					all_total_price = all_total_price + _quantity * row['price']
# 				session['all_total_quantity'] = all_total_quantity
# 				session['all_total_price'] = all_total_price
# 				return redirect(url_for('.products'))
# 			else:
# 				cursor.execute("SELECT * FROM product")
# 				rows = cursor.fetchall()
# 				return render_template('index.html', products=rows, status='stock_error')
# 	except Exception as e:
# 		print(e)
# 	finally:
# 		cursor.close()
# 		conn.close()







    
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
