from flask import Flask
from octocd.controllers.build import build


def create_app():
    """Initializes flask app

    Creates the app using a flask application factory.

    Returns:
        Instance of a flask application

    """

    app = Flask(__name__)

    app.register_blueprint(build, url_prefix='/build')

    return app
