from datetime import datetime
from extensions import db

class Restock(db.Model):
    __tablename__ = 'restock'

    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id', ondelete="SET NULL"), nullable=True, index=True)
    quantity_added = db.Column(db.Integer, nullable=True)
    cost_price_at_time = db.Column(db.Float, nullable=False)  # Store cost price at restock time
    total_cost = db.Column(db.Float, nullable=False)  # quantity_added * cost_price_at_time
    restocked_at = db.Column(db.DateTime, default=datetime.utcnow)

    inventory = db.relationship('Inventory', backref=db.backref('restock_records'))

    def __repr__(self):
        return f"<Restock {self.quantity_added} units for {self.inventory_id}>"