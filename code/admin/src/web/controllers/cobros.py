from datetime import datetime
from functools import wraps
from core.equipo import MemberService
from core.charge import ChargeService
from core.charge.charge import Charge
from core.jya import ServiceJyA as s
from core.jya.jya import JyA
from core.payment_method import PaymentMethodService
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from web.forms.charge import ChargeCreateForm
from web.forms.jya import JyAForm
from src.core.database import db
from src.web.controllers import _helpers as h


bp = Blueprint("cobros", __name__, url_prefix="/cobros")


def validate_charge_decorator(func):
    """
    Decorador que chequea que un miembro exista y no esté borrado.
    Args:
        func: función del controlador a ser decorada.
    Returns:
        function: si el miembro es válido, devuelve la función decorada. Si no, redirige a la página principal.
    """

    @wraps(func)
    def wrapper(charge_id: int, *args, **kwargs):
        # Aquí debe obtenerse solo el ID del usuario
        charge = ChargeService.find_charge_by_id(charge_id)
        if not charge or charge.deleted:
            h.flash_error("Miembro no encontrado")
            return redirect("/")
        # Se pasa el ID del usuario en lugar del diccionario completo
        return func(charge, *args, **kwargs)

    return wrapper


@bp.get("/")
@h.authenticated_route(module="cobros", permissions=("show", "index",))
def charge_get():
    """
    Muestra la lista de cobros.

    """
    page, per_page = h.url_pagination_args(
        default_per_page=10
    )
    order = request.args.get('order', 'asc')
    metodo_pago = request.values.get("metodo_pago")
    desde = request.values.get("start_date")
    hasta = request.values.get("end_date")
    nombre = request.values.get("nombre")
    apellido = request.values.get("apellido")

    if desde and hasta:

        desde_date = datetime.strptime(desde, '%Y-%m-%d')
        hasta_date = datetime.strptime(hasta, '%Y-%m-%d')

        if hasta_date < desde_date:
            h.flash_error(
                "La fecha 'Hasta' no puede ser anterior a la fecha 'Desde'.")
            return redirect(url_for("cobros.charge_get"))


    if request.args.get('toggle_order'):
        order = 'desc' if order == 'asc' else 'asc'
    charges, total = ChargeService.filter_users(
        order, page, per_page, metodo_pago, desde, hasta, nombre, apellido
    )

    return render_template(
        "cobros/index.html",
        nombre=nombre,
        apellido=apellido,
        charges=charges,
        page=page,
        per_page=per_page,
        total=total,
        order=order,
        metodo_pago=metodo_pago,
        start_date=desde,
        end_date=hasta
    )


@bp.get("/deudores")
@h.authenticated_route(module="cobros", permissions=("show", "index",))
def debtors_get():
    """
    Muestra la lista de deudores.
    """
    page, per_page = h.url_pagination_args(default_per_page=10)

    count_changes, total = ChargeService.count_charges_for_jya(page, per_page)

    return render_template(
        "cobros/deudores.html",
        jya=count_changes,
        page=page,
        per_page=per_page,
        total=total,
    )


@bp.get("/register")
@h.authenticated_route(module="cobros", permissions=("create",))
def charge_new_get():
    """
    Muestra el formulario para registrar un nuevo cobro.
    """
    form = ChargeCreateForm()

    return render_template("cobros/register.html", form=form)


@bp.post("/register")
@h.authenticated_route(module="cobros", permissions=("create",))
def register_charge_post():
    """
    Registra un nuevo cobro.
    """
    params = request.form

    charge_data = {
        "id_jya": params.get("id_jya"),
        "id_member": params.get("id_member"),
        "id_payment_method": params.get("id_payment_method"),
        "amount": params.get("amount"),
        "observation": params.get("observation"),
        "date": params.get("date"),
    }

    charge = ChargeService.create_charge(**charge_data)
    if not charge:
        h.flash_error("No se pudo registrar el cobro")
        return redirect(url_for("cobros.cobros_new_get"))

    h.flash_success("Cobro registrado exitosamente")

    return redirect(url_for("cobros.charge_get"))


@bp.get("/<int:charge_id>")
@h.authenticated_route(module="cobros", permissions=("show", "update",))
@validate_charge_decorator
def charge_id_get(charge, *args, **kwargs):
    """
    Muestra la información de un cobro. 
    """
    form = ChargeCreateForm(
        amount=charge.amount,
        id_member=charge.id_member,
        id_jya=charge.id_jya,
        id_payment_method=charge.id_payment_method,
        observation=charge.observation,
        date=charge.date
    )

    members_query, total = MemberService.all_members()
    members = [(member[0].id, f"{member[0].nombre} {member[0].apellido}")
               for member in members_query]
    methods_of_payments = [(method_of_payment.id, method_of_payment.name)
                           for method_of_payment in PaymentMethodService.list_payment_methods()]
    jya = [(jya.id, f"{jya.name} {jya.lastname}") for jya in s.list_jya()]
    return render_template(
        "cobros/update.html", charge=charge, form=form, members=members, methods_of_payments=methods_of_payments, jya=jya
    )


@bp.post("/<int:charge_id>")
@h.authenticated_route(module="cobros", permissions=("show", "update",))
@validate_charge_decorator
def charge_id_post(charge, *args, **kwargs):
    """
    Actualiza la información de un cobro.
    """
    form = ChargeCreateForm(request.form)
    
    if form.date.data:
        form.date.data = form.date.data.strftime('%Y-%m-%d')

    if not form.validate():  
        h.flash_info("Por favor, complete todos los campos requeridos.")
        return redirect(url_for("cobros.charge_id_get", charge_id=charge.id)) 
    
    ChargeService.update_charge(charge.id, **form.values())
    h.flash_success("Pagos actualizado con éxito.")
    return redirect(url_for("cobros.charge_get"))


@bp.post("/<int:charge_id>/mark_as_charge")
@h.authenticated_route(module="cobros", permissions=("update",))
@validate_charge_decorator
def charge_id_paid_post(charge, *args, **kwargs):

    value = ChargeService.mark_charge_as_paid(charge.id)
    h.flash_success(f"Cobro marcado como {value[1]}.")
    return redirect(url_for("cobros.charge_get"))


@bp.post("/<int:charge_id>/delete")
@h.authenticated_route(module="cobros", permissions=("destroy",))
@validate_charge_decorator
def charge_id_delete_post(charge, *args, **kwargs):
    """
    Elimina un cobro.
    """
    result = ChargeService.delete_charge(charge.id)

    if result:
        h.flash_success("Cobro eliminado con éxito.")
        return redirect(url_for("cobros.charge_get"))

    h.flash_error("No se pudo eliminar el cobro.")
    return redirect(url_for("cobros.charge_get"))
