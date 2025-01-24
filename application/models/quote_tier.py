from application import db
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import validates

class QuoteTier(db.Model):
    __tablename__ = 'quote_tiers'
    
    id = db.Column(db.Integer, primary_key=True)
    tier_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    description = db.Column(db.Text)
    quote_id = db.Column(db.Integer, ForeignKey('quotes.id'), nullable=False)
    
    # Relationship
    quote = db.relationship('Quote', back_populates='tiers')
    
    __table_args__ = (
        CheckConstraint('tier_number BETWEEN 1 AND 5', name='check_tier_range'),
        CheckConstraint('price > 0', name='check_positive_price'),
        {'comment': 'Pricing tiers for volume discounts'}
    )

    @validates('tier_number')
    def validate_tier_number(self, key, tier_number):
        if not 1 <= tier_number <= 5:
            raise ValueError("Tier number must be between 1-5")
        return tier_number
    
    def __repr__(self):
        return f'<QuoteTier T{self.tier_number} {self.name} ${self.price}>'
