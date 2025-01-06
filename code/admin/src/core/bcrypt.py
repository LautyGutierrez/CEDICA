from flask import Flask
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def init_app(app: Flask):
    """Initializes the bcrypt for the application.

    Args:
        app: Flask
            The application instance
    """
    bcrypt.init_app(app)
