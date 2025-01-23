import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables first
load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-123")
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
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{(Path(__file__).parent / 'instance/dev.db').absolute()}"
    )
    SERVER_NAME = "127.0.0.1:5003"  # Must match explicit host/port
    PREFERRED_URL_SCHEME = "http"
    FLASK_RUN_PORT = 5003  # Set default port for flask run command


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
