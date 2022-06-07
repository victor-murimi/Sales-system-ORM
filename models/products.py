from enum import unique
from sqlalchemy.orm import backref
from sqlalchemy.sql.expression import true
from main import db
from models.sales import Sales
from models.stock import Stocks

class Products(db.Model):
    __tablename__='products'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(80),unique=True,nullable=False)
    buying_price=db.Column(db.Integer,nullable=False)
    Selling_price=db.Column(db.Integer,nullable=False)
    product_quantity=db.Column(db.Integer,nullable=False)

    rel=db.relationship(Sales , backref='products') 
    rel=db.relationship(Stocks ,backref='products')