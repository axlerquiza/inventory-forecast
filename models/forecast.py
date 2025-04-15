from datetime import datetime
from extensions import db

class Forecast(db.Model):
    __tablename__ = 'forecast'

    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id', ondelete="SET NULL"), nullable=True, index=True)
    forecasted_demand = db.Column(db.Integer, nullable=False)  # Predicted demand
    forecast_date = db.Column(db.DateTime, default=datetime.utcnow)  # Date of forecast
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    inventory = db.relationship('Inventory', backref=db.backref('forecasts', cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<Forecast Inventory {self.inventory_id} - Demand: {self.forecasted_demand}>"