from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user
from flask_wtf import form
from video_platform.video.forms import VideoForm

video = Blueprint('video', __name__)


@video.route('/upload', methods=['GET', 'POST'])
def upload():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))

    form = VideoForm()
    return render_template('video/upload.html', form=form)
