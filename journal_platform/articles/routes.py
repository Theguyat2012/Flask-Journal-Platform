from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user
from journal_platform import db
from journal_platform.models import Article, User
from journal_platform.articles.forms import NewArticleForm

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

@articles.route("/articles/<int:article_id>")
def article(article_id):
    article = Article.query.filter_by(id=article_id).first()
    user = User.query.filter_by(id=article.user_id).first()
    return render_template("articles/article.html", article=article, user=user)
