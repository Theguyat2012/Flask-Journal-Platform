import os, string, random
from sqlalchemy import ForeignKey
from journal_platform import app, db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.utils import secure_filename


@login_manager.user_loader
def load_user(user):
    return User.query.get(user)

followers = db.Table('followers', db.Column('follower_id', db.Integer, db.ForeignKey('user.id')), db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))
chat_users = db.Table('chat_users', db.Column('user_id', db.ForeignKey('user.id'), primary_key=True), db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'), primary_key=True))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False, default="default.jpg")
    articles = db.relationship('Article', backref='author', lazy=True)
    comments = db.relationship('ArticleComment', backref='author', lazy=True)
    followed = db.relationship('User', secondary=followers, primaryjoin=(followers.c.follower_id == id), secondaryjoin=(followers.c.followed_id == id), backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    messages = db.relationship('Message', backref='author', lazy=True)

    def save_image(self, form_image):
        image_file = form_image.data
        image_file_extension = form_image.data.filename.split('.')[1]
        image_filename = secure_filename(''.join(random.choices(string.ascii_letters + string.digits, k = 64)) + '.' + image_file_extension)

        if (os.path.exists(os.path.join(app.root_path, 'static', image_filename))):
            self.save_image(form_image)
        else:
            image_file.save(os.path.join(app.root_path, 'static', image_filename))
            if self.image != "default.jpg":
                os.remove(os.path.join(app.root_path, 'static', self.image))
            self.image = image_filename

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
    
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO: Differentiate drafts from published articles somehow
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(15000), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('ArticleComment', backref='article', lazy=True)
    photos = db.relationship('Photo', backref='article', lazy=True)
    videos = db.relationship('Video', backref='article', lazy=True)

    def save_multiple_files(self, form_object, object_class):
        for object in form_object.data:
            filename = secure_filename(object.filename)
            if filename:
                object.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new_object = object_class(name=filename, article_id=self.id)
                db.session.add(new_object)
                db.session.flush()


class ArticleComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Message', backref='chat', lazy=True)
    chat_users = db.relationship('User', secondary=chat_users, lazy='dynamic', backref=db.backref('chats', lazy='dynamic'))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
