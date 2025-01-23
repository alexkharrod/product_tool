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

class QuoteForm(FlaskForm):
    title = StringField('Quote Title', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    content = TextAreaField('Quote Content', validators=[
        DataRequired(),
        Length(min=10, max=2000)
    ])
    submit = SubmitField('Save Quote')
