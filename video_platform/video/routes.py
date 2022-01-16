from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user
from flask_wtf import form
from video_platform import db
import video_platform
from video_platform.models import Video
from video_platform.video.forms import VideoForm

video = Blueprint('video', __name__)


@video.route('/upload', methods=['GET', 'POST'])
def upload():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))

    form = VideoForm()
    if form.validate_on_submit():
        video = Video(title=form.title.data, description=form.description.data, file=form.video.data.filename, user_id=current_user.id)
        db.session.add(video)
        db.session.commit()
        print(video)
        return redirect(url_for('video.upload'))

    return render_template('video/upload.html', form=form)
