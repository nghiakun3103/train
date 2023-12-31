import math
from flask import render_template, request, redirect, session, jsonify
import dao
import utils
from app import app, login
from flask_login import login_user


@app.route('/')
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')

    cates = dao.load_categories()
    products = dao.load_products(kw, cate_id, page)

    num = dao.count_product()

    return render_template('index.html', categories=cates, products=products,
                           pages=math.ceil(num/app.config['PAGE_SIZE']))


@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')

@app.route('/api/cart', methods=['post'])
def add_cart():
    """
    {
        "cart":{
            "1":{
                "id": 1,
                "name": "ABC",
                "price": 12,
                "quantity": 2
            }, "2":{
                "id": 2,
                "name": "ABC",
                "price": 12,
                "quantity": 2
            }
        }
    }
    :return:
    """
    cart = session.get('cart')
    if cart is None:
        cart = {}

    data = request.json
    id = str(data.get("id"))

    if id in cart: # san pham da co trong gio
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else: # san pham chua co trong gio
        cart[id] = {
                "id": id,
                "name": data.get("name"),
                "price": data.get("price"),
                "quantity": 1
            }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))

@app.route('/cart')
def cart_list():
    return render_template('cart.html')

@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
