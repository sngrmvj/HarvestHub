
from setup import db
from datetime import datetime
from sqlalchemy import PrimaryKeyConstraint

class Agent(db.Model):
    __tablename__ = 'agent'
    agent_id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def check_password(self, password):
        return self.password == password

    def __repr__(self):
        return '<User %r>' % self.username
    


class Farmer(db.Model):
    __tablename__ = 'farmer'
    farmer_id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(240), nullable=False)

    def check_password(self, password):
        return self.password == password

    def __repr__(self):
        return '<User %r>' % self.username
    
class Agent_Farmer(db.Model):
    __tablename__ = 'agent_farmer'
    agent_id = db.Column(db.String(10), nullable=False)
    farmer_id = db.Column(db.String(10), nullable=False)
    truck_id = db.Column(db.String(80), nullable=False)
    bag_id = db.Column(db.String(80), unique=True, nullable=False)
    owner = db.Column(db.String(80), default="HarvestHub_Owner")
    commodity = db.Column(db.String(80), nullable=False)
    price_kg = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        PrimaryKeyConstraint('agent_id', 'farmer_id', 'bag_id'),
    )

    def __repr__(self):
        return ''


class WareHouse(db.Model):
    __tablename__ = 'warehouse'
    agent_id = db.Column(db.String(10), nullable=False)
    farmer_id = db.Column(db.String(10), nullable=False)
    bag_id = db.Column(db.String(80), unique=True, nullable=False)
    owner = db.Column(db.String(80), default="HarvestHub_Owner")
    commodity = db.Column(db.String(80), nullable=False)
    price_kg = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    delivered = db.Column(db.Boolean, nullable=False)
    profit_percent = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('farmer_id', 'bag_id', 'commodity'),
    )

    def __repr__(self):
        return ''
    

class SellStatistics(db.Model):
    __tablename__ = 'sell_statistics'
    farmer_id = db.Column(db.String(10), unique=True, nullable=False)
    bag_id = db.Column(db.String(80), unique=True, nullable=False)
    owner = db.Column(db.String(80), default="HarvestHub_Owner")
    commodity = db.Column(db.String(80), nullable=False)
    price_kg = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        PrimaryKeyConstraint('farmer_id', 'bag_id', 'commodity'),
    )

    def __repr__(self):
        return ''