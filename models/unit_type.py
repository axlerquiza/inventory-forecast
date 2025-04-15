from extensions import db

class UnitType(db.Model):
    __tablename__ = 'unit_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)  # New column added
