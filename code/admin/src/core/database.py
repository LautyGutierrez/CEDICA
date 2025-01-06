import typing as t
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app: Flask) -> None:
    """
        Initialize the database with the app

    """
    db.init_app(app)
    config_db(app)


def config_db(app: Flask) -> None:
    """
        Configure the database with the app

    """

    @app.teardown_request
    def close_db_session(exception: t.Union[BaseException, None] = None) -> None:
        db.session.close()


def reset_db() -> None:
    """Reset the database"""
    db.drop_all()
    db.create_all()
