from datetime import datetime
from enum import Enum
from application import db
from sqlalchemy import Sequence, CheckConstraint
from sqlalchemy.orm import validates
from application.models.product import Product
from application.models.user import User

class QuoteStatus(Enum):
    OPEN = "Open"
    CLOSED = "Closed"

class Quote(db.Model):
    __tablename__ = 'quotes'
    
    # Primary Information
    id = db.Column(db.Integer, primary_key=True)
    quote_number = db.Column(db.Integer, 
                           Sequence('quote_seq', start=1000, increment=1),
                           unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    rep_email = db.Column(db.String(120), db.ForeignKey('users.email'), nullable=False)
    customer_name = db.Column(db.String(150), nullable=False)
    status = db.Column(db.Enum(QuoteStatus), default=QuoteStatus.OPEN)
    
    # Product Reference
    product_id = db.Column(db.String(50), db.ForeignKey('products.sku'), nullable=False)
    product = db.relationship('Product', backref='quotes')
    
    # Quantity Tiers
    quantity1 = db.Column(db.Integer, nullable=False)
    air_freight1 = db.Column(db.Float)
    ocean_freight1 = db.Column(db.Float)
    markup1 = db.Column(db.Float)
    quote_price1 = db.Column(db.Float, nullable=False)
    
    quantity2 = db.Column(db.Integer)
    air_freight2 = db.Column(db.Float)
    ocean_freight2 = db.Column(db.Float)
    markup2 = db.Column(db.Float)
    quote_price2 = db.Column(db.Float)
    
    quantity3 = db.Column(db.Integer)
    air_freight3 = db.Column(db.Float)
    ocean_freight3 = db.Column(db.Float)
    markup3 = db.Column(db.Float)
    quote_price3 = db.Column(db.Float)
    
    # PDF Information
    generated_pdf = db.Column(db.LargeBinary)
    pdf_generated_at = db.Column(db.DateTime)
    last_printed_at = db.Column(db.DateTime)
    
    # Relationships
    rep = db.relationship('User', foreign_keys=[rep_email], backref='quotes')
    
    __table_args__ = (
        CheckConstraint('quantity2 IS NULL OR quantity2 > quantity1', 
                       name='check_quantity_order_2'),
        CheckConstraint('quantity3 IS NULL OR quantity3 > quantity2', 
                       name='check_quantity_order_3'),
    )

    @validates('quantity1', 'quantity2', 'quantity3')
    def validate_quantities(self, key, value):
        if value is not None and value < 1:
            raise ValueError("Quantity must be at least 1")
        return value

    @validates('quote_price1', 'quote_price2', 'quote_price3')
    def validate_prices(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Price must be a positive number")
        return value

    @validates('quote_number')
    def validate_quote_number(self, key, number):
        if Quote.query.filter(Quote.quote_number == number).first():
            raise ValueError("Quote number must be unique")
        return number

    @validates('status')
    def validate_status_transitions(self, key, status):
        if self.status == QuoteStatus.CLOSED and status != QuoteStatus.CLOSED:
            raise ValueError("Cannot reopen a closed quote")
        return status

    def __repr__(self):
        return f'<Quote {self.quote_number} - {self.customer_name}>'
