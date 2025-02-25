from application import db
from sqlalchemy.orm import validates

class Configuration(db.Model):
    __tablename__ = 'configurations'
    
    id = db.Column(db.Integer, primary_key=True)
    dimensional_weight_divisor = db.Column(db.Float, default=5000, nullable=False)
    description = db.Column(db.String(200))
    
    products = db.relationship('Product', backref='config', foreign_keys='Product.config_id', lazy=True)

    @validates('dimensional_weight_divisor')
    def validate_divisor(self, key, divisor):
        if divisor <= 0:
            raise ValueError('Divisor must be a positive number')
        return divisor
