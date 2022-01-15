from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms import validators
from wtforms.validators import DataRequired


class VideoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description')
    video = FileField('Video', validators=[FileAllowed('mp4'), DataRequired()])
    submit = SubmitField('Upload')
