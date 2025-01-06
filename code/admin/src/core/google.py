from authlib.integrations.flask_client import OAuth
from flask import Flask

oauth = OAuth()


def init_app(app: Flask) -> None:
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={
            'scope': 'openid email profile',
            'prompt': 'consent'
        }
    )