from datetime import datetime
from enum import Enum

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

from application import db


class QuoteStatus(Enum):
    OPEN = "Open"
    CLOSED = "Closed"


class Quote(db.Model):
    __tablename__ = "quotes"

    id = db.Column(db.Integer, primary_key=True)
    quote_number = db.Column(db.Integer, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", name="fk_quote_user"), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default=QuoteStatus.OPEN.value)

    # Product Reference
    product_sku = db.Column(
        db.String(50), db.ForeignKey("products.sku", name="fk_quote_product"), nullable=False
    )

    # Quantity Tiers
    quantity1 = db.Column(db.Integer, nullable=False)
    quantity2 = db.Column(db.Integer)
    quantity3 = db.Column(db.Integer)

    # Pricing
    air_freight1 = db.Column(db.Float)
    ocean_freight1 = db.Column(db.Float)
    markup1 = db.Column(db.Float)
    quote_price1 = db.Column(db.Float, nullable=False)

    air_freight2 = db.Column(db.Float)
    ocean_freight2 = db.Column(db.Float)
    markup2 = db.Column(db.Float)
    quote_price2 = db.Column(db.Float)

    air_freight3 = db.Column(db.Float)
    ocean_freight3 = db.Column(db.Float)
    markup3 = db.Column(db.Float)
    quote_price3 = db.Column(db.Float)

    # PDF Information
    pdf_data = db.Column(db.LargeBinary)
    generated_at = db.Column(db.DateTime)
    last_printed = db.Column(db.DateTime)

    # Relationships
    product = db.relationship("Product", back_populates="quotes")
    user = db.relationship("User", backref="quotes")

    __table_args__ = (
        CheckConstraint(
            "quantity2 > quantity1 OR quantity2 IS NULL",
            name="check_quantity_order_1_2",
        ),
        CheckConstraint(
            "quantity3 > quantity2 OR quantity3 IS NULL",
            name="check_quantity_order_2_3",
        ),
    )

    @validates("quantity1", "quantity2", "quantity3")
    def validate_quantities(self, key, value):
        if key == "quantity1" and value < 1:
            raise ValueError("Quantity1 must be at least 1")
        if key in ["quantity2", "quantity3"] and value is not None:
            prev = getattr(self, f"quantity{int(key[-1])-1}")
            if value <= prev:
                raise ValueError(f"{key} must be greater than previous quantity")
        return value

    @validates("quote_price1", "quote_price2", "quote_price3")
    def validate_prices(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Prices must be positive")
        return value

    @classmethod
    def generate_quote_number(cls):
        last_quote = cls.query.order_by(cls.quote_number.desc()).first()
        return 1000 if not last_quote else last_quote.quote_number + 1

    def __repr__(self):
        return f"<Quote {self.quote_number}>"
