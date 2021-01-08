from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import DataRequired, URL, Email
import email_validator


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign me up!")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in!")


class CreateCustomer(FlaskForm):
    name = StringField("Customer Name", validators=[DataRequired()])
    phone_number = TelField("Phone Number", validators=[])
    email = EmailField("Email", validators=[Email()])
    address = StringField("Address")
    zip_code = StringField("ZIP Code")
    iva_code = StringField("IVA Code")
    submit = SubmitField("Create the Customer!")
