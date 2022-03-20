import os
from queue import Empty
from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user
from numpy import empty
from journal_platform import db, app
from journal_platform.models import Article, User, ArticleComment, Photo, Video
from journal_platform.articles.forms import NewArticleForm
from journal_platform.comments.forms import ArticleCommentForm
from werkzeug.utils import secure_filename

articles = Blueprint('articles', __name__)


@articles.route("/articles/new", methods=['GET', 'POST'])
def new():
    if not current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = NewArticleForm()

    if request.form.get('post'):
        article = Article(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(article)
        db.session.flush()

        # FIXME: photos and videos use the same code.

        photos = request.files.getlist('photos')
        if photos:
            for photo in photos:
                photo_filename = secure_filename(photo.filename)
                photo.save(os.path.join(app.root_path, 'static', photo_filename))
                new_photo = Photo(name=photo_filename, article_id=article.id)
                db.session.add(new_photo)
                db.session.flush()

        videos = request.files.getlist('videos')
        if videos:
            for video in videos:
                video_filename = secure_filename(video.filename)
                video.save(os.path.join(app.root_path, 'static', video_filename))
                new_video = Video(name=video_filename, article_id=article.id)
                db.session.add(new_video)
                db.session.flush()

        db.session.commit()
        return redirect(url_for("main.index"))
    elif request.form.get('draft'):
        # TODO: save article to drafts
        return redirect(url_for("articles.new"))

    return render_template("articles/new.html", form=form)

@articles.route("/articles/<int:article_id>", methods=['GET', 'POST'])
def article(article_id):
    article = Article.query.filter_by(id=article_id).first()
    user = User.query.filter_by(id=article.user_id).first()
    user_articles = Article.query.filter_by(user_id=user.id).order_by(Article.date_posted.desc())
    other_articles = Article.query.order_by(Article.date_posted.desc())
    article_comments = ArticleComment.query.filter_by(article_id=article.id).order_by(ArticleComment.date_posted.desc())
    form = ArticleCommentForm()

    if form.validate_on_submit():
        article_comment = ArticleComment(content=form.content.data, user_id=current_user.id, article_id=article.id)
        db.session.add(article_comment)
        db.session.commit()
        return redirect(url_for("articles.article", article_id=article_id))

    return render_template("articles/article.html", article=article, user=user, user_articles=user_articles, other_articles=other_articles, form=form, User=User, article_comments=article_comments)
