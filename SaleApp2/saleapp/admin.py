from flask_admin import Admin, expose
from __init__ import app, db
from flask_admin.contrib.sqla import ModelView
from models import Category, Product, UserRole
from flask_admin import BaseView
from flask_login import logout_user, current_user
from flask import redirect


class MyAuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class MyProductView(MyAuthenticatedView):
    column_list = ['id', 'name', 'category_id']
    column_searchable_list = ['id', 'name']
    column_filters = ['id', 'name', 'price']
    can_export = True
    column_labels = {
        'name': 'Tên sản phẩm',
        'category_id': 'Danh mục sản phẩm'
    }


class MyCategoryView(MyAuthenticatedView):
    column_list = ['id', 'name', 'products']


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')

    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app, name='Quản trị trang web bán hàng', template_mode='bootstrap4')
admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))
