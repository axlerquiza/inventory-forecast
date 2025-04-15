from extensions import db

class Role(db.Model):
    __tablename__ = 'roles'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    @staticmethod
    def create_default_roles():
        """Create default roles if they don't already exist."""
        default_roles = [
            {"id": 1, "name": "Admin", "description": "Full system access"},
            {"id": 2, "name": "Manager", "description": "Manage inventory and employees"},
            {"id": 3, "name": "Employee", "description": "Basic access to inventory"},
        ]
        for role_data in default_roles:
            role = Role.query.get(role_data["id"])
            if not role:
                role = Role(**role_data)
                db.session.add(role)
        db.session.commit()