from application import db
from datetime import datetime
from sqlalchemy import Enum
import enum

class ActionType(enum.Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    LOCKOUT = "LOCKOUT"

class EntityType(enum.Enum):
    QUOTE = "Quote"
    PRODUCT = "Product"
    USER = "User"
    CONFIG = "Configuration"

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action_type = db.Column(Enum(ActionType), nullable=False)
    entity_type = db.Column(Enum(EntityType), nullable=False)
    entity_id = db.Column(db.String(50), nullable=False)
    changes = db.Column(db.JSON, nullable=True)
    ip_address = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f'<AuditLog {self.action_type} {self.entity_type} {self.entity_id}>'
