from flask import Blueprint, render_template
from journal_platform.models import Video

main = Blueprint('main', __name__)


@main.route("/")
def index():
    videos = Video.query.all()
    return render_template('main/index.html', videos=videos)
