import os
import random
from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user
from flask_wtf import form
from werkzeug.utils import secure_filename
from PIL import Image
from video_platform import db, app
from video_platform.models import Video
from video_platform.video.forms import VideoForm

video = Blueprint('video', __name__)


@video.route('/upload', methods=['GET', 'POST'])
def upload():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))

    form = VideoForm()
    if form.validate_on_submit():
        video_filename = secure_filename(form.video.data.filename)
        video_file = form.video.data
        video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))

        # Create video thumbnail
        thumbnail = ''

        video = Video(title=form.title.data, description=form.description.data, video=video_filename, thumbnail=thumbnail, user_id=current_user.id)
        db.session.add(video)
        db.session.commit()

        return redirect(url_for('video.upload'))

    return render_template('video/upload.html', form=form)

@video.route('/video/<int:video_id>')
def watch(video_id):
    video = Video.query.filter_by(id=video_id).first()
    return render_template('video/watch.html', video=video)
