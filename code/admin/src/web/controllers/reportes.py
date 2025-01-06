from datetime import datetime
from src.web.forms.reporteForm import ReporteForm
from src.core.payment import PaymentService
from src.core.jya import ServiceJyA
from flask import Blueprint, render_template, request, redirect, url_for
from src.web.controllers import _helpers as h
import urllib.parse
from src.web.forms.validators import (
    solo_letras,
    solo_numeros,
)

validation_rules = {
    "name": solo_letras,
    "lastname": solo_letras,
    "document_number": solo_numeros,
    "pagos_minima": solo_numeros,
    "pagos_maxima": solo_numeros,
    "valor_minimo": solo_numeros,
    "valor_maximo": solo_numeros,
} 
    

bp = Blueprint("reportes", __name__)


@bp.get("/reporte-propuestas-trabajo")
@h.authenticated_route(
    module="reportes",
    permissions=(
        "index",
        "show",
    ),
)
def reporte_propuestas_trabajo():
    propuestas = ServiceJyA.cantidad_propuestas_trabajo()
    return render_template('reportes/reporte_propuestas_trabajo.html', propuestas=propuestas,  urllib=urllib)


@bp.get("/reporte-deudores")
@h.authenticated_route(
    module="reportes",
    permissions=(
        "index",
        "show",
    ),
)
def reporte_deudores():
    """
    Renderiza la vista de reporte de deudores.

    Returns:
        render_template:
            Vista de reporte de deudores.
    
    Errors:
        Ingresar un valor válido:
            Si el valor ingresado no es válido, se muestra un mensaje de error.
    """

    order_field: str = request.args.get("order_by", "pagos")
    order_type: str = request.args.get("toggle_order", "asc")
    field: str = request.args.get("filter_field", "pagos_minima")
    filter_input: str = request.args.get("filter_input", "")
    page, per_page = h.url_pagination_args(default_per_page=10)

    if filter_input:
        if not validation_rules[field](filter_input):
            h.flash_error("Ingrese un valor válido.")
            return redirect(url_for("reportes.reporte_deudores"))

    deudores, total = ServiceJyA.deudores(
        order_field, order_type, field, filter_input, page, per_page
    )

    return render_template(
        "reportes/reporte_deudores.html",
        deudores=deudores,
        order_by=order_field,
        order=order_type,
        filter_field=field,
        filter_input=filter_input,
        page=page,
        per_page=per_page,
        total=total,
    )


@bp.get("/reporte-cobros")
@h.authenticated_route(
    module="reportes",
    permissions=(
        "index",
        "show",
    ),
)
def reporte_historico_cobros():
    form = ReporteForm()
    return render_template("reportes/reporte_cobros_form.html", form=form)


@bp.get('/reporte-historial-cobros')
@h.authenticated_route(module="reportes", permissions=("index","show",))
def reporte_historico_cobros_post():
    page, per_page = h.url_pagination_args(default_per_page=10)
    
    
    fecha_desde_str = request.args.get('fecha_desde')
    fecha_desde = datetime.strptime(fecha_desde_str, '%Y-%m-%d')
    fecha_hasta_str = request.args.get('fecha_hasta')
    fecha_hasta = datetime.strptime(fecha_hasta_str, '%Y-%m-%d')
    miembro = request.args.get('miembro')
   
    if not fecha_desde or not fecha_hasta or not miembro:
        h.flash_error("Por favor, complete los campos.")
        return redirect(url_for('reportes.reporte_historico_cobros'))
    
    if fecha_hasta < fecha_desde:
        h.flash_error("La fecha de inicio debe ser menor a la fecha de fin.")
        return redirect(url_for('reportes.reporte_historico_cobros')) 

   
    cobros, total = PaymentService.cobros_por_miembro(fecha_desde, fecha_hasta , miembro , page, per_page)
   
    return render_template('reportes/reporte_cobros.html', cobros=cobros, page=page, per_page=per_page, total=total, fecha_desde=fecha_desde_str, fecha_hasta=fecha_hasta_str, miembro=miembro)


@bp.get("/reportes-graficos")
@h.authenticated_route(
    module="reportes",
    permissions=(
        "index",
        "show",
    ),
)
def reportes_graficos():
    return render_template("reportes/reportes_index.html")

@bp.get("/propuesta-trabajo-jya/<propuesta>")
@h.authenticated_route(module="reportes", permissions=("index","show",))
def propuesta_trabajo_jya(propuesta):
    
    order_field: str = request.args.get("order_by", "name")
    order_type: str = request.args.get("toggle_order", "asc")
    field: str = request.args.get("filter_field", "name")
    filter_input: str = request.args.get("filter_input", "")
    page, per_page = h.url_pagination_args(default_per_page=10)

    if filter_input:
        if not validation_rules[field](filter_input):
            h.flash_error("Ingrese un valor válido.")
            return redirect(url_for("reportes.propuesta_trabajo_jya", propuesta=propuesta))

    jya, total = ServiceJyA.propuesta_trabajo_jya(
        propuesta, order_field, order_type, field, filter_input, page, per_page
    )
    
    return render_template(
        'reportes/propuesta_trabajo_jya.html', 
        jya=jya,
        order_by=order_field,
        order=order_type,
        filter_field=field,
        filter_input=filter_input,
        page=page,
        per_page=per_page,
        total=total,
        propuesta=propuesta
    )
