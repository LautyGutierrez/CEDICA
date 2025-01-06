from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    session,
)
from src.web.controllers import _helpers as h
from src.web.forms.contentForm import ContentForm
from src.web.forms.validators import formulario_valido, texto_con_signos
from src.core.content import ContentService

bp = Blueprint("content", __name__, url_prefix="/content")


required_fields = ["titulo", "resumen", "texto"]

validation_rules = {
    "titulo": texto_con_signos,
    "resumen": texto_con_signos,
    "texto": texto_con_signos,
}


@bp.get("/")
@h.authenticated_route(
    module="contenido",
    permissions=(
        "index",
        "show",
    ),
)
def show_contents():
    """
    Renderiza la página principal de contenido, mostrando todos los contenidos de forma paginada y filtrada (si aplica), con las operaciones CRUD.

    Returns:
        render_template
            Renderiza el HTML index del módulo contenido.
    """
    state: str = request.args.get("filterSelect", "")
    filter_input: str = request.args.get("filter_input", "")
    page, per_page = h.url_pagination_args(default_per_page=8)
    contents, total = ContentService.all_contents(
        page=page, per_page=per_page, state=state, filter_input=filter_input
    )
    return render_template(
        "content/index.html",
        contents=contents,
        total=total,
        page=page,
        per_page=per_page,
        state=state,
        filter_input=filter_input,
    )


@bp.get("/create")
@h.authenticated_route(module="contenido", permissions=("create",))
def create_content():
    """
    Renderiza el formulario para crear un nuevo contenido.

    Returns:
        render_template:
            Renderiza el HTML del formulario para crear un nuevo contenido.
    """
    form = ContentForm()
    return render_template("content/create.html", form=form)


@bp.post("/create")
@h.authenticated_route(module="contenido", permissions=("create",))
def create_content_post():
    """
    Registra a un nuevo contenido en la base de datos.

    Returns:
        redirect:
            Redirecciona a la página donde se muestran los contenidos si el contenido fue creado exitosamente.
            Redirecciona al formulario de creación de contenido si hubo un error en la creación.

    Raises:
        Exception:
            Si hubo un error al crear el contenido.

    Errores:
        Faltan campos requeridos:
            Si no se ingresaron todos los campos requeridos.
        Campo con error:
            Si hubo un error con un campo ingresado.
        Error al crear contenido:
            Si hubo un error al crear el contenido en la base de datos.
    """
    params = request.form
    missing_fields = [field for field in required_fields if not params.get(field)]

    if missing_fields:
        h.flash_errors(f"Faltan campos requeridos")
        return redirect(url_for("content.create_content"))

    content_data = {
        "title": params.get("titulo"),
        "summary": params.get("resumen"),
        "content_text": params.get("texto"),
    }

    ok, errors = formulario_valido(params, validation_rules)

    if not ok:
        for field, error_list in errors.items():
            for error in error_list:
                h.flash_error(f"El campo {field} tiene un error: {error}")
                break
        return redirect(url_for("content.create_content"))

    form = ContentForm(data=content_data)
    if not form.validate_on_submit():
        h.flash_errors(f"Error con la información ingresada")
        return redirect(url_for("content.create_content"))

    try:
        user_id = session["user_id"]
        content = ContentService.create_content(user_id, **content_data)
        h.flash_success(f"Contenido creado exitosamente!")
    except Exception as e:
        print(e)
        h.flash_error(f"Error al crear contenido")
        return redirect(url_for("content.create_content"))

    return redirect(url_for("content.show_contents"))


