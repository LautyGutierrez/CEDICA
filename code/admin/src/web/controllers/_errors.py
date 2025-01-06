import flask
from sqlalchemy import exc as sqlalchemy_exc
from werkzeug import exceptions


import src.web.controllers.api.base as api_base


def handle_forbidden_error(e: exceptions.Forbidden):
    """Handles the Forbidden error.

    Args:
        e: exceptions.Forbidden
            The exception to handle

    Returns:
        tuple: The response and status code

    """
    return (
        flask.render_template(
            "_errors/default.html",
            error_code="403",
            error_title="Acceso denegado",
            error_message="No tienes permisos para acceder a esta página",
        ),
        403,
    )


def handle_not_found_error(e: exceptions.NotFound):
    """Handles the Not Found error.	

    Args:
        e: exceptions.NotFound

    Returns:
        tuple: The response and status code

    """
    if flask.request.path.startswith("/api"):
        return api_base.API_NOT_FOUND_RESPONSE

    return (
        flask.render_template("_errors/404.html"),
        404,
    )


def handle_method_not_allowed_error(e: exceptions.MethodNotAllowed):
    """Handles the Method Not Allowed error.

    Args:
        e: exceptions.MethodNotAllowed

    Returns:
        tuple: The response and status code

    """
    if flask.request.path.startswith("/api"):
        return api_base.API_METHOD_NOT_ALLOWED_RESPONSE

    return (
        flask.render_template(
            "_errors/default.html",
            error_code="405",
            error_title="Método http no permitido",
            error_message=f"El método \
                {flask.request.method} no está permitido en esta página",
        ),
        405,
    )


def handle_sqlalchemy_error(e: sqlalchemy_exc.SQLAlchemyError):
    """Handles the SQLAlchemy error.

    Args:
        e: sqlalchemy_exc.SQLAlchemyError

    Returns:
        tuple: The response and status code

    """
    return (
        flask.render_template(
            "_errors/500.html",
            error_code="500",
            error_title="Error interno del servidor",
            error_message=f"Se ha producido un error inesperado \
                con la base de datos{(', ' + e.code) if e.code else ''}",
        ),
        500,
    )


def handle_internal_server_error(e: exceptions.InternalServerError):
    """Handles the Internal Server error.

    Args:
        e: exceptions.InternalServerError

    Returns:
        tuple: The response and status code

    """

    error_code = 500 if e.code is None else e.code
    error_message = "Se ha producido un error inesperado"
    if (
        e.original_exception
        and hasattr(e.original_exception, "message")
        and isinstance(e.original_exception.message, str)  # type: ignore
        and len(e.original_exception.message) > 0  # type: ignore
    ):
        error_message = e.original_exception.message  # type: ignore

    return (
        flask.render_template(
            "_errors/500.html",
            error_code=error_code,
            error_message=error_message,
        ),
        error_code,
    )


def register_error_handlers(app: flask.Flask) -> None:
    """Registers the error handlers for the application.

    Args:
        app: flask.Flask
            The application instance

    """

    app.register_error_handler(exceptions.NotFound, handle_not_found_error)

    app.register_error_handler(exceptions.Forbidden, handle_forbidden_error)

    app.register_error_handler(
        exceptions.MethodNotAllowed, handle_method_not_allowed_error
    )

    app.register_error_handler(
        api_base.BaseAPIError, api_base.handle_api_error
    )

    app.register_error_handler(
        sqlalchemy_exc.SQLAlchemyError, handle_sqlalchemy_error
    )

    app.register_error_handler(
        exceptions.InternalServerError, handle_internal_server_error
    )
