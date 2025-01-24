import re
import urllib.parse
from datetime import datetime
from flask import current_app
from sqlalchemy.orm import validates
from application import db

class Product(db.Model):
    """Core product model with pricing tiers and validation"""
    __tablename__ = "products"

    # Configuration Relationship
    config_id = db.Column(db.Integer, db.ForeignKey('configurations.id'))
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Unique Product Identifier
    sku = db.Column(db.String(50), unique=True, nullable=False)
    
    # Product Information
    name = db.Column(db.String(100), nullable=False)
    vendor_name = db.Column(db.String(100), nullable=False)
    vendor_part_number = db.Column(db.String(15))
    category = db.Column(db.String(5), nullable=False)
    keywords = db.Column(db.Text)
    description = db.Column(db.Text)
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
    imprint_types = db.Column(db.String(200))
    production_time = db.Column(db.String(50), nullable=False, comment="Production time description (e.g. '4-6 weeks')")
    stock_date = db.Column(db.Date)

    # Status Tracking
    in_spreadsheet = db.Column(db.Boolean, default=False)
    price_list_created = db.Column(db.Boolean, default=False)
    new_products_sheet_created = db.Column(db.Boolean, default=False)
    in_qb = db.Column(db.Boolean, default=False)
    in_web = db.Column(db.Boolean, default=False)

    # Relationships
    quotes = db.relationship(
        "Quote", back_populates="product", cascade="all, delete-orphan", lazy=True
    )
    created_by = db.relationship("User", back_populates="products", foreign_keys=[created_by_id])
    tiers = db.relationship(
        "ProductTier", 
        backref="product", 
        order_by="ProductTier.index",
        cascade="all, delete-orphan",
        lazy=True
    )

    # Validations
    @validates("sku")
    def validate_sku(self, key, sku):
        if Product.query.filter_by(sku=sku).first() and not self.sku:
            raise ValueError("SKU must be unique")
        return sku

    @validates("image_url")
    def validate_image_url(self, key, url):
        if url:
            result = urllib.parse.urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise ValueError("Invalid URL format")
        return url

    @validates("width", "length", "height", "weight")
    def validate_dimensions(self, key, value):
        if value <= 0:
            raise ValueError(f"{key} must be positive")
        return value

    @validates("production_time")
    def validate_production_time(self, key, value):
        if not isinstance(value, str):
            raise ValueError("Production time must be a string")
        if len(value) > 50:
            raise ValueError("Production time cannot exceed 50 characters")
        return value

    @validates("tiers")
    def validate_tiers(self, key, tiers):
        if len(tiers) > 7:
            raise ValueError("Maximum of 7 pricing tiers allowed")
            
        quantities = [t.quantity for t in tiers]
        costs = [float(t.unit_cost) for t in tiers]
        
        if any(q1 >= q2 for q1, q2 in zip(quantities, quantities[1:])):
            raise ValueError("Tier quantities must be strictly increasing")
            
        if any(c1 < c2 for c1, c2 in zip(costs, costs[1:])):
            raise ValueError("Tier costs must be descending or equal")
            
        return tiers

    @property
    def dimensional_weight(self):
        divisor = current_app.config["DIMENSIONAL_DIVISOR"]
        return (self.width * self.length * self.height) / divisor

    @property
    def completion_status(self):
        return all([
            self.in_spreadsheet,
            self.price_list_created,
            self.new_products_sheet_created,
            self.in_qb,
            self.in_web,
        ])

    def __repr__(self):
        return f"<Product {self.sku}>"

class ProductTier(db.Model):
    __tablename__ = "product_tiers"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Numeric(10,2), nullable=False)
    effective_date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    index = db.Column(db.Integer, nullable=False)

    @validates('quantity', 'unit_cost')
    def validate_tier_values(self, key, value):
        if key == 'quantity' and value < 1:
            raise ValueError("Quantity must be at least 1")
        if key == 'unit_cost' and value <= 0:
            raise ValueError("Unit cost must be positive")
        return value
