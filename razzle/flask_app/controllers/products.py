from math import prod
from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models import user, product, category


@app.route('/product/create', methods=["POST"])
def create_product():
    option = request.form.get('quantity')
    if not product.Product.validate_product(request.form):
        return redirect('/product/add')

    data = {
        "name":request.form['name'],
        "description": request.form['description'],
        "price":request.form['price'],
        "quantity": request.form['quantity'],
        "image_url": request.form['image_url']
    }
    product.Product.save(data)

    name = {
            "name": request.form['name']
        }
    product_id = product.Product.get_one_byName(name).id
    category_id = request.form['category']
    product_with_category = {
        'product_id':product_id,
        'category_id':category_id
    }

    category.Category.make_categorization(product_with_category)

    return redirect('/dashboard');

@app.route('/add_product')
def show_add_page():


    if  'admin' not in session:
        flash("Must be logged in as admin!!")
        return redirect('/dashboard')
    else:        
        all_categories = category.Category.get_all()
        all_products = product.Product.get_all()
        return render_template('add_product.html', all_products=all_products, all_categories=all_categories)


@app.route('/edit_product', methods=["POST"])
def edit_product():
    
    if not product.Product.validate_product(request.form):
        return redirect(request.referrer)
    data = {
        
        "name":request.form['name'],
        "description": request.form['description'],
        "price":request.form['price'],
        "quantity": request.form['quantity'],
        "image_url": request.form['image_url'],
        "id":request.form['product_id']
    }
    product.Product.update(data)


    # Trying to sort which categories are checked/unchecked so they can be added or deleted


    # product_id =  {
    #     'products_id':request.form['product_id']
    # }

    # all_prod_cats = []
    # all_prod_cats = product.Product.get_all_cat_for_product(product_id)
    # print('product cat data aaaaaaaaaa', all_prod_cats)

    cat_data = []
    checked_cat = (request.form.getlist('category_id'))
    print("THIS DATA &%&%&%&%&", checked_cat)
    for i in checked_cat:
        cat_data.append({
        'product_id': request.form['product_id'],
        "category_id":i
    })
    print("NEW DATAAAAAA", cat_data)
    
    for new_cat in cat_data:
        category.Category.make_categorization(new_cat)

    
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
    return render_template('edit_product.html', product=product.Product.get_one(data), all_categories=category.Category.get_all())


@app.route('/delete/<int:id>')
def delete_product(id):
    product.Product.delete(id)
    return redirect('/dashboard')
