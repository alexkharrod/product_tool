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

class TierForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=99999999)])
    air_freight = FloatField('Air Freight', validators=[NumberRange(max=99999.99)], render_kw={"step": "0.01"})
    ocean_freight = FloatField('Ocean Freight', validators=[NumberRange(max=99999.99)], render_kw={"step": "0.01"})
    markup = FloatField('Markup %', validators=[NumberRange(min=0, max=99.99)], render_kw={"step": "0.01"})
    quote_price = FloatField('Price', validators=[
        DataRequired(), 
        NumberRange(min=0.01, max=99999999.99)
    ], render_kw={"step": "0.01"})

class QuoteForm(FlaskForm):
    """Form for creating/editing quotes with dynamic pricing tiers"""
    customer_name = StringField('Customer Name', validators=[
        DataRequired(),
        Length(min=2, max=100),
        InputRequired(message="Customer name is required")
    ], render_kw={"placeholder": "Acme Corp"})
    
    tiers = FieldList(
        FormField(TierForm),
        min_entries=1,
        max_entries=10,
        label="Pricing Tiers"
    )
    
    add_tier = SubmitField('➕ Add Tier', render_kw={"class": "btn-secondary"})
    submit = SubmitField('💾 Save Quote', render_kw={"class": "btn-primary"})
