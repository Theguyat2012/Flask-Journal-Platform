from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ArticleCommentForm(FlaskForm):
    content = StringField('Comment here...', validators=[DataRequired()])
    submit = SubmitField('Comment')
