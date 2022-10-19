from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models import user, product, category, order
from flask_app.config.mysqlconnection import connectToMySQL


@app.route('/place_order', methods=["POST"])
def create_order():
    total_price = session['cart_total']
    user_id = session['user_id']
    print('ORDER PLACED')


    # order_items = []
    # for item in session['cart']:
    #     order_items.append([item['name'], item['quantity'], item['price']])
    # print('testesss',order_items)

    

    data = {
        "total_price": total_price,
        "user_id": user_id
    }
    order.Order.save(data)

    order_id = order.Order.getOrderId()
    order_id = order_id.get('max(id)')
    for item in session['cart']:
        data = {
            "quantity": item['quantity'],
            "order_id": order_id,
            "product_id": item['id']
        }
        order.Order.saveDetails(data)



    session['cart_total'] = 0
    session['cart'] = []
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
    user_id = {
        'user_id':user_id
    }
    all_orders = []
    all_orders = order.Order.get_one_by_user(user_id)
    print("iyiyiyiy", all_orders)

    return render_template('view_orders.html', all_orders = all_orders)


@app.route('/view_order/<int:id>')
def view_order_details(id):

    data = {
        "id": id
    }
    order_details = order.Order.get_products_in_orders(data)
    # print(order_details)
    full_order = order.Order.get_one(data) 
    order_list = []
    for prod in order_details:
        product_id = prod.get('product_id')
        qty_of_product = prod.get('quantity')
        data = {
            "id": product_id
        }
        this_product = product.Product.get_one(data)
        print('THISISTEETE',this_product.name)
        order_list.append([this_product, qty_of_product])

    # Need to implement a way to only let users see their orders ((not typing in a random order number in url))

    print(order_list[1][0].name)

    return render_template('view_order_details.html', order_list = order_list, full_order = full_order )


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
