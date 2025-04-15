from extensions import db, bcrypt
from models.user import User
import logging

def create_admin():
    """Ensure an admin account always exists."""
    admin_username = "admin"
    admin_password = "123"
    admin_email = "admin@email.com"

    # Check if admin already exists
    existing_admin = User.query.filter_by(username=admin_username).first()
    if existing_admin:
        logging.info("Admin account already exists.")
        return

    # Create admin user
    hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')
    admin_user = User(username=admin_username, email=admin_email, password=hashed_password, role_id=1)
    db.session.add(admin_user)
    db.session.commit()
    logging.info("Admin account created successfully.")
