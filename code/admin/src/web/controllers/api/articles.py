from flask import Blueprint, jsonify, request
from datetime import datetime

from web.controllers.api import base
from src.web.schemas.content import contents_schema
from src.core.content import ContentService

bp = Blueprint("articles", __name__, url_prefix="/articles")

@bp.get("/")
@base.validation(method="GET")
def articles():
    """
    Genera un JSON de la lista de artículos que cumplan con los filtros ingresados con paginación devolviéndolo en un JSON.

    Query Parameters:
        author: str
            Email del autor del artículo.
        published_from: str
            Fecha de publicación mínima del artículo (formato: YYYY-MM-DD).
        published_to: str
            Fecha de publicación máxima del artículo (formato: YYYY-MM-DD).
        page: int
            Página a mostrar.
        per_page: int
            Cantidad de artículos por página.

    Returns:
        JSON con la lista de artículos filtrados.
    """
    author = request.args.get('author') or None
    published_from = request.args.get('published_from') or None
    published_to = request.args.get('published_to') or  None
    page = request.args.get('page', type=int, default=1)
    per_page = request.args.get('per_page', type=int, default=10)

    contents, total = ContentService.all_contents(
        author=author,
        published_from=published_from,
        state="publicado",
        published_to=published_to,
        page=page,
        per_page=per_page,
    )

    combined_contents = []
    for content, content_user, user in contents:
        content.email = user.email
        combined_contents.append(content)

    data_articles = contents_schema.dump(combined_contents)
    return jsonify(data_articles,{"total":total})
