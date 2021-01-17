import os
# from functools import wraps
import importlib
from flask import Flask, redirect, url_for, g
from flask_bootstrap import Bootstrap
from flask_login import current_user

from model import db, User
from views import Home

auth_spec = importlib.util.spec_from_file_location('auth', 'views/auth.py')
auth = importlib.util.module_from_spec(auth_spec)
auth_spec.loader.exec_module(auth)

customers_spec = importlib.util.spec_from_file_location('customers', 'views/customers.py')
customers = importlib.util.module_from_spec(customers_spec)
customers_spec.loader.exec_module(customers)

line_items_spec = importlib.util.spec_from_file_location('line_items', 'views/line_items.py')
line_items = importlib.util.module_from_spec(line_items_spec)
line_items_spec.loader.exec_module(line_items)

vendors_spec = importlib.util.spec_from_file_location('vendors', 'views/vendors.py')
vendors = importlib.util.module_from_spec(vendors_spec)
vendors_spec.loader.exec_module(vendors)

APP_SECRET = os.getenv("APP_SECRET")
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///accounting.db")

app = Flask(__name__)

app.config['SECRET_KEY'] = APP_SECRET
app.config['UPLOAD_FOLDER'] = 'static/uploads'
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# with app.app_context():
#     db.create_all()

auth.login_manager.init_app(app)


@app.login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login"))


@app.before_request
def before_request():
    g.user = current_user


# Home
app.add_url_rule('/', view_func=Home.as_view('home'))

# Auth
app.add_url_rule('/register', view_func=auth.Register.as_view('register'))
app.add_url_rule('/login', view_func=auth.Login.as_view('login'))
app.add_url_rule('/logout', view_func=auth.Logout.as_view('logout'))

# Customers
app.add_url_rule('/customers/new', view_func=customers.CreateCustomerView.as_view('create_customer'))
app.add_url_rule('/customers/list', view_func=customers.AllCustomers.as_view('all_customers'))
app.add_url_rule('/customers/<int:customer_id>', view_func=customers.SingleCustomer.as_view('single_customer'))

# Line Items
app.add_url_rule('/line-items/create', view_func=line_items.CreateLineItemView.as_view('new_line_item'))
app.add_url_rule('/line-items/<int:line_item_id>', view_func=line_items.EditLineView.as_view('edit_line_item'))

# Vendors
app.add_url_rule('/vendors/create', view_func=vendors.CreateVendorView.as_view('new_vendor'))

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
