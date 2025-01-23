from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, DecimalField,
    SubmitField, PasswordField, BooleanField,
    SelectField, IntegerField, DateField, SelectMultipleField
)
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    vendor_name = StringField('Vendor Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    vendor_part_number = StringField('Vendor Part Number', validators=[
        DataRequired(),
        Length(min=3, max=50)
    ])
    sku = StringField('SKU', validators=[
        DataRequired(),
        Length(min=3, max=20)
    ])
    category = SelectField('Category', choices=[
        ('electronics', 'Electronics'),
        ('office', 'Office Supplies'),
        ('tools', 'Tools')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[
        Length(max=500)
    ])
    price = DecimalField('Price', places=2, validators=[
        DataRequired(),
        NumberRange(min=0.01)
    ])
    width = DecimalField('Width (cm)', places=1, validators=[
        DataRequired(),
        NumberRange(min=0.1)
    ])
    length = DecimalField('Length (cm)', places=1, validators=[
        DataRequired(),
        NumberRange(min=0.1)
    ])
    height = DecimalField('Height (cm)', places=1, validators=[
        DataRequired(),
        NumberRange(min=0.1)
    ])
    weight = DecimalField('Weight (kg)', places=1, validators=[
        DataRequired(),
        NumberRange(min=0.1)
    ])
    quantity_per_carton = IntegerField('Quantity per Carton', validators=[
        DataRequired(),
        NumberRange(min=1)
    ])
    moq = IntegerField('Minimum Order Quantity', validators=[
        DataRequired(),
        NumberRange(min=1)
    ])
    production_time = StringField('Production Time', validators=[
        Length(max=50)
    ])
    stock_date = DateField('Stock Date')
    imprint_location = StringField('Imprint Location', validators=[
        Length(max=100)
    ])
    imprint_dimensions = StringField('Imprint Dimensions', validators=[
        Length(max=50)
    ])
    imprint_types = SelectMultipleField('Imprint Types', choices=[
        ('screen', 'Screen Printing'),
        ('embroidery', 'Embroidery'),
        ('laser', 'Laser Engraving')
    ])
    added_to_spreadsheet = BooleanField('Added to Spreadsheet')
    price_list_created = BooleanField('Price List Created')
    new_products_sheet_created = BooleanField('New Products Sheet Created')
    added_to_qb = BooleanField('Added to QuickBooks')
    added_to_web = BooleanField('Added to Website')
    submit = SubmitField('Save Product')
