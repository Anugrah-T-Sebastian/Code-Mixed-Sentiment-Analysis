from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, validators, BooleanField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from Sentiment.models import User, Item

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')
    
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class StatementInputForm(FlaskForm):
    input_string = StringField(label='', validators=[Length(min=2, max=100), DataRequired()])
    submit =  SubmitField(label='Submit')


class AddItemform(FlaskForm):
    name = StringField(label='Product Name', validators=[Length(min=2, max=30), DataRequired()])
    company = StringField(label='Company Name', validators=[Length(min=2, max=30)])
    description = StringField(label='Product Description', validators=[Length(min=2, max=30), DataRequired()])
    submit =  SubmitField(label='Add Item')


class ExtractSentimentForm(FlaskForm):
    submit = SubmitField(label='Extract Sentiment')


class EditButtonForm(FlaskForm):
    submit = SubmitField(label='Edit Item')


class RemoveButtonForm(FlaskForm):
    submit = SubmitField(label='Remove Item')


class EditItemForm(FlaskForm): 
    name = StringField(label='Product Name', validators=[Length(min=2, max=30), DataRequired()])
    company = StringField(label='Company Name', validators=[Length(min=2, max=30)])
    description = StringField(label='Product Description', validators=[Length(min=2, max=30), DataRequired()])
    submit =  SubmitField(label='Edit Item')




    