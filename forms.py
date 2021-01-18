from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, BooleanField, FileField
from wtforms.fields.html5 import EmailField, TelField, DateField
from wtforms.validators import DataRequired, Email, Optional


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
    phone_number = TelField("Phone Number", validators=[Optional()])
    email = EmailField("Email", validators=[Optional(), Email()])
    address = StringField("Address", validators=[Optional()])
    zip_code = StringField("ZIP Code", validators=[Optional()])
    iva_code = StringField("IVA Code", validators=[Optional()])
    submit = SubmitField("Submit")


class CreateVendor(FlaskForm):
    name = StringField("Vendor Name", validators=[DataRequired()])
    phone_number = TelField("Phone Number", validators=[Optional()])
    email = EmailField("Email", validators=[Optional(), Email()])
    address = StringField("Address", validators=[Optional()])
    zip_code = StringField("ZIP Code", validators=[Optional()])
    iva_code = StringField("IVA Code", validators=[Optional()])
    submit = SubmitField("Submit")


class CreateLine(FlaskForm):
    line_date = DateField("Date", validators=[DataRequired()])
    kind = SelectField("Kind", choices=["Invoice", "Expense"], validators=[DataRequired()])
    item = StringField("Description", validators=[DataRequired()])
    currency = SelectField("Currency", choices=['CHF', 'EUR', 'USD'])
    amount = StringField("Amount", validators=[DataRequired()])
    paid = BooleanField("Paid?")
    customer = SelectField("Customer")
    vendor = SelectField("Vendor")
    document = FileField("Invoice or receipt")
    submit = SubmitField("Submit")


