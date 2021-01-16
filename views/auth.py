from flask.views import View
from flask import render_template, redirect, url_for, flash, request, g
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, LoginManager, login_required, logout_user
from forms import RegisterForm, LoginForm
from model import db, User


login_manager = LoginManager()

# def admin_only(function):
#     @wraps(function)
#     def wrapper_function(*args, **kwargs):
#         if g.user.id == 1:
#             return function(*args, **kwargs)
#         else:
#             abort(403, description="Only admin users can access this route.")
#     return wrapper_function


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Register(View):
    # decorators = [login_required]
    methods = ['GET', 'POST']

    def dispatch_request(self):
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
                    return redirect(
                        url_for("login", form=LoginForm(), error="There is already an email registered with "
                                                                 "this account, please log in!"))
                else:
                    login_user(user)
                    flash(f"You have been registered successfully! Welcome {g.user.name}")
                    return redirect(url_for('home'))
            else:
                return render_template("register.html", form=form)
        return render_template("register.html", form=form)


class Login(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
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
                    flash(f"You have been logged in successfully! Welcome back {g.user.name}")
                    return redirect(url_for("home"))
            else:
                return render_template("login.html", form=form)
        return render_template("login.html", form=form)


class Logout(View):
    def dispatch_request(self):
        logout_user()
        flash(f"You have been logged out successfully!")
        return redirect(url_for('home'))