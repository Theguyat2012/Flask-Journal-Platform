from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user
from journal_platform import db
from journal_platform.models import Article, User, ArticleComment
from journal_platform.articles.forms import NewArticleForm
from journal_platform.comments.forms import ArticleCommentForm

articles = Blueprint('articles', __name__)


@articles.route("/articles/new", methods=['GET', 'POST'])
def new():
    if not current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = NewArticleForm()

    if request.form.get('post'):
        article = Article(title=request.form['title'], content=request.form['content'], user_id=current_user.id)
        db.session.add(article)
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
    article_comments = ArticleComment.query.filter_by(article_id=article.id).order_by(ArticleComment.date_posted.desc())
    form = ArticleCommentForm()

    if form.validate_on_submit():
        print('HELLOOOO')
        article_comment = ArticleComment(content=form.content.data, user_id=current_user.id, article_id=article.id)
        db.session.add(article_comment)
        db.session.commit()
        return redirect(url_for("articles.article", article_id=article_id))

    return render_template("articles/article.html", article=article, user=user, form=form, User=User, article_comments=article_comments)
