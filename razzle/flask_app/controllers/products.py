from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models import user, product


@app.route('/product/create', methods=["POST"])
def create_product():
    option = request.form.get('quantity')
    if not product.Product.validate_product(request.form):
        return redirect('/product/add')

    data = {
        "name":request.form['name'],
        "artist": session['full_name'],
        "description": request.form['description'],
        "price":request.form['price'],
        "quantity": request.form['quantity'],
        "user_id": request.form['user_id']
    }

    product.Product.save(data)
    return redirect('/dashboard');

@app.route('/add_product')
def show_add_page():
    return render_template('add_product.html')

# @app.route('/products/categories')
# def show_categories():
#     return render_template('categories.html')


        

@app.route('/edit_product', methods=["POST"])
def edit_product():
    # Checks if the cook time was inputted

    if not product.Product.validate_product(request.form):
        return redirect(request.referrer)
    data = {
        
        "name":request.form['name'],
        "artist": session['full_name'],
        "description": request.form['description'],
        "price":request.form['price'],
        "quantity": request.form['quantity'],
        "user_id": request.form['user_id'],
        "id":request.form['id']
    }

    product.Product.update(data)
    return redirect('/dashboard');

@app.route('/<int:id>')
def show_product(id):
    if 'user_id' not in session:
        flash('Not logged in!')
        return render_template('/index.html')
    data = {
        "id": id
    }
    print(product.Product.get_one(data).image_url)
    return render_template('view_product.html', product=product.Product.get_one(data))

@app.route('/product/edit/<int:id>')
def show_edit_product(id):
    if 'user_id' not in session:
        flash('Not logged in!')
        return render_template('/index.html')
    data = {
        "id": id
    }
    return render_template('edit_product.html', product=product.Product.get_one(data))


@app.route('/delete/<int:id>')
def delete_product(id):
    product.Product.delete(id)
    return redirect('/dashboard')
