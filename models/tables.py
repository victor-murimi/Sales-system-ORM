from flask.scaffold import F
from sqlalchemy.orm import backref
from sqlalchemy.sql import func
from main import db
from ..main import db

class User(db.model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(80), unique=True, nullable=False)
    username=db.Column(db.String(80))
    password = db.Column(db.String(80))
    confirm_password = db.Column(db.String(120))
    
class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    pid=db.Column(db.Integer,db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer)
    created_at=db.Column(db.DateTime(timezone=True),server_default=func.now())

class Restocking_update(db.Model):
    __tablename__ = 'restocking_update'
    id = db.Column(db.Integer, primary_key=True)
    pid=db.Column(db.Integer,db.ForeignKey('stocks.pid'))
    stockchanged=db.Column(db.Integer)
    newstock=db.Column(db.Integer)
    change_time=db.Column(db.DateTime(timezone=True),server_default=func.now())





