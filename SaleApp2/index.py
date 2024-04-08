import math

from flask import render_template, request, redirect
from flask_login import login_user
import dao
from admin import admin
from __init__ import app, login


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
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        if username.__eq__('admin') and password.__eq__('123'):
            return redirect('/')
    return render_template('login.html')


@app.route('/admin-login', methods=['post'])
def process_admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)
    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
