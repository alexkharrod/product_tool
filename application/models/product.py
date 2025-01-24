from flask import current_app
from application import db
from sqlalchemy import event
from sqlalchemy.orm import validates
from datetime import datetime
import re
import urllib.parse

class Product(db.Model):
    __tablename__ = 'products'
    
    # Primary Information
    sku = db.Column(db.String(50), primary_key=True)
    vendor_name = db.Column(db.String(100), nullable=False)
    vendor_part_number = db.Column(db.String(50))
    category = db.Column(db.String(100), nullable=False)
    keywords = db.Column(db.Text)
    description = db.Column(db.Text)  # Rich text content
    image_url = db.Column(db.String(500))
    
    # Dimensional Information
    length = db.Column(db.Float, nullable=False)
    width = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    quantity_per_ctn = db.Column(db.Integer, nullable=False)
    
    # Production Information
    moq = db.Column(db.Integer, nullable=False)
    package_type = db.Column(db.String(100))
    imprint_location = db.Column(db.String(100))
    imprint_dimensions = db.Column(db.String(50))
    imprint_types = db.Column(db.String(200))  # Comma-separated values
    production_time = db.Column(db.String(50))
    stock_date = db.Column(db.Date)
    
    # Status Tracking
    in_spreadsheet = db.Column(db.Boolean, default=False)
    price_list_created = db.Column(db.Boolean, default=False)
    new_products_sheet_created = db.Column(db.Boolean, default=False)
    in_qb = db.Column(db.Boolean, default=False)
    in_web = db.Column(db.Boolean, default=False)
    
    # Relationships
    quotes = db.relationship('Quote', back_populates='product', cascade='all, delete-orphan', lazy=True)
    config_id = db.Column(db.Integer, db.ForeignKey('configurations.id'))
    
    # Validation Methods
    @validates('sku')
    def validate_sku(self, key, sku):
        if not re.match(r'^[A-Z0-9-]{5,}$', sku):
            raise ValueError('Invalid SKU format')
        if Product.query.filter_by(sku=sku).first() and not self.sku:
            raise ValueError('SKU must be unique')
        return sku
    
    @validates('image_url')
    def validate_image_url(self, key, url):
        if url:
            result = urllib.parse.urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise ValueError('Invalid URL format')
        return url
    
    @validates('width', 'length', 'height', 'weight')
    def validate_dimensions(self, key, value):
        if value <= 0:
            raise ValueError(f'{key} must be positive')
        return value
    
    @property
    def dimensional_weight(self):
        divisor = current_app.config['DIMENSIONAL_DIVISOR']
        return (self.width * self.length * self.height) / divisor
    
    @property
    def completion_status(self):
        return all([
            self.in_spreadsheet,
            self.price_list_created,
            self.new_products_sheet_created,
            self.in_qb,
            self.in_web
        ])

    def __repr__(self):
        return f'<Product {self.sku}>'
