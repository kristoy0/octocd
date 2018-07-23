from flask import Flask
from octocd.controllers.main import main


def create_app():
    """Initializes flask app

    Creates the app using a flask application factory.

    Returns:
        Instance of a flask application

    """

    app = Flask(__name__)

    app.register_blueprint(main)

    return app
