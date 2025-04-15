from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_login import current_user
from config import Config
from extensions import db, bcrypt, login_manager
from models.user import User
from models.role import Role
from controllers.auth_controller import auth_bp
from controllers.forgotpassword_controller import forgotpassword_bp
from controllers.dashboard_controller import dashboard_bp
from controllers.inventory_controller import inventory_bp
from controllers.sales_controller import sales_bp
from controllers.restocking_controller import restocking_bp
from controllers.reports_controller import reports_bp
from controllers.statistics_controller import statistics_bp
from controllers.notifications_controller import notifications_bp
from controllers.accounts_controller import accounts_bp
from controllers.profile_controller import profile_bp
from controllers.category_controller import category_bp
from controllers.unit_type_controller import unit_type_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db)

# Set the login view to the new login route
login_manager.login_view = 'auth.login'

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(forgotpassword_bp) 
app.register_blueprint(dashboard_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(restocking_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(statistics_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(accounts_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(category_bp)
app.register_blueprint(unit_type_bp)

# Redirect root route ("/") to the login page if not logged in
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.view'))  # Redirect to dashboard if user is logged in
    return redirect(url_for('auth.login'))  # Redirect to login page if user is not logged in

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

from admin import create_admin
with app.app_context():
    db.create_all()  # Create tables if they don't exist
    Role.create_default_roles()  # Call the method to create default roles
    create_admin()  # Creates admin [username: admin, password: 123]

if __name__ == '__main__':
    app.run()
    