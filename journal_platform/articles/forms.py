from flask_wtf import FlaskForm
from wtforms.fields import MultipleFileField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class NewArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content')
    photos = MultipleFileField('Photos')
    videos = MultipleFileField('Videos')
    post = SubmitField('Post')
    draft = SubmitField('Draft')