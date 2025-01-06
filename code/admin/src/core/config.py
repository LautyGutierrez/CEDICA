import os
import typing as t
from dotenv import load_dotenv
from flask import Flask


class ConfigurationError(Exception):
    pass


def env_or_error(env: str, default: t.Union[str, None] = None) -> str:
    """
    Get the value of an environment variable or raise an error if it is not set.

    Args:
        env (str): The name of the environment variable.
        default (Union[str, None]): The default value if the environment variable is not set.

    Returns:
        str: The value of the environment variable.

    Raises:
        ConfigurationError: If the environment variable is not set and no default value is provided.
    """
    value = os.getenv(env, default)
    if value is None:
        raise ConfigurationError(f"Environment variable '{env}' not set")
    return value


class DevelopmentConfig:
    # SQLAlcemy configuration
    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool

    # WTForm config
    WTF_CSRF_ENABLED: bool
    WTF_CSRF_SECRET_KEY: str
    WTF_CSRF_CHECK_DEFAULT: bool

    # Flask configuration
    SECRET_KEY: str

    # Flask session configuration
    SESSION_TYPE: str

    # Flask-JWT-Extended configuration
    JWT_SECRET_KEY: str
    JWT_TOKEN_LOCATION: t.List[str]
    JWT_HEADER_NAME: str
    JWT_ERROR_MESSAGE_KEY: str
    # Minio configuration
    MINIO_SERVER: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SECURE: bool
    MINIO_BUCKET_NAME = str
    MINIO_BASE_URL = str

    @classmethod
    def load_env_config(cls) -> "DevelopmentConfig":
        """
        Load configuration from environment variables.
        """
        load_dotenv()

        config = cls()

        DB_USER = env_or_error('DB_USER')
        DB_PASS = env_or_error('DB_PASS')
        DB_HOST = os.getenv('DB_HOST', 'localhost')  # Default to localhost
        DB_PORT = os.getenv('DB_PORT', '5432')  # Default to 5432
        DB_NAME = env_or_error('DB_NAME')

        # Construir la URL de la base de datos
        config.SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        config.SQLALCHEMY_TRACK_MODIFICATIONS = True

        config.SECRET_KEY = env_or_error("SECRET_KEY")
        config.WTF_CSRF_CHECK_DEFAULT = (env_or_error(
            "WTF_CSRF_CHECK_DEFAULT", "true").lower() == "true")
        config.WTF_CSRF_ENABLED = (env_or_error(
            "WTF_CSRF_ENABLED", "true").lower() == "true")
        config.WTF_CSRF_SECRET_KEY = env_or_error("WTF_CSRF_SECRET_KEY")

        config.SESSION_TYPE = env_or_error("SESSION_TYPE", "filesystem")

        config.JWT_SECRET_KEY = env_or_error("JWT_SECRET_KEY")
        config.JWT_HEADER_NAME = env_or_error("JWT_HEADER_NAME", "JWT")
        config.JWT_TOKEN_LOCATION = env_or_error(
            "JWT_TOKEN_LOCATION", "headers").split(",")
        config.JWT_ERROR_MESSAGE_KEY = env_or_error(
            "JWT_ERROR_MESSAGE_KEY", "jwt_error_message")
        config.MINIO_SERVER = "localhost:9000"
        config.MINIO_ACCESS_KEY = "CpiansPCNyGfpxsVQEok"
        config.MINIO_SECRET_KEY = "z4Ew1WDcoK95Fx006KZ2L4JwJuwawFKgtBCR8fFI"
        config.MINIO_SECURE = False
        config.MINIO_BUCKET_NAME = "grupo21"
        config.MINIO_BASE_URL = "http://localhost:9001/browser"
        return config


class ProductionConfig:

    SECRET_KEY = "1dd6e340982e8b0c134bc18d456d839593cd9d8e408893ac"
    WTF_CSRF_SECRET_KEY = "8aecd43bb78f6e554eefeb0ff88a0d97c566b3f1c8f8a7b4"
    JWT_SECRET_KEY = "69fdc82d286e1ab59d45f1d687d966e960067f423c941457"
    WTF_CSRF_CHECK_DEFAULT = "true"
    WTF_CSRF_ENABLED = "true"
    SESSION_TYPE = "filesystem"
    JWT_HEADER_NAME = "JWT"
    JWT_TOKEN_LOCATION = "headers"
    JWT_ERROR_MESSAGE_KEY = "jwt_error_message"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MINIO_SECURE = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }

    @classmethod
    def load_env_config(cls) -> "ProductionConfig":
        """
        Load configuration from environment variables.
        """

        config = cls()

        config.MINIO_SERVER = os.environ.get("MINIO_SERVER")
        config.MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
        config.MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
        config.MINIO_BUCKET_NAME = os.environ.get("MINIO_BUCKET_NAME")
        config.SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
        return config


def init_app(app: Flask, env: str) -> None:
    """
    Initialize the Flask app with the configuration.
    """

    config_env = ProductionConfig.load_env_config()
    #config_env = DevelopmentConfig.load_env_config()

    app.config.from_object(config_env)


def main():
    app = Flask(__name__)
    env = os.getenv("FLASK_ENV", "development")
    init_app(app, env)
    app.run(debug=(env == "development"))


if __name__ == "__main__":
    main()
