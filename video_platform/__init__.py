from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = "1234"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'video_platform/static/'
db = SQLAlchemy(app)
login_manager = LoginManager(app)


from video_platform.main.routes import main
from video_platform.users.routes import users
from video_platform.video.routes import video
app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(video)


def create_app():
    return app
