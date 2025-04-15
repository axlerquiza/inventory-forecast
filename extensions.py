from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
