import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables first
load_dotenv()


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]  # Required - set in .env
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or f"sqlite:///{Path(__file__).parent}/instance/production.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CKEditor configuration
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_HEIGHT = 400
    CKEDITOR_TOOLBAR = [
        {"name": "basicstyles", "items": ["Bold", "Italic"]},
        {"name": "lists", "items": ["BulletedList"]},
        {"name": "tools", "items": ["Maximize"]},
    ]
    PDF_STORAGE_PATH = Path(__file__).parent / "instance/pdfs"
    PDF_MAX_IMAGE_DIMENSIONS = (1200, 800)  # width, height in pixels
    PDF_ALLOWED_MIME_TYPES = ["image/png", "image/jpeg", "image/webp"]
    PDF_DEFAULT_DPI = 300
    DIMENSIONAL_DIVISOR = 5000  # Standard divisor for dimensional weight calculation

    # Security settings
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    REMEMBER_COOKIE_DURATION = 604800  # 1 week

    # Email configuration
    MAIL_SERVER = os.environ["MAIL_SERVER"]
    MAIL_PORT = int(os.environ["MAIL_PORT"])
    MAIL_USE_TLS = os.environ["MAIL_USE_TLS"].lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{(Path(__file__).parent / 'instance/dev.db').absolute()}"
    )
    SERVER_NAME = "localhost:3001"  # Match curl request host
    PREFERRED_URL_SCHEME = "http" 
    FLASK_RUN_PORT = 3001  # Default port for flask run


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
