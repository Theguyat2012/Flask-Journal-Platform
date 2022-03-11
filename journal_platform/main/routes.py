from flask import Blueprint, render_template
from journal_platform.models import Article, User

main = Blueprint('main', __name__)


@main.route("/")
def index():
    articles = Article.query.order_by(Article.date_posted.desc()).all()
    return render_template('main/index.html', articles=articles, User=User)
