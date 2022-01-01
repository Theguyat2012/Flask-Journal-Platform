from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "1234"

    db.init_app(app)

    from video_platform.main.routes import main
    from video_platform.users.routes import users
    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
