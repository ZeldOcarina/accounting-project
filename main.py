# from functools import wraps
from flask import Flask, render_template, redirect, url_for, flash, abort, g
from flask_bootstrap import Bootstrap
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import RegisterForm, LoginForm, CreateCustomer
from flask import request


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounting.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    lines = relationship("LineItem", back_populates="author")


class LineItem(db.Model):
    __tablename__ = "line_items"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    kind = db.Column(db.Enum(("income", "expense")))
    item = db.Column(db.String(300), nullable=False)
    amount = db.Column(db.Float)
    paid = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="lines")
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="payments")


class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    address = db.Column(db.String(500))
    email = db.Column(db.String(500))
    zip_code = db.Column(db.Integer())
    iva_code = db.Column(db.String(200))
    phone_number = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime, default=date.today())
    payments = relationship("LineItem", back_populates="customer")


# db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login"))


# def admin_only(function):
#     @wraps(function)
#     def wrapper_function(*args, **kwargs):
#         if g.user.id == 1:
#             return function(*args, **kwargs)
#         else:
#             abort(403, description="Only admin users can access this route.")
#     return wrapper_function


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            password = generate_password_hash(request.form.get("password"))
            user = User(
                name=request.form.get("name"),
                email=request.form.get("email"),
                password=password
            )
            try:
                db.session.add(user)
                db.session.commit()
            except IntegrityError:
                return redirect(url_for("login", form=LoginForm(), error="There is already an email registered with "
                                                                         "this account, please log in!"))
            else:
                login_user(user)
                return redirect(url_for('home'))
        else:
            return render_template("register.html", form=form)
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                found_user = User.query.filter_by(email=request.form.get("email")).first()
                user = load_user(found_user.id)
                is_password_right = check_password_hash(user.password, request.form.get("password"))
                if not is_password_right:
                    error = "Wrong password, please try again."
                    return render_template("login.html", form=form, error=error), 403
                else:
                    login_user(found_user)
            except AttributeError:
                error = "The email you've tried to login with does not exist in the database"
                return render_template("login.html", error=error, form=form), 404
            else:
                return redirect(url_for("home", name=user.name))
        else:
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/customers', methods=['GET', 'POST'])
def customers():
    form = CreateCustomer()
    if request.method == 'POST':
        print(request.form)
        if form.validate_on_submit():
            customer = Customer(
                name=request.form.get("name"),
                address=request.form.get("address"),
                email=request.form.get("email"),
                zip_code=request.form.get("zip_code"),
                iva_code=request.form.get("iva_code"),
                phone_number=request.form.get("phone_number"),
            )
            db.session.add(customer)
            db.session.commit()
        return redirect('/')
    return render_template('new_customer.html', form=form)


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)