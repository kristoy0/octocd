from flask import Flask

from octocd.controllers.auth import auth
from octocd.controllers.build import build
from octocd.controllers.github import github
from .models import db


def create_app():
    """Initializes flask app

    Creates the app using a flask application factory.

    Returns:
        Instance of a flask application

    """

    app = Flask(__name__)
    app.config.from_object('octocd.config.DevConfig')

    app.register_blueprint(build, url_prefix='/build')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(github, url_prefix='/github')

    db.init_app(app)
    db.create_all(app=app)

    return app
