from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, BooleanField, FileField
from wtforms.fields.html5 import EmailField, TelField, DateField
from wtforms.validators import DataRequired, Email, Optional


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Nome", validators=[DataRequired()])
    submit = SubmitField("Iscrivimi!")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in!")


class CreateCustomer(FlaskForm):
    name = StringField("Nome del Cliente", validators=[DataRequired()])
    phone_number = TelField("Numero di Telefono", validators=[Optional()])
    email = EmailField("Email", validators=[Optional(), Email()])
    address = StringField("Indirizzo", validators=[Optional()])
    zip_code = StringField("Codice CAP", validators=[Optional()])
    iva_code = StringField("Codice IVA/Partita IVA", validators=[Optional()])
    submit = SubmitField("Invia")


class CreateVendor(FlaskForm):
    name = StringField("Nome del Fornitore", validators=[DataRequired()])
    phone_number = TelField("Numero di Telefono", validators=[Optional()])
    email = EmailField("Email", validators=[Optional(), Email()])
    address = StringField("Indirizzo", validators=[Optional()])
    zip_code = StringField("Codice CAP", validators=[Optional()])
    iva_code = StringField("Codice IVA/Partita IVA", validators=[Optional()])
    submit = SubmitField("Invia")


class CreateLine(FlaskForm):
    line_date = DateField("Data", validators=[DataRequired()])
    kind = SelectField("Tipologia", choices=["Invoice", "Expense"], validators=[DataRequired()])
    item = StringField("Descrizione", validators=[DataRequired()])
    currency = SelectField("Valuta", choices=['CHF', 'EUR', 'USD'])
    amount = StringField("Ammontare", validators=[DataRequired()])
    paid = BooleanField("Pagata?")
    customer = SelectField("Cliente")
    vendor = SelectField("Fornitore")
    document = FileField("Fattura o ricevuta")
    submit = SubmitField("Invia")


