from application import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import enum

class Permission(enum.IntFlag):
    """Granular permissions system using bitwise flags."""
    VIEW = 1
    EDIT = 2
    DELETE = 4
    MANAGE_USERS = 8
    ADMIN = 15  # All permissions

class User(db.Model, UserMixin):
    """Central user model handling authentication and authorization."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    permissions = db.Column(db.Integer, nullable=False, default=Permission.VIEW,
                          comment="Bitwise combination of Permission flags")
    last_login = db.Column(db.DateTime)
    failed_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True, nullable=False)
    products = db.relationship("Product", back_populates="created_by", foreign_keys="Product.created_by_id")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
