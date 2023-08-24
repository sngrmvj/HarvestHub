

from setup import db
from datetime import datetime

class Retailer(db.Model):
    __tablename__ = 'retailer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(400), nullable=False)
    phonenumber = db.Column(db.Integer(10), nullable=False)

    def check_password(self, password):
        return self.password == password

    def __repr__(self):
        return '<User %r>' % self.username
    

class Purchases(db.Model):
    __tablename__ = 'retailer_purchases'
    purchase_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    owner = db.Column(db.String(80), default="HarvestHub_Owner")
    retailer_email = db.Column(db.String(120), unique=True, nullable=False)
    retailer_address = db.Column(db.String(400), nullable=False)
    retailer_phonenumber = db.Column(db.Integer(10), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    commodity = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'User - {self.retailer_email}'