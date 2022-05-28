from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models import user, product, category, order


@app.route('/place_order', methods=["POST"])
def create_order():
    total_price = session['cart_total']
    user_id = session['user_id']
    print('ORDER PLACED')
    data = {
        "total_price": total_price,
        "user_id": user_id
    }
    order.Order.save(data)

    # name = {
    #     "name": request.form['name']
    # }
    # order_id = order.Order.get_one_byName(name).id
    # category_id = request.form['category']
    # order_with_category = {
    #     'order_id': order_id,
    #     'category_id': category_id
    # }



    return redirect('/dashboard')

@app.route('/my_orders')
def view_my_orders():
    user_id = session['user_id']
    all_orders = order.Order.get_one_by_user(user_id)

    return render_template('view_orders.html', all_orders = all_orders)


# @app.route('/add_order')
# def show_oder_page():

#     if 'admin' not in session:
#         flash("Must be logged in as admin!!")
#         return redirect('/dashboard')
#     else:
#         all_categories = category.Category.get_all()
#         all_orders = order.Order.get_all()
#         return render_template('add_order.html', all_orders=all_orders, all_categories=all_categories)


# @app.route('/edit_order', methods=["POST"])
# def edit_order():

#     if not order.Order.validate_order(request.form):
#         return redirect(request.referrer)
#     data = {

#         "name": request.form['name'],
#         "description": request.form['description'],
#         "price": request.form['price'],
#         "quantity": request.form['quantity'],
#         "image_url": request.form['image_url'],
#         "id": request.form['id']
#     }

#     order.Order.update(data)
#     return redirect('/dashboard')


# @app.route('/<int:id>')
# def show_order(id):
#     if 'user_id' not in session:
#         flash('Not logged in!')
#         return render_template('/index.html')
#     data = {
#         "id": id
#     }
#     print(order.Order.get_one(data).image_url)
#     return render_template('view_order.html', order=order.Order.get_one(data))


# @app.route('/order/edit/<int:id>')
# def show_edit_order(id):
#     if 'user_id' not in session:
#         flash('Not logged in!')
#         return render_template('/index.html')
#     data = {
#         "id": id
#     }
#     return render_template('edit_order.html', order=order.Order.get_one(data), all_categories=category.Category.get_all())


# @app.route('/delete/<int:id>')
# def delete_order(id):
#     order.Order.delete(id)
#     return redirect('/dashboard')