@bp.post("/changeStatus/<int:content_id>")
@h.authenticated_route(module="contenido", permissions=("update",))
def change_status(content_id: int):
    """
    Cambia el estado de un contenido.
    Si el contenido estaba en estado borrador, lo cambia a publicado.
    Si el contenido estaba en estado publicado, lo cambia a archivado.
    Si el contenido estaba en estado archivado, lo cambia a publicado.

    Args:
        content_id: int
            ID del contenido a cambiar de estado.

    Returns:
        redirect:
            Redirecciona a la página donde se muestran los contenidos si el estado del contenido fue cambiado exitosamente o si hubo un error al cambiar el estado.

    Errors:
        No se pudo cambiar el estado del contenido:
            Si hubo un error al cambiar el estado del contenido.
    """
    change: bool = ContentService.change_status(content_id)
    if not change:
        h.flash_error("No se pudo cambiar el estado del contenido")
    else:
        h.flash_success("Estado del contenido cambiado exitosamente!")
    return redirect(url_for("content.show_contents"))


@bp.post("/delete/<int:content_id>")
@h.authenticated_route(module="contenido", permissions=("destroy",))
def delete_content(content_id: int):
    """
    Elimina lógicamente un contenido de la base de datos.

    Args:
        content_id: int
            ID del contenido a eliminar.

    Returns:
        redirect:
            Redirecciona a la página donde se muestran los contenidos si el contenido fue eliminado exitosamente o si hubo un error al eliminar el contenido.

    Errors:
        No se pudo eliminar el contenido:
            Si hubo un error al eliminar el contenido.

    Raises:
        Exception:
            Si hubo un error al eliminar el contenido.
    """
    try:
        ContentService.delete(content_id)
        h.flash_success("Contenido eliminado exitosamente!")
    except Exception as e:
        print(e)
        h.flash_error("No se pudo eliminar el contenido")
    return redirect(url_for("content.show_contents"))


@bp.get("/<int:content_id>")
@h.authenticated_route(
    module="contenido",
    permissions=(
        "show",
        "update",
    ),
)
def edit_content(content_id: int):
    """
    Renderiza el formulario para editar un contenido, con los campos pre-cargados con la información del contenido.

    Args:
        content_id: int
            ID del contenido a editar.

    Returns:
        redirect:
            Redirecciona a la página donde se muestran los contenidos si el contenido no existe.
        render_template:
            Renderiza el HTML del formulario para editar un contenido.
    """
    content = ContentService.get_content(content_id)
    if not content:
        h.flash_error("Contenido no encontrado")
        return redirect(url_for("content.show_contents"))

    form = ContentForm(
        titulo=content.title,
        resumen=content.summary,
        texto=content.content_text,
    )

    return render_template("content/edit.html", form=form, content=content)


@bp.post("/<int:content_id>")
@h.authenticated_route(
    module="contenido",
    permissions=(
        "show",
        "update",
    ),
)
def edit_content_post(content_id: int):
    """
    Edita la información de un contenido.

    Args:
        content_id: int
            ID del contenido a editar.

    Returns:
        redirect:
            Redirecciona a la página donde se muestran los contenidos si el contenido fue editado exitosamente.
            Redirecciona al formulario de edición de contenido si hubo un error en la edición.

    Errors:
        Faltan campos requeridos:
            Si no se ingresaron todos los campos requeridos.
        Campo con error:
            Si hubo un error con un campo ingresado.
        No se pudo editar el contenido:
            Si hubo un error al editar el contenido en la base de datos.

    Raises:
        Exception:
            Si hubo un error al editar el contenido.
    """
    params = request.form
    missing_fields = [field for field in required_fields if not params.get(field)]

    if missing_fields:
        h.flash_errors(f"Faltan campos requeridos")
        return redirect(url_for("content.edit_content", content_id=content_id))

    ok, errors = formulario_valido(params, validation_rules)

    if not ok:
        for field, error_list in errors.items():
            for error in error_list:
                h.flash_error(f"El campo {field} tiene un error: {error}")
                break
        return redirect(url_for("content.edit_content", content_id=content_id))

    content_data = {
        "title": params.get("titulo"),
        "summary": params.get("resumen"),
        "content_text": params.get("texto"),
    }
    try:
        ContentService.edit_content(content_id, content_data)
        h.flash_success("Contenido editado exitosamente!")
    except Exception as e:
        print(e)
        h.flash_error("No se pudo editar el contenido")
        return redirect(url_for("content.edit_content", content_id=content_id))

    return redirect(url_for("content.show_contents"))

