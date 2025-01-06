from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.contact import ContactoService as c
from src.web.controllers import _helpers as h

from src.web.forms.contactoForm import ContactoEditForm
from src.web.forms.validators import (
    formulario_valido,
    contacto_estado_valido,
    contacto_comentario_valido,
)

bp = Blueprint("contacto", __name__, url_prefix="/contacto")
validation_rules = {
    "estado": contacto_estado_valido,
    "comentario": contacto_comentario_valido,
}


@bp.get("/index")
@h.authenticated_route(module="contacto", permissions=("index",))
def index():
    """
    Muestra la lista de contactos con opciones de filtrado y ordenamiento.

    Args:
        None

    Returns:
        render_template:
            Renderiza la plantilla de listado de contactos con los contactos filtrados y ordenados.
    """
    estado = request.args.get("estado")
    orden = request.args.get("orden", "desc")
    page, per_page = h.url_pagination_args(default_per_page=10)
    if request.args.get("toggle_order"):
        orden = "desc" if orden == "asc" else "asc"

    contactos, total = c.index(estado, orden, page, per_page)
    return render_template(
        "contacto/index.html",
        contactos=contactos,
        page=page,
        per_page=per_page,
        total=total,
        estado=estado,
        orden=orden,
    )


@bp.get("/update/<int:contacto_id>")
@h.authenticated_route(module="contacto", permissions=("update",))
def update(contacto_id):
    """
    Muestra el formulario de edición para un contacto específico.

    Args:
        contacto_id (int): ID del contacto a editar.

    Returns:
        render_template:
            Renderiza la plantilla de edición del contacto con el formulario prellenado.
    """
    contacto = c.getContacto(contacto_id)
    if not contacto:
        flash("Contacto no encontrado", "danger")
    else:
        form = ContactoEditForm(obj=contacto)
    return render_template("contacto/edit.html", form=form, contacto_id=contacto_id)


@bp.post("/delete/<int:contacto_id>")
@h.authenticated_route(module="contacto", permissions=("destroy",))
def delete(contacto_id):
    """
    Elimina un contacto específico de la base de datos.

    Args:
        contacto_id (int): ID del contacto a eliminar.

    Returns:
        redirect:
            Redirige a la vista de listado de contactos después de eliminar el contacto.
    """
    contacto = c.getContacto(contacto_id)
    if contacto:
        c.borrarContacto(contacto)
        flash("Contacto borrado correctamente", "success")
    else:
        flash("Contacto no encontrado", "danger")
    return redirect(url_for("contacto.index"))


@bp.post("/update_contacto/<int:contacto_id>")
@h.authenticated_route(module="contacto", permissions=("update",))
def update_contacto(contacto_id):
    """
    Actualiza un contacto con los datos del formulario, informando el éxito o error de la operación.

    Args:
        contacto_id (int): ID del contacto a actualizar.

    Returns:
        redirect:
            Redirige a la vista de listado de contactos después de actualizar el contacto,
            o redirige a la vista de edición del contacto si hay errores en el formulario.
    """
    contacto = c.getContacto(contacto_id)
    if not contacto:
        flash("Contacto no encontrado", "danger")
    else:
        form_data = {key: value for key, value in request.form.items() if value}

        filtered_validation_rules = {
            key: value for key, value in validation_rules.items()
        }
        ok, errors = formulario_valido(form_data, filtered_validation_rules)
        if ok:
            ok = c.updateContacto(contacto, request.form)
            if ok:
                flash("Contacto actualizado correctamente", "success")
        else:
            for field, error_list in errors.items():
                for error in error_list:
                    flash(f"El campo {field} tiene un error: {error}", "error")
            return redirect(url_for("contacto.update", contacto_id=contacto_id))
    return redirect(url_for("contacto.index"))


@bp.get("/show_mensaje/<int:contacto_id>")
@h.authenticated_route(module="contacto", permissions=("show",))
def show_mensaje(contacto_id):
    """
    Muestra los mensajes de un contacto específico.

    Args:
        contacto_id (int): ID del contacto a mostrar.

    Returns:
        render_template:
            Renderiza la plantilla del mensaje del contacto.
    """
    contacto = c.getContacto(contacto_id)
    if not contacto:
        flash("Contacto no encontrado", "danger")
    return render_template("contacto/show.html", contacto=contacto)
