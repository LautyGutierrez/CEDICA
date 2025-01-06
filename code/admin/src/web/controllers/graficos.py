from src.core.charge import ChargeService
from src.core.jya import ServiceJyA
from flask import Blueprint, render_template
import plotly.express as px
import json
from plotly.utils import PlotlyJSONEncoder as jsone
from src.web.controllers import _helpers as h

bp = Blueprint('graficos', __name__)

@bp.get('/grafico-beca')
@h.authenticated_route(module="reportes", permissions=("index","show",))
def grafico_beca():
    """
    Retorna un gráfico de torta con la proporción de JyA con y sin beca.
    
    Returns:
        render_template: Retorna el template grafico.html con el gráfico de torta.
    """
    cant_con_beca = ServiceJyA.cantidad_becados()
    cant_sin_beca = ServiceJyA.cantidad_sin_beca()
    
    data = {
        'Beca': ['Con Beca', 'Sin Beca'],
        'Cantidad': [cant_con_beca, cant_sin_beca]
    }

    fig = px.pie(
        data,
        names='Beca',
        values='Cantidad',
        title='Proporción de JyA con y sin Beca'
    )
    fig.update_layout(
        width=1000,
        height=600
    )
    graph_json = json.dumps(fig, cls=jsone)
    title = "Gráfico de Jinetes/Amazonas con Becas"
    texto = "Acá podés observar la proporción de Jinetes/Amazonas con y sin Beca"
    return render_template('graficos/grafico.html', graph_json=graph_json, title=title, texto=texto)

@bp.get('/grafico-discapacidad')
@h.authenticated_route(module="reportes", permissions=("index","show",))
def grafico_discapasidad():
    """
    Retorna un gráfico torta con la proporcios de los tipos
    de discapacidad de los JyA.
    
    Returns:
        render_template: Retorna el template grafico.html con el gráfico de torta.
    """
    cant_motora = ServiceJyA.cantidad_discapacidad('Motora')
    cant_mental = ServiceJyA.cantidad_discapacidad('Mental')
    cant_visceral = ServiceJyA.cantidad_discapacidad('Visceral')
    cant_sensorial = ServiceJyA.cantidad_discapacidad('Sensorial')
    
    data = {
        "Tipo": ['Motora', 'Mental', 'Visceral', 'Sensorial'],
        "Cantidad": [cant_motora, cant_mental, cant_visceral, cant_sensorial]
    }
    
    fig = px.pie(
        data,
        names='Tipo',
        values='Cantidad',
        title='Proporción de Tipos de Discapacidad de Jinetes/Amazonas'
    )
    fig.update_layout(
        width=1000,
        height=600
    )
    graph_json = json.dumps(fig, cls=jsone)
    title = "Gráfico de Jinetes/Amazonas por Tipo de Discapacidad"
    texto = "Acá podés observar la proporción de las discapacidades de los Jinetes/Amazonas dentro de la institución"
    return render_template('graficos/grafico.html', graph_json=graph_json, title=title, texto=texto)

@bp.get('/grafico-ingresos')
@h.authenticated_route(module="reportes", permissions=("index","show",))
def grafico_ingresos():
    """
    Retorna un gráfico de barras con los ingresos por mes de los ultimos 12 meses.
    
    Returns:
        render_template: Retorna el template grafico.html con el gráfico de barras.
    """
    ingresos_por_mes = ChargeService.obtener_ingresos_por_mes()
    meses = [resultado[0].strftime('%Y-%m') for resultado in ingresos_por_mes]  # Mes en formato YYYY-MM
    ingresos = [resultado[1] for resultado in ingresos_por_mes]  # Suma de los ingresos del mes


    meses_nombres = {
        '01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril',
        '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto',
        '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'
    }
        
    meses_nombres_convertidos = [f"{meses_nombres[mes.split('-')[1]]} {mes.split('-')[0]}" for mes in meses]
    
    data = {
        "Meses": meses_nombres_convertidos,
        "Ingresos": ingresos
    }
    
    fig = px.bar(
        data,
        x='Meses',
        y='Ingresos',
        title='Ingresos por Mes de los Últimos 12 Meses'
    )
    fig.update_layout(
        width=1000,
        height=600
    )
    graph_json = json.dumps(fig, cls=jsone)
    title = "Gráfico de Ingresos por Mes"
    texto = "Acá podés observar los ingresos mensuales de la institución de los últimos 12 meses"
    return render_template('graficos/grafico.html', graph_json=graph_json, title=title, texto=texto)