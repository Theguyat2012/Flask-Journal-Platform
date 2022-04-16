from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=255)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')

class EditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=255)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image = FileField('Profile Picture')
    submit = SubmitField('Update')

class FollowForm(FlaskForm):
    submit = SubmitField('Follow')

class UnfollowForm(FlaskForm):
    submit = SubmitField('Unfollow')
