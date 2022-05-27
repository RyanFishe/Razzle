from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models import user, category, category


@app.route('/category/create', methods=["POST"])
def create_category():
    option = request.form.get('quantity')
    if not category.Category.validate_category(request.form):
        return redirect('/category/add')

    data = {
        "name":request.form['name'],
        "artist": session['full_name'],
        "description": request.form['description'],
        "price":request.form['price'],
        "quantity": request.form['quantity'],
        "user_id": request.form['user_id']
    }

    category.Category.save(data)
    return redirect('/dashboard');

@app.route('/category/add')
def show_add_category_page():
    return render_template('add_category.html')

@app.route('/categories')
def show_categories():
   
    products_with_categories = category.Category.get_products_in_categories()
    all_categories = category.Category.get_all()
    return render_template('categories.html', all_categories = all_categories, products_with_categories=products_with_categories)


        

@app.route('/edit_category', methods=["POST"])
def edit_category():
    # Checks if the cook time was inputted

    if not category.Category.validate_category(request.form):
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

    category.Category.update(data)
    return redirect('/dashboard');

@app.route('/category/<int:id>')
def show_single_category(id):
    if 'user_id' not in session:
        flash('Not logged in!')
        return render_template('/index.html')
    data = {
        "id": id
    }
    return render_template('view_category.html', category=category.Category.get_one(data))

@app.route('/category/edit/<int:id>')
def show_edit_category(id):
    if 'user_id' not in session:
        flash('Not logged in!')
        return render_template('/index.html')
    data = {
        "id": id
    }
    return render_template('edit_category.html', category=category.Category.get_one(data))


@app.route('/delete/<int:id>')
def delete_category(id):
    category.Category.delete(id)
    return redirect('/dashboard')
