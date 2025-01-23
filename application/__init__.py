from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import DevelopmentConfig

# Initialize extensions first
db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()

# Import models after extensions but before migrate initialization
from application.models.user import User
from application.models.product import Product
from application.models.quote import Quote
from application.models.configuration import Configuration
from application.models.audit_log import AuditLog

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        # Configure all model relationships
        db.configure_mappers()
    
    # Register blueprints with URL prefixes
    from application.routes.main import bp as main_bp
    from application.routes.auth import bp as auth_bp
    from application.routes.product import bp as product_bp
    from application.routes.quote import bp as quote_bp
    from application.routes.admin.dashboard import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(quote_bp, url_prefix='/quotes')
    app.register_blueprint(admin_bp)
    
    return app
