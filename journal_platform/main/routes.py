from flask import Blueprint, render_template
from flask_login import current_user
from sqlalchemy.orm import sessionmaker
from journal_platform.models import Article, User

main = Blueprint('main', __name__)


@main.route("/")
def index():
    articles = Article.query.order_by(Article.date_posted.desc()).all()

    followed_articles = []
    if current_user.is_authenticated:
        followed_ids = []
        for followed in current_user.followed.all():
            followed_ids.append(followed.id)
        followed_articles = Article.query.filter(Article.user_id.in_(followed_ids)).order_by(Article.date_posted.desc())

    return render_template('main/index.html', articles=articles, User=User, Article=Article, followed_articles=followed_articles)
