import typing as t
from functools import wraps
import flask
from flask import typing as tf
from flask import current_app


def flash_info(message: str) -> None:
    """Flashes an info message.

    Args:
        message (str): The message to flash

    """
    flask.flash(message, "info")


def flash_success(message: str) -> None:
    """Flashes a success message.

    Args:
        message (str): The message to flash

    """
    flask.flash(message, "success")


def flash_warning(message: str) -> None:
    """Flashes a warning message.

    Args:

        message (str): The message to flash

    """
    flask.flash(message, "warning")


def flash_error(message: str) -> None:
    """Flashes an error message.

    Args:
        message (str): The message to flash

    """
    flask.flash(message, "error")


TRoute = t.TypeVar("TRoute", bound=t.Callable[..., t.Any])


def require_session(message: t.Union[str, t.Literal[False]] = "Debes iniciar sesion para acceder",) -> t.Callable[[TRoute], TRoute]:
    """Decorator that requires a session to access the route.	
    Args:
        message (Union[str, Literal[False]], optional): The message to show if the user is not logged in. Defaults to "Debes iniciar sesion para acceder".

    Returns:
        Callable[[TRoute], TRoute]: The decorated function
    """

    def decorator(func: TRoute) -> TRoute:
        """The decorator function.
        Args:
            func (TRoute): The route function

        Returns:
            TRoute: The decorated function
        """
        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> tf.ResponseReturnValue:
            if flask.session.get("user_id") is None:
                if message:
                    flash_info(message)

                return flask.redirect("/login")

            return func(*args, **kwargs)

        return wrapper  # pyright: ignore[reportReturnType]

    return decorator


def require_no_session(message: t.Union[str, t.Literal[False]] = "",) -> t.Callable[[TRoute], TRoute]:
    """Decorator that requires no session to access the route.
    Args:
        message (Union[str, Literal[False]], optional): The message to show if the user is logged in. Defaults to "".

    Returns:

        Callable[[TRoute], TRoute]: The decorated function
    """
    def decorator(func: TRoute) -> TRoute:
        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> tf.ResponseReturnValue:
            if flask.session.get("user_id") is not None:
                if message:
                    flash_info(message)

                return flask.redirect("/")

            return func(*args, **kwargs)

        return wrapper  # pyright: ignore[reportReturnType]

    return decorator


def authenticated_route(module: str = "", permissions: t.Tuple[str, ...] = tuple(),) -> t.Callable[[TRoute], TRoute]:
    """Decorator that requires the user to be authenticated to access the route.
    Args:
        module (str, optional): The module of the route. Defaults to "".
        permissions (Tuple[str, ...], optional): The permissions required to access the route. Defaults to tuple().

    Returns:
        Callable[[TRoute], TRoute]: The decorated function
    """

    _permissions = tuple(
        f"{module}_{permission}" for permission in permissions
    )

    def has_permissions(required: t.Tuple[str, ...]) -> bool:
        """Checks if the user has the given permissions.
        Args:
            required (Tuple[str, ...]): The permissions to check

        Returns:
            bool: True if the user has all the permissions, False otherwise
        """
        user_permissions: t.Tuple[str, ...] = (
            flask.g.user_permissions or tuple())
        return all(
            required_permission in user_permissions
            for required_permission in required
        )

    def decorator(func: TRoute) -> TRoute:
        """The decorator function.

        Args:
            func (TRoute): The route function

        Returns:
            TRoute: The decorated function
        """

        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> tf.ResponseReturnValue:
            if flask.g.user is None:
                return flask.redirect("/login")

            if not flask.g.user.is_active and not has_permissions(("usuario_update",)):
                return flask.redirect("/account_disabled")

            flask.g.user_has_permissions = has_permissions

            if not has_permissions(_permissions):
                return flask.redirect("/")

            return func(*args, **kwargs)

        return wrapper  # pyright: ignore[reportReturnType]

    return decorator


def url_pagination_args(
    default_page: int = 1,
    default_per_page: int = 10,
    max_per_page: int = 100,
):
    """Extracts pagination arguments from the request URL.

    Args:
        default_page (int, optional): The default page. Defaults to 1.
        default_per_page (int, optional): The default results per page. Defaults to 10.
        max_per_page (int, optional): The maximum results per page. Defaults to 100.

    Returns:    
        Tuple[int, int]: The page and results per page
    """
    arg_page = flask.request.args.get("page", "")
    arg_per_page = flask.request.args.get("per_page", "")

    page = int(arg_page) if arg_page.isdigit() else default_page
    per_page = (
        int(arg_per_page) if arg_per_page.isdigit() else default_per_page
    )

    page = page if page > 0 else default_page
    per_page = per_page if 0 < per_page <= max_per_page else default_per_page

    return page, per_page


"""MINIO CONFIGURATION"""


def archivo_url(archivo):
    """Genera la URL de un archivo en Minio.

    Args:
        archivo: str | None

    Returns:
        str: La URL del archivo
    """
    client = current_app.storage.client
    if archivo is None:
        return "-"
    return client.presigned_get_object("grupo21", archivo)
