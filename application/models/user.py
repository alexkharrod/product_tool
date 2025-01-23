from application import db, login
from sqlalchemy import Column, Integer, String, Boolean
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum
import enum
import re

class Role(enum.Enum):
    ADMIN = "Admin"
    MARKETING = "Marketing"
    USER = "User"

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(Enum(Role), nullable=False, default=Role.USER)
    last_login = db.Column(db.DateTime)
    failed_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    remember_token = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def is_admin(self):
        return self.role == Role.ADMIN
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    def set_password(self, password):
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{10,128}$', password):
            raise ValueError("Password must contain at least 10 characters, one uppercase letter, one number, and one special character")
        self.password_hash = generate_password_hash(password)
        
    def change_password(self, old_password, new_password):
        if not self.check_password(old_password):
            raise ValueError("Current password is incorrect")
        self.set_password(new_password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
