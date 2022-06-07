from main import db
from sqlalchemy.orm import backref
from sqlalchemy.sql import func

class Sales(db.Model):
    __tablename__='sales'

    id=db.Column(db.Integer,primary_key=True)
    product_id=db.Column(db.Integer,db.ForeignKey('products.id'))
    quantity=db.Column(db.Integer)
    created_at=db.Column(db.DateTime(timezone=True),server_default=func.now())