from datetime import datetime
from extensions import db
from sqlalchemy.orm import relationship

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    item_code = db.Column(db.String(100), nullable=False, unique=True)
    stock_level = db.Column(db.Integer, nullable=False)
    min_threshold = db.Column(db.Integer, nullable=False)
    max_threshold = db.Column(db.Integer, nullable=False)
    forecasted_demand = db.Column(db.Integer, nullable=True)  # New: Forecasted stock demand
    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="SET NULL"), nullable=True)
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_types.id', ondelete="SET NULL"), nullable=True)
    image = db.Column(db.String(255), nullable=True) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # New: Timestamp for record creation
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # New: Last update time

    category = relationship('Category', backref='inventory')
    unit_type = relationship('UnitType', backref='inventory')