from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = "1234"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

UPLOAD_FOLDER = app.root_path + "/static"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

socketio = SocketIO(app)


from journal_platform.main.routes import main
from journal_platform.users.routes import users
from journal_platform.video.routes import video
from journal_platform.articles.routes import articles
from journal_platform.chats.routes import chats
app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(video)
app.register_blueprint(articles)
app.register_blueprint(chats)


def create_app():
    return app
