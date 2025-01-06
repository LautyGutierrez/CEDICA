from flask import Flask
from flask_wtf.csrf import CSRFProtect
from web.controllers.api import contact

csrf = CSRFProtect()


def init_app(app: Flask) -> None:
    """Initializes the CSRF protection for the application.

    Args:
        app: Flask
            The application instance
    """
    csrf.init_app(app)
    from web.controllers.api import contact
    csrf.exempt(contact.bp) 
