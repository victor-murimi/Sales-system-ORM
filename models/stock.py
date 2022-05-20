from main import db
from sqlalchemy.orm import backref
from sqlalchemy.sql import func
class Stocks(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer,unique=True, primary_key=True)
    pid=db.Column(db.Integer,db.ForeignKey('products.id'))
    created_at=db.Column(db.DateTime(timezone=True),server_default=func.now(),nullable=False)
    stock_quantity = db.Column(db.Integer)
    
   