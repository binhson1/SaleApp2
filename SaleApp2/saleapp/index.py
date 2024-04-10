import math

from flask import render_template, request, redirect, session, jsonify
from flask_login import login_user, logout_user, current_user
from admin import admin
from __init__ import app, login
import dao, utils
import cloudinary.uploader
from decorator import loggedin


@app.route('/')
def index():
    q = request.args.get("q")
    cate_id = request.args.get("category_id")
    page = request.args.get('page')
    products = dao.load_products(q, cate_id=cate_id, page=page)
    counter = dao.count_product()
    return render_template('index.html', products=products,
                           pages=math.ceil(counter / app.config['PAGE_SIZE']))
    # return "Hi"


@app.route('/products/<int:id>')
def details(id):
    product = dao.get_product_by_id(product_id=id)
    return render_template('product-details.html', product=product)


@app.context_processor
def common_attributes():
    return {
        'categories': dao.load_categories()

    }


@app.route('/login', methods=['get', 'post'])
@loggedin
def login_my_user():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        u = dao.auth_user(username=username, password=password)
        if u:
            login_user(user=u)
            return redirect('/')
        else:
            err_msg = 'Username hoac password khong dung'
    return render_template('login.html', err_msg=err_msg)


@app.route('/logout', methods=['get'])
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.route('/admin-login', methods=['post'])
def process_admin_login():
    err_msg = ''
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)  # trang thai dang nhap session
    else:
        err_msg = 'Sai tai khoan hoac mat khau'
    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/api/carts', methods=['post'])
def add_to_cart():
    cart = session.get('cart')
    if not cart:
        cart = {}

    id = str(request.json.get('id'))
    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "id": id,
            "name": request.json.get('name'),
            "price": request.json.get('price'),
            "quantity": 1
        }
    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/register', methods=['post', 'get'])
@loggedin
def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            avatar_path = None
            avatar = request.files.get('avatar')
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']
            else:
                err_msg = 'Hệ thống đang lỗi'
            dao.register(name=request.form.get('name'),
                         username=request.form.get('username'),
                         password=password,
                         avatar=avatar_path)

            return redirect('/login')
        else:
            err_msg = "Mật khẩu không khớp"
    return render_template('register.html', err_msg=err_msg)


if __name__ == '__main__':
    app.run(debug=True)
