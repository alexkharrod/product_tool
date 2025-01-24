from datetime import datetime
from enum import Enum
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import validates, relationship
from application import db
import sqlalchemy as sa

class QuoteTier(db.Model):
    __tablename__ = "quote_tiers"
    
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, ForeignKey('quotes.id'), nullable=False)
    tier_number = db.Column(db.Integer, nullable=False)  # 1-5
    quantity = db.Column(db.Integer, nullable=False)
    air_freight = db.Column(db.Float)
    ocean_freight = db.Column(db.Float)
    markup = db.Column(db.Float)
    quote_price = db.Column(db.Float, nullable=False)
    
    __table_args__ = (
        CheckConstraint("tier_number BETWEEN 1 AND 5", name="check_tier_number_range"),
        CheckConstraint("quantity > 0", name="check_positive_quantity"),
        CheckConstraint("quote_price > 0", name="check_positive_price"),
    )
    
    @validates('quantity')
    def validate_quantity(self, key, value):
        if value <= 0:
            raise ValueError("Quantity must be positive")
        return value
        
    @validates('quote_price')
    def validate_price(self, key, value):
        if value <= 0:
            raise ValueError("Price must be positive")
        return value


class QuoteStatus(Enum):
    OPEN = "Open"
    CLOSED = "Closed"


class Quote(db.Model):
    __tablename__ = "quotes"

    id = db.Column(db.Integer, primary_key=True)
    quote_number = db.Column(db.Integer, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", name="fk_quote_user"), nullable=False
    )
    customer_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default=QuoteStatus.OPEN.value)

    # Product Reference
    product_sku = db.Column(
        db.String(50),
        db.ForeignKey("products.sku", name="fk_quote_product"),
        nullable=False,
    )

    # Product Dimensions
    length = db.Column(sa.Numeric(6,1), nullable=False, comment="Length in centimeters")
    width = db.Column(sa.Numeric(6,1), nullable=False, comment="Width in centimeters")
    height = db.Column(sa.Numeric(6,1), nullable=False, comment="Height in centimeters")
    weight = db.Column(sa.Numeric(8,2), nullable=False, comment="Weight in kilograms")
    quantity_per_ctn = db.Column(db.Integer, nullable=False, comment="Units per carton")

    # Pricing Tiers (1-5)
    tiers = relationship("QuoteTier", 
                        backref="quote", 
                        cascade="all, delete-orphan",
                        order_by="QuoteTier.tier_number")

    # PDF Information
    pdf_data = db.Column(db.LargeBinary)
    generated_at = db.Column(db.DateTime)
    last_printed = db.Column(db.DateTime)

    # Relationships
    product = db.relationship("Product", back_populates="quotes")
    user = db.relationship("User", backref="quotes")

    __table_args__ = (
        CheckConstraint(
            "(SELECT COUNT(*) FROM quote_tiers WHERE quote_id = id) BETWEEN 1 AND 5",
            name="check_tier_count"
        ),
    )

    @validates('tiers')
    def validate_tiers(self, key, tiers):
        if not tiers:
            raise ValueError("At least one pricing tier required")
            
        # Ensure tier numbers are sequential and quantities increase
        prev_quantity = 0
        for tier in sorted(tiers, key=lambda t: t.tier_number):
            if tier.tier_number < 1 or tier.tier_number > 5:
                raise ValueError("Tier numbers must be between 1-5")
                
            if tier.quantity <= prev_quantity:
                raise ValueError("Quantities must be in ascending order")
                
            prev_quantity = tier.quantity
            
        return tiers

    @classmethod
    def generate_quote_number(cls):
        last_quote = cls.query.order_by(cls.quote_number.desc()).first()
        return 1000 if not last_quote else last_quote.quote_number + 1

    def __repr__(self):
        return f"<Quote {self.quote_number}>"
