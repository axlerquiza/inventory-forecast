from datetime import datetime
from extensions import db

class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id', ondelete="SET NULL"), nullable=True, index=True)
    quantity_sold = db.Column(db.Integer, nullable=False)
    selling_price_at_time = db.Column(db.Float, nullable=False)  # Store selling price at sale time
    total_revenue = db.Column(db.Float, nullable=False)  # quantity_sold * selling_price_at_time
    sold_at = db.Column(db.DateTime, default=datetime.utcnow)

    inventory = db.relationship('Inventory', backref=db.backref('sales_records'))

    def __repr__(self):
        return f"<Sale {self.quantity_sold} units for {self.inventory_id}>"