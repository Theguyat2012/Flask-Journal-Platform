import os
from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user
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

        article.save_multiple_files(form.photos, Photo, article.id)
        article.save_multiple_files(form.videos, Video, article.id)

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
