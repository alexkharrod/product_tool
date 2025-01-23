from datetime import date
from enum import Enum
from application import db
from sqlalchemy import event
from sqlalchemy.orm import validates
import re
from urllib.parse import urlparse
import bleach

class ImprintType(Enum):
    SPOT_COLOR = "Spot Color"
    FULL_COLOR = "Full Color"
    EDGE_TO_EDGE = "Edge to Edge Full Color"
    ENGRAVE = "Engrave"

class Product(db.Model):
    __tablename__ = 'products'
    
    # Primary Information
    sku = db.Column(db.String(50), primary_key=True)
    vendor_name = db.Column(db.String(100), nullable=False)
    vendor_part_number = db.Column(db.String(100))
    category = db.Column(db.String(50), nullable=False)
    keywords = db.Column(db.Text)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    
    # Dimensional Information
    width_cm = db.Column(db.Float, nullable=False)
    length_cm = db.Column(db.Float, nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    quantity_per_carton = db.Column(db.Integer, nullable=False)
    
    # Configuration Reference
    configuration_id = db.Column(db.Integer, db.ForeignKey('configurations.id', name='fk_product_configuration_id'))
    
    # Production Information
    moq = db.Column(db.Integer, nullable=False)
    package_type = db.Column(db.String(50))
    imprint_location = db.Column(db.String(100))
    imprint_dimensions = db.Column(db.String(50))
    imprint_types = db.Column(db.JSON)  # Stores list of ImprintType values
    production_time = db.Column(db.String(50))
    stock_date = db.Column(db.Date)
    
    # Status Tracking
    added_to_spreadsheet = db.Column(db.Boolean, default=False)
    price_list_created = db.Column(db.Boolean, default=False)
    new_products_data_sheet = db.Column(db.Boolean, default=False)
    added_to_qb = db.Column(db.Boolean, default=False)
    added_to_web = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                         onupdate=db.func.current_timestamp())

    @property
    def dimensional_weight(self):
        from application.models.configuration import Configuration
        config = Configuration.query.first()
        divisor = config.dimensional_weight_divisor if config else 5000
        return (self.width_cm * self.length_cm * self.height_cm) / divisor

    @property
    def completion_status(self):
        return all([
            self.added_to_spreadsheet,
            self.price_list_created,
            self.new_products_data_sheet,
            self.added_to_qb,
            self.added_to_web
        ])

    @validates('sku')
    def validate_sku(self, key, sku):
        if not re.match(r'^[A-Z]{3}-\d{4}-[A-Z0-9]{3}$', sku):
            raise ValueError("Invalid SKU format. Expected format: ABC-1234-XYZ")
        if Product.query.filter(Product.sku == sku).first():
            raise ValueError("SKU must be unique")
        return sku

    @validates('image_url')
    def validate_image_url(self, key, url):
        if url:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise ValueError("Invalid URL format")
        return url

    @validates('width_cm', 'length_cm', 'height_cm', 'weight_kg')
    def validate_dimensions(self, key, value):
        if value <= 0:
            raise ValueError(f"{key} must be a positive number")
        return value

    @validates('moq')
    def validate_moq(self, key, value):
        if value < 1:
            raise ValueError("MOQ must be at least 1")
        return value

    @validates('description')
    def sanitize_description(self, key, description):
        # Allow basic formatting while stripping other HTML
        allowed_tags = ['ul', 'ol', 'li', 'i', 'em', 'strong']
        # Implementation would use a proper HTML sanitizer like Bleach
        return bleach.clean(description, tags=allowed_tags, strip=True)

    def __repr__(self):
        return f'<Product {self.sku} - {self.vendor_name}>'
