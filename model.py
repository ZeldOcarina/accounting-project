from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    line_items = relationship("LineItem", backref="users")


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
    line_items = relationship("LineItem", backref="customers")


class Vendor(db.Model):
    __tablename__ = "vendors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    address = db.Column(db.String(500))
    email = db.Column(db.String(500))
    zip_code = db.Column(db.Integer())
    iva_code = db.Column(db.String(200))
    phone_number = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime, default=date.today())
    line_items = relationship("LineItem", backref="vendors")


class LineItem(db.Model):
    __tablename__ = "line_items"
    id = db.Column(db.Integer, primary_key=True)
    line_date = db.Column(db.Date)
    kind = db.Column(db.String)
    item = db.Column(db.String(300), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    amount = db.Column(db.Float)
    file = db.Column(db.String(300))
    paid = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendors.id"))