from core.contact import ContactoService
from flask import Blueprint, jsonify,current_app
from web.schemas.contact import contact_schema
from src.web.controllers.api import base
from src.web.forms import api as api_forms
import requests


bp = Blueprint("contact", __name__, url_prefix="/contact")


@bp.post("/")
@base.validation(api_forms.RequestContactForm)
def new_request_contact(body: api_forms.RequestContactFormValues):
    """
    Crea una nueva solicitud de contacto a partir de los datos enviados.
    
    Returns:
        JSON con los datos de la nueva solicitud o un mensaje de error en caso de que falten parámetros obligatorios.
    """
    
    name = body["nombre"]
    lastname = body["apellido"]
    email = body["email"]
    body_ms = body["cuerpo_mensaje"]
    token = body["recaptcha_token"]
    if not token:    
        return jsonify({"error": "Error al enviar el token de recaptcha"}), 400
    response = requests.post("https://www.google.com/recaptcha/api/siteverify",
        data={"secret": current_app.config.get("CAPTCHA_SECRET_KEY"), "response": token})

    result = response.json()
    if not result.get("success"):
        return jsonify({"error": "El token de recaptcha es inválido"}), 400
    
    if not name:
        return jsonify({"error": "El parámetro 'name' es obligatorio"}), 400

    if not lastname:
        return jsonify({"error": "El parámetro 'lastname' es obligatorio"}),400

    if not email:
        return jsonify({"error": "El parámetro 'email' es obligatorio"}), 400

    if not body_ms:
        return jsonify({"error": "El parámetro 'body' es obligatorio"}), 400

    
    contacto = {
            "nombre":name,
            "apellido": lastname ,
            "email": email,
            "cuerpo_mensaje":body_ms,
        }
    
    
    new_request = contact_schema.dump(ContactoService.create(**contacto))
    return jsonify(new_request), 201
