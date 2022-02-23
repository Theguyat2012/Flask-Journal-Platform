from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class VideoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description')
    video = FileField('Video')
    submit = SubmitField('Upload')
