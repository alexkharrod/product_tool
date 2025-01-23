from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
ckeditor = CKEditor()


def create_app():
    app = Flask(
        __name__,
        instance_path="/Users/alexharrod/Documents/PythonProjects/product_tool/instance",
        instance_relative_config=True,
    )

    # Add datetime format filter
    app.jinja_env.filters["datetime"] = lambda value: (
        value.strftime("%Y-%m-%d %H:%M") if value else ""
    )
    app.config.from_object("application.config.DevelopmentConfig")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)
    ckeditor.init_app(app)

    # Import models after db initialization
    from application import models
    from application.routes.admin.dashboard import admin_bp
    from application.routes.auth import auth_bp

    # Register blueprints
    from application.routes.main import main_bp

    app.register_blueprint(main_bp, url_prefix="/")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app


