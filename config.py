import os
from dotenv import load_dotenv
import urllib.parse

# Load environment variables from .env file
load_dotenv()

class Config:
    # Database configuration
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    encoded_password = urllib.parse.quote(DB_PASSWORD)
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{encoded_password}@{DB_HOST}/{DB_NAME}"

    # Flask configuration
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("FLASK_DEBUG") == "1"

    # File upload configurations
    PROFILE_PIC_FOLDER = "static/profile_pics/"
    INVENTORY_UPLOAD_FOLDER = "static/inventory_uploads/"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}