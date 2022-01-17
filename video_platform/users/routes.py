from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from video_platform import db
from video_platform.models import User
from video_platform.users.forms import RegisterForm, LoginForm

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
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
            return redirect(url_for('main.index'))

    return render_template('users/login.html', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/users/<username>')
def profile(username):
    videos = User.query.filter_by(username=username).first().videos
    return render_template('users/profile.html', videos=videos)

@users.route('/users/<username>/update')
def update(username):
    return render_template('users/update.html')
