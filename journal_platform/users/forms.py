from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
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
    bio = TextAreaField('Bio (255 characters)')
    submit = SubmitField('Update')

class LinksForm(FlaskForm):
    title = StringField('Title')
    url = StringField('URL')
    submit = SubmitField('Save')

class LinkUpdateForm(FlaskForm):
    id = IntegerField()
    title = StringField('Title')
    url = StringField('URL')
    update = SubmitField('Update')

class FollowForm(FlaskForm):
    submit = SubmitField('Follow')

class UnfollowForm(FlaskForm):
    submit = SubmitField('Unfollow')
