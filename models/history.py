from datetime import datetime
from extensions import db

class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="SET NULL"), nullable=True, index=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id', ondelete="SET NULL"), nullable=True, index=True)
    action_type = db.Column(db.String(50), nullable=False)  # "add_stock" or "remove_stock"
    description = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('history'))
    inventory = db.relationship('Inventory', backref=db.backref('history_records'))

    def __repr__(self):
        return f"<History {self.action_type} - {self.description}>"