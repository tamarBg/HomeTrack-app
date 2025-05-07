from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(120), nullable=False,unique=True)
    password = db.Column(db.String(120), nullable=False)
    purchases = db.relationship('Purchase', backref='user', lazy=True)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date =  db.Column(db.Date, nullable=True, default=datetime.now)