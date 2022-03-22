import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from journal_platform import app, db
from journal_platform.models import User, Article
from journal_platform.users.forms import RegisterForm, LoginForm, EditForm, FollowForm

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        flash('Account registered!', 'success')
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("users.login"))

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
    flash("Logged out of " + current_user.username + ".", 'danger')
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/users/<username>', methods=['GET', 'POST'])
def profile(username):
    user = User.query.filter_by(username=username).first()
    articles = Article.query.order_by(Article.date_posted.desc()).filter_by(user_id=user.id)

    follow_form = FollowForm()
    if request.form.get('submit'):
        if not current_user.is_following(user):
            current_user.follow(user)
            db.session.commit()
        else:
            current_user.unfollow(user)
            db.session.commit()
        return redirect(url_for('users.profile', username=username))

    return render_template('users/profile.html', user=user, articles=articles, follow_form=follow_form)

@users.route('/users/<username>/edit', methods=['GET', 'POST'])
def edit(username):
    if current_user.is_authenticated:
        user = User.query.filter_by(username=username).first()
        if current_user == user:
            form = EditForm()
            if form.validate_on_submit():
                current_user.username = form.username.data
                current_user.email = form.email.data

                if form.image.data:
                    current_user.save_image(form.image)
                else:
                    os.remove(os.path.join(app.root_path, 'static', current_user.image))
                    current_user.image = "default.jpg"

                db.session.commit()
                return redirect(url_for('users.profile', user=user, username=current_user.username))

            return render_template('users/edit.html', user=user, form=form)
        else:
            return redirect(url_for('users.profile', user=user, username=username))
    else:
        return redirect(url_for('users.login'))
