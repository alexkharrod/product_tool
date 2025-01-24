from application import db, login
from sqlalchemy import Column, Integer, String, Boolean
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum
import enum
import re

class Role(enum.Enum):
    """Defines system roles with access control levels.
    
    Values:
        ADMIN: Full system access and administration privileges
        MARKETING: Access to product/quote management features 
        USER: Basic authenticated access with profile management
    """
    ADMIN = "Admin"
    MARKETING = "Marketing"
    USER = "User"

class User(db.Model, UserMixin):
    """Central user model handling authentication and authorization.
    
    Attributes:
        id (int): Primary key identifier
        email (str): Unique email address used for login (max 120 chars)
        password_hash (str): Securely hashed password using Werkzeug
        role (Role): Access level via Role enum (default: USER)
        last_login (DateTime): Timestamp of last successful authentication
        failed_attempts (int): Count of consecutive failed login attempts
        locked_until (DateTime): Account lock expiration time if locked
        remember_token (str): Token for persistent login sessions
        is_active (bool): Soft delete flag (default: True)
    """
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(Enum(Role), nullable=False, default=Role.USER,
                    comment="Allowed values: 'Admin', 'Marketing', 'User'")
    last_login = db.Column(db.DateTime)
    failed_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    remember_token = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    products = db.relationship("Product", back_populates="created_by", lazy="dynamic")

    def __repr__(self):
        """Official string representation of User instance.
        
        Returns:
            str: Readable format showing user email
        """
        return f'<User {self.email}>'
    
    @classmethod
    def get_by_email(cls, email):
        """Retrieve user by email address.
        
        Args:
            email (str): Email address to search for
            
        Returns:
            User: First matching user instance or None
        """
        return cls.query.filter_by(email=email).first()
        
    def change_password(self, old_password, new_password):
        """Securely update user password after validation.
        
        Args:
            old_password (str): Current password for verification
            new_password (str): New password to set
            
        Raises:
            ValueError: If old password doesn't match or new password invalid
        """
        if not self.check_password(old_password):
            raise ValueError("Current password is incorrect")
        self.set_password(new_password)
    
    def is_admin(self):
        """Check if user has administrative privileges.
        
        Returns:
            bool: True if role is ADMIN, False otherwise
        """
        return self.role == Role.ADMIN

    def set_password(self, password):
        """Hash and store password following security policies.
        
        Args:
            password (str): Plain text password to hash
            
        Raises:
            ValueError: If password fails complexity requirements:
                - 10-128 characters
                - At least 1 uppercase letter
                - At least 1 number
                - At least 1 special character
        """
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{10,128}$', password):
            raise ValueError("Password must contain at least 10 characters, one uppercase letter, one number, and one special character")
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Verify password against stored hash.
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches hash, False otherwise
        """
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    """Flask-Login user loader callback.
    
    Args:
        id (str): User ID as string from session
        
    Returns:
        User: User instance if found, None otherwise
    """
    return User.query.get(int(id))
