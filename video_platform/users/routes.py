import os
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from video_platform import app, db
from video_platform.models import User
from video_platform.users.forms import RegisterForm, LoginForm, EditForm

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        flash('Account registered!', 'success')
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, image="default.jpg")
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('users/register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash("Logged in as " + current_user.username + "!", 'success')
            return redirect(url_for('main.index'))

    return render_template('users/login.html', form=form)

@users.route('/logout')
@login_required
def logout():
    flash("Logged out" + current_user.username + ".", 'danger')
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/users/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    videos = User.query.filter_by(username=username).first().videos
    return render_template('users/profile.html', user=user, videos=videos)

@users.route('/users/<username>/edit', methods=['GET', 'POST'])
def edit(username):
    if current_user.is_authenticated:
        user = User.query.filter_by(username=username).first()
        if current_user == user:
            form = EditForm()
            if form.validate_on_submit():
                current_user.username = username
                current_user.email = form.email.data

                if form.image.data:
                    # TODO: Save as a random string
                    image_filename = secure_filename(form.image.data.filename)
                    image_file = form.image.data
                    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
                    current_user.image = form.image.data.filename

                db.session.commit()
                return redirect(url_for('users.profile', user=user, username=current_user.username))

            return render_template('users/update.html', user=user, form=form)
        else:
            return redirect(url_for('users.profile', user=user, username=username))
    else:
        return redirect(url_for('users.login'))
