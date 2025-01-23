from application import db
from sqlalchemy.orm import validates

class Configuration(db.Model):
    __table_args__ = {'extend_existing': True}  # Add this line to ensure table metadata is refreshed
    __tablename__ = 'configurations'
    
    id = db.Column(db.Integer, primary_key=True)
    dimensional_weight_divisor = db.Column(db.Float, default=5000, nullable=False)
    description = db.Column(db.String(200))
    
    products = db.relationship('Product', backref='config', lazy=True)

    @validates('dimensional_weight_divisor')
    def validate_divisor(self, key, divisor):
        if divisor <= 0:
            raise ValueError('Divisor must be a positive number')
        return divisor
