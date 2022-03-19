from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = "1234"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)


from journal_platform.main.routes import main
from journal_platform.users.routes import users
from journal_platform.video.routes import video
from journal_platform.articles.routes import articles
app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(video)
app.register_blueprint(articles)


def create_app():
    return app
