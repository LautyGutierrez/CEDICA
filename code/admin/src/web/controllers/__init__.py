import typing as t

from core.auth import AuthService
import flask

from src.web.controllers import admin, root, jya, members, payments, ecuestre, cobros, contacto, content, graficos, reportes
from web.controllers.api import articles
from web.controllers.api import contact
_blueprints = (
    admin.bp,
    root.bp,
    jya.bp,
    members.bp,
    ecuestre.bp,
    payments.bp,
    cobros.bp,
    graficos.bp,
    reportes.bp, 
    contacto.bp,
    content.bp,
    articles.bp,
    contact.bp
)


def init_app(app: flask.Flask):
    """Initializes the controllers.

    Registers the blueprints and error handlers for the application.
    Also registers the before request hook for the application.

    Args:
        app: flask.Flask
            The application instance

    """
    from src.web.controllers import _errors

    _errors.register_error_handlers(app)

    for bp in _blueprints:
        app.register_blueprint(bp)

    def user_has_permissions(_: t.Tuple[str, ...]) -> bool:
        """Checks if the user has the given permissions.

        Args:
            _: t.Tuple[str, ...]
                The permissions to check

        Returns:
            bool: True if the user has all the permissions, False otherwise

        """

        return False

    def before_request_hook():
        if flask.request.path.startswith("/static"):
            return None

        flask.g.user = None
        flask.g.user_permissions = tuple()
        flask.g.user_has_permissions = user_has_permissions

        user_id = flask.session.get("user_id")
        if user_id is not None:
            user = AuthService.find_user_by_id(user_id)
            if user is None:
                flask.session.clear()
            else:
                flask.g.user = user
                if user.rol_id != 6:
                    flask.g.user_permissions = AuthService.user_permissions(user.id)

    app.before_request(before_request_hook)
