from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.fields.simple import PasswordField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Length,Email

from app.Model.models import User

class RegistrationForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    student=BooleanField('I am a student')
    faculty=BooleanField('I am a faculty member')
    email=StringField('Email',validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired()])
    password2=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username already exists. Please use a different username.')

    def validate_email(self,email):
        _email = User.query.filter_by(email=email.data).first()
        if _email is not None:
            raise ValidationError('This email is already in user. Please use a different email address.')

class LoginForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    remember_me=BooleanField('Remember me')
    submit=SubmitField('Sign in')