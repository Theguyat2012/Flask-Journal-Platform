from flask_wtf import FlaskForm
from wtforms import SubmitField


class ChatForm(FlaskForm):
    submit = SubmitField('Chat')
