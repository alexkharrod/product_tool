from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from .config import DevelopmentConfig

# Initialize extensions first
db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

# Import models after extensions but before migrate initialization
from application.models.user import User
from application.models.product import Product, ProductTier
from application.models.quote import Quote
from application.models.configuration import Configuration
from application.models.audit_log import AuditLog

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Add robust datetime filter with null handling
    from datetime import datetime
    def format_datetime(value, format='%Y-%m-%d %H:%M'):
        try:
            if value is None:
                return 'Never'
            if isinstance(value, datetime):
                return value.strftime(format)
            return value.strftime(format)  # Handle dateutil objects
        except Exception as e:
            app.logger.error(f"Datetime filter error: {str(e)}")
            return 'Invalid date'
    app.jinja_env.filters['datetime'] = format_datetime
    
    # Configure login manager
    login.login_view = 'auth.login'
    login.login_message_category = 'info'
    
    # Initialize extensions
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    with app.app_context():
        # Configure all model relationships
        db.configure_mappers()
    
    # Register blueprints with URL prefixes
    from application.routes.main import main_bp
    from application.routes.auth import bp as auth_bp
    from application.routes.product import product as product_bp
    from application.routes.quote import bp as quote_bp
    from application.routes.admin.dashboard import admin_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(product_bp, url_prefix='/')
    app.register_blueprint(quote_bp, url_prefix='/quotes')
    app.register_blueprint(admin_bp)
    
    return app
