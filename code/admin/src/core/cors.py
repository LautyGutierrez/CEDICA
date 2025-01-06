from flask import Flask
from flask_cors import CORS

cors: CORS


def init_app(app: Flask) -> None:
    """Initializes the CORS for the application.

    Args:
        app: Flask
            The application instance   
    """

    global cors
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
