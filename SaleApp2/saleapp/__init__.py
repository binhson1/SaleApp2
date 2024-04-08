from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
# from flask_babelex import Babel

app = Flask(__name__)
app.secret_key = '(*&()^(^(*^'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/saledb?charset=utf8mb4" % quote(
    'Sonhaian123.')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 2

cloudinary.config(cloud_name='dy2dgfaiq', api_key='376561342321139', api_secret='fuf5FQ4BVaHNwBCyP74b4b-uS_g')

db = SQLAlchemy(app)
login = LoginManager(app)

# babel = Babel(app=app)
#
# @babel.localeselector
# def load_locale():
#     return 'vi'
