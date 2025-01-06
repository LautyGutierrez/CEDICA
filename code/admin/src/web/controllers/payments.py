from datetime import datetime
from core.equipo import MemberService
from core.payment import PaymentService
from core.type_of_payment import TypeOfPaymentService
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from web.forms.payment import PaymentCreateForm
from src.core.database import db
from src.web.controllers import _helpers as h

bp = Blueprint("pagos", __name__, url_prefix="/pagos")


@bp.get("/")
@h.authenticated_route(module="pagos", permissions=("show", "index",))
def payments_get():
    page, per_page = h.url_pagination_args(
        default_per_page=10
    )
    order = request.args.get('order', 'asc')
    tipo_pago = request.values.get("tipo_pago")
    desde = request.values.get("start_date")
    hasta = request.values.get("end_date")

    if desde and hasta:

        desde_date = datetime.strptime(desde, '%Y-%m-%d')
        hasta_date = datetime.strptime(hasta, '%Y-%m-%d')

        if hasta_date < desde_date:
            h.flash_error(
                "La fecha 'Hasta' no puede ser anterior a la fecha 'Desde'.")
            return redirect(url_for("pagos.payments_get"))

    if request.args.get('toggle_order'):
        order = 'desc' if order == 'asc' else 'asc'
    payments, total = PaymentService.filter_users(
        order, page, per_page, tipo_pago, desde, hasta
    )
    return render_template(
        "pagos/index.html",
        payments=payments,
        page=page,
        per_page=per_page,
        total=total,
        order=order,
        tipo_pago=tipo_pago,
        start_date=desde,
        end_date=hasta
    )


@bp.get("/register")
@h.authenticated_route(module="pagos", permissions=("create",))
def payment_new_get():

    form = PaymentCreateForm()

    return render_template("pagos/register.html", form=form)


@bp.post("/register")
@h.authenticated_route(module="pagos", permissions=("create",))
def register_payment_post():

    params = request.form

    pago_data = {
        "id_member": params.get("id_member") if params.get("id_member") else None,
        "id_type_of_payment": params.get("id_type_of_payment"),
        "amount": params.get("amount"),
        "description": params.get("description"),
        "date": params.get("date"),
    }

    payment = PaymentService.create_payment(**pago_data)
    if not payment:
        h.flash_error("No se pudo registrar el pago")
        return redirect(url_for("pagos.payment_new_get"))

    h.flash_success("Pago registrado exitosamente")

    return redirect(url_for("pagos.payments_get"))


@bp.get("/<int:payment_id>")
@h.authenticated_route(module="pagos", permissions=("show", "update",))
def payment_id_get(payment_id: int):
    payment = PaymentService.find_payment_by_id(payment_id)
    if not payment:
        h.flash_info(f"Pago con id {payment_id} no encontrado.")
        return redirect(url_for("pagos.payments_get"))
    
    form = PaymentCreateForm(
        amount=payment.amount,
        id_member=payment.id_member,
        id_type_of_payment=payment.id_type_of_payment,
        description=payment.description,
        date=payment.date
    )

    members_all, total = MemberService.all_members()
    members = [(member[0].id, f"{member[0].nombre} {member[0].apellido}")
               for member in members_all]

    if payment.id_member is None:
        members_not_in_payment = True
    else:
        members_not_in_payment = False

    type_of_payment = [(type_of_payment.id, type_of_payment.name)
                       for type_of_payment in TypeOfPaymentService.list_type_of_payment()]

    return render_template(
        "pagos/update.html", payment=payment, form=form, members=members, type_of_payment=type_of_payment, members_not_in_payment=members_not_in_payment
    )


@bp.post("/<int:payment_id>")
@h.authenticated_route(module="pagos", permissions=("show", "update",))
def payment_id_post(payment_id: int):
    payment = PaymentService.find_payment_by_id(payment_id)

    if not payment:
        h.flash_info(f"Pago con id {payment_id} no encontrado.")
        return redirect(url_for("pagos.payments_get"))

    form = PaymentCreateForm(request.form)
    if form.date.data:
        form.date.data = form.date.data.strftime('%Y-%m-%d')
    
    if not form.validate():  
        h.flash_info("Por favor, complete todos los campos requeridos.")
        return redirect(url_for("pagos.payment_id_get", payment_id=payment_id))

    if form.id_member.data in [None, '', ' ']:
        print("id_member is empty")
        form.id_member.data = None
        
    PaymentService.update_payment(payment_id, **form.values())
    h.flash_success("Pagos actualizado con éxito.")
    return redirect(url_for("pagos.payments_get"))


@bp.post("/<int:payment_id>/delete")
@h.authenticated_route(module="pagos", permissions=("destroy",))
def payment_id_delete_post(payment_id: int):
    payment = PaymentService.find_payment_by_id(payment_id)

    if not payment:
        h.flash_info(f"Pago con id {payment_id} no encontrado.")
        return redirect(url_for("pagos.payments_get"))

    result = PaymentService.delete_payment(payment_id)

    if result:
        h.flash_success("Pago eliminado con éxito.")
        return redirect(url_for("pagos.payments_get"))

    h.flash_error("No se pudo eliminar el pago.")
    return redirect(url_for("pagos.payments_get"))
