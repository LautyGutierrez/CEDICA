import os
from src.core import database
from flask import Flask
from flask_session import Session
from src.core import config, cors, csrf,google
from src.web import controllers
from src.core.auth import user
from src.web.storage import storage
from flask_cors import CORS
from src.web.controllers import _helpers as h
session = Session()


def create_app(env: str = "development", static_folder: str = "../../static"):
    app = Flask(
        __name__, static_folder=static_folder, template_folder="./templates"
    )
    app.config['GOOGLE_CLIENT_ID'] = os.getenv("GOOGLE_CLIENT_ID")
    app.config['GOOGLE_CLIENT_SECRET'] = os.getenv("GOOGLE_CLIENT_SECRET")
    app.config['CAPTCHA_SECRET_KEY']  =os.getenv("CAPTCHA_SECRET_KEY")
    config.init_app(app, env)
    google.init_app(app)
    storage.init_app(app)
    csrf.init_app(app)
    CORS(app)
    cors.init_app(app)
    session.init_app(app)
    database.init_app(app)
    controllers.init_app(app)
    app.jinja_env.globals.update(archivo_url=h.archivo_url)
    register_cli_commands(app)

    return app


def register_cli_commands(app: Flask) -> None:
    """Register CLI commands for database management."""

    @app.cli.command("reset-db")
    def reset_db():
        """Clear all tables and create them again."""
        database.reset_db()
        print("Database has been reset.")

    @app.cli.command("reset-db-dev")
    def reset_db_dev():
        """
        Drops all tables, creates them again, and seeds the database.
        Also loads test data for development.
        """
        from src.core import seed, seed_dev

        database.reset_db()
        seed.seed_db()
        seed_dev.seed_db()
        print("Development database has been reset and seeded.")

    @app.cli.command("seed-db")
    def seed_db():
        """Seed the database with initial data."""
        from src.core import seed

        seed.seed_db()
        print("Database has been seeded with initial data.")

    @app.cli.command("seed-db-dev")
    def seed_db_dev():
        """Load test data for development."""
        from src.core import seed_dev

        seed_dev.seed_db()
        print("Development data has been seeded.")
