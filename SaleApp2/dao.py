import json
# from _ast import slice
from _tracemalloc import start
import hashlib
from models import Category, Product, User
from __init__ import app, login, db


def load_categories():
    return Category.query.all()
    # with open('data/categories.json', encoding='utf-8') as f:
    #     return json.load(f)


def count_product():
    return int(Product.query.count())


def load_products(q=None, cate_id=None, page=None):
    query = Product.query

    if q:
        query = query.filter(Product.name.contains(q))

    if cate_id:
        query = query.filter(Product.category_id.__eq__(cate_id))

    if page:
        page_size = app.config['PAGE_SIZE']
        start = (int(page) - 1) * page_size
        query = query.slice(start, start + page_size)
    return query.all()
    # with open('data/products.json', encoding='utf-8') as f:
    #     products = json.load(f)
    #
    #     if q:
    #         products = [p for p in products if p['name'].find(q) >= 0]
    #     if cate_id:
    #         products = [p for p in products if p['category_id'].__eq__(int(cate_id))]
    #
    #     return products
    #


def get_product_by_id(product_id):
    return Product.query.get(product_id)
    # with open('data/products.json', encoding='utf-8') as f:
    #     products = json.load(f)
    #     for p in products:
    #         if p['id'] == product_id:
    #             return p


def get_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(str(password).strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def register(name, username, password, avatar):
    password = str(hashlib.md5(str(password).strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()
