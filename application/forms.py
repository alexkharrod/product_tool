from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, DecimalField, FloatField,
    SubmitField, PasswordField, BooleanField,
    SelectField, IntegerField, DateField, SelectMultipleField,
    FieldList, FormField
)
from wtforms.validators import (
    DataRequired, InputRequired, Length, 
    NumberRange, Email, EqualTo
)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password')
    ])
    submit = SubmitField('Register')

class CreateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    is_admin = BooleanField('Administrator')
    submit = SubmitField('Create User')

class EditUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_admin = BooleanField('Administrator')
    submit = SubmitField('Update User')

class ProductSearchForm(FlaskForm):
    sku = StringField('Product SKU', validators=[
        Length(min=2, max=100)
    ], render_kw={"placeholder": "Search by SKU..."})
    vendor_name = StringField('Vendor Name', validators=[
        Length(min=2, max=100)
    ], render_kw={"placeholder": "Filter by vendor..."})
    submit = SubmitField('Search')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ], render_kw={"placeholder": "Enter product name..."})
    
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(min=10, max=500)
    ], render_kw={"placeholder": "Describe the product features and specifications...", "rows": 4})
    
    submit = SubmitField('Save Product')

class TierForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=99999999)])
    unit_cost = FloatField('Unit Cost', validators=[
        DataRequired(),
        NumberRange(min=0.01)
    ], render_kw={"step": "0.01"})
    air_freight = FloatField('Air Freight', validators=[NumberRange(max=99999.99)], render_kw={"step": "0.01"})
    ocean_freight = FloatField('Ocean Freight', validators=[NumberRange(max=99999.99)], render_kw={"step": "0.01"})
    markup = FloatField('Markup %', validators=[NumberRange(min=0, max=99.99)], render_kw={"step": "0.01"})
    quote_price = FloatField('Price', validators=[
        DataRequired(), 
        NumberRange(min=0.01, max=99999999.99)
    ], render_kw={"step": "0.01"})

class QuoteForm(FlaskForm):
    """Form for creating/editing quotes with tiered pricing"""
    customer_name = StringField('Customer Name', validators=[
        DataRequired(),
        Length(min=2, max=100),
        InputRequired(message="Customer name is required")
    ], render_kw={"placeholder": "Acme Corp", "autofocus": True})
    
    # Product Reference
    product_sku = SelectField('Product', coerce=str, validators=[DataRequired()])
    
    # Product Dimensions
    length = DecimalField('Length (cm)', validators=[DataRequired(), NumberRange(min=0.1)], 
                        render_kw={"step": "0.1"})
    width = DecimalField('Width (cm)', validators=[DataRequired(), NumberRange(min=0.1)])
    height = DecimalField('Height (cm)', validators=[DataRequired(), NumberRange(min=0.1)])
    weight = DecimalField('Weight (kg)', validators=[DataRequired(), NumberRange(min=0.01)],
                        render_kw={"step": "0.01"})
    quantity_per_ctn = IntegerField('Quantity per Carton', validators=[DataRequired(), NumberRange(min=1)])
    
    # Pricing Tiers
    tiers = FieldList(
        FormField(TierForm),
        min_entries=1,
        max_entries=5,
        label="Pricing Tiers"
    )
    
    add_tier = SubmitField('Add Tier', render_kw={"class": "btn-secondary"})
    submit = SubmitField('Save Quote', render_kw={"class": "btn-primary"})
