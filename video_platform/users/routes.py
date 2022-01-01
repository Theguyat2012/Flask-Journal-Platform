from flask import Blueprint, render_template
from video_platform.users.forms import RegisterForm

users = Blueprint('users', __name__)


@users.route('/register')
def register():
    form = RegisterForm()
    return render_template('users/register.html', form=form)