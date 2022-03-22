from flask_wtf import FlaskForm
from wtforms.fields import MultipleFileField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class MultipleFileAllowed(object):
    def __init__(self, extensions, message=None):
        self.extensions = extensions
        self.message = message
        if not message:
            message = "File must have " + extensions + " extensions."

    def __call__(self, form, field):
        files = []

        for data in field.data:
            if len(data.filename.split('.')) > 1:
                if data.filename.split('.')[1].lower() in self.extensions:
                    files.append(data)
                else:
                    raise ValidationError(self.message)

        return files

class NewArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content')
    photos = MultipleFileField('Photos', validators=[MultipleFileAllowed(['jpg', 'png'], 'Images only!')])
    videos = MultipleFileField('Videos', validators=[MultipleFileAllowed(['mp4', 'web', 'ogg'], 'Videos only!')])
    post = SubmitField('Post')
    draft = SubmitField('Draft')
