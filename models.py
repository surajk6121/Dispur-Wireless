# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    address = db.Column(db.String(1000))
    contact = db.Column(db.String(100))
    is_activated = db.Column(db.Integer, default=0)
    role_id = db.Column(db.String(100))

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(100))
    tariff = db.Column(db.String(100))
    validity = db.Column(db.String(100))
    rental = db.Column(db.String(100))

class Subscribers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Plan_ID = db.Column(db.Integer)
    U_ID = db.Column(db.Integer)
    Amount_Payable = db.Column(db.Integer)
    Date_Of_Call = db.Column(db.String(100))
    Call_Duration = db.Column(db.String(100))
    Subscription_date = db.Column(db.String(100))