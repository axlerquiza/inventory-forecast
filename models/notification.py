from datetime import datetime
from extensions import db

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="SET NULL"), nullable=True, index=True)
    action_type = db.Column(db.String(50), nullable=False)  # "add", "update", "delete"
    entity_type = db.Column(db.String(50), nullable=False)  # "account", "category", "unit_type", "inventory", "restock", "sale"
    description = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('notifications'))

    def __repr__(self):
        return f"<Notification {self.entity_type} - {self.action_type}>"