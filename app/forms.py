from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, URL
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Password (Repeated)', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username: StringField):
        if User.query.filter_by(username=username.data).first() is not None:
            raise ValidationError('Username already exists')

    def validate_email(self, email: StringField):
        if User.query.filter_by(email=email.data).first() is not None:
            raise ValidationError('Email already exists')


class NewLinkForm(FlaskForm):
    redirect_url = StringField('Redirect URL', validators=[DataRequired()])
    submit = SubmitField('Create')
