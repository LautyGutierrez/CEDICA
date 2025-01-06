from datetime import datetime
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
    Response,
    current_app as app,
    send_file,
)
from functools import wraps
from os import fstat
from src.core.archivos import ArchivoService
from src.core.auth import AuthService
from src.web.controllers import _helpers as h
from src.core.equipo import MemberService
from src.core.equipo.member_user_controller import MemberUser
from web.forms.archivoForm import ArchivoMiembroForm
from web.forms.enlaceForm import EnlaceForm
from web.forms.memberForm import MemberForm, DeleteMemberForm
from src.web.forms.validators import (
    formulario_valido,
    solo_letras,
    solo_fechas,
    solo_numeros,
    es_correo_valido,
    letras_y_numeros,
    es_enlace_valido,
)
import io
import os

bp = Blueprint("member", __name__, url_prefix="/member")

validation_rules = {
    "nombre": solo_letras,
    "apellido": solo_letras,
    "dni": solo_numeros,
    "domicilio": letras_y_numeros,
    "email": es_correo_valido,
    "localidad": solo_letras,
    "telefono": solo_numeros,
    "profesion": solo_letras,
    "puesto_laboral": solo_letras,
    "fecha_inicio": solo_fechas,
    "fecha_cese": solo_fechas,
    "nombre_emergencia": solo_letras,
    "telefono_emergencia": solo_numeros,
    "obra_social": solo_letras,
    "num_afiliado": solo_numeros,
    "condicion": solo_letras,
}

required_fields = [
    "nombre",
    "apellido",
    "dni",
    "domicilio",
    "email",
    "localidad",
    "telefono",
    "profesion",
    "puesto_laboral",
    "fecha_inicio",
    "nombre_emergencia",
    "telefono_emergencia",
    "condicion",
]

optional_fields = ["fecha_cese", "obra_social", "num_afiliado"]


def validate_possible_repeated(fields) -> bool:
    """
    Hace las validaciones de que no se repitan posibles campos repetidos.
    Args:
        fields: campos que pueden ser repetidos.
    Returns:
        bool:
            True si ya existe un miembro con alguno de esos campos;
            False en caso de que no.
    """
    validation_checks = {
        0: (
            "Ya existe un miembro registrado con el email ingresado",
            MemberService.find_member_by_mail,
        ),
        1: (
            "Ya existe un miembro registrado con el DNI ingresado",
            MemberService.find_member_by_dni,
        ),
        2: (
            "Ya existe un miembro registrado con el número afiliado ingresado",
            MemberService.find_member_by_num,
        ),
    }

    for index, (error_message, validation_func) in validation_checks.items():
        if fields[index] and validation_func(fields[index]):
            h.flash_error(error_message)
            return True

    return False


def validate_member_decorator(func):
    """
    Decorador que chequea que un miembro exista y no esté borrado.
    Args:
        func: función del controlador a ser decorada.
    Returns:
        function: si el miembro es válido, devuelve la función decorada. Si no, redirige a la página principal.
    """

    @wraps(func)
    def wrapper(member_id: int, *args, **kwargs):
        member = MemberService.get_member(member_id)
        if not member or member.borrado:
            h.flash_error("Miembro no encontrado")
            return redirect("/")
        return func(member, *args, **kwargs)

    return wrapper


def save_file_minio(file, filename: str) -> None:
    """
    Se sube el archivo a Minio.
    Args:
        file: el archivo a ser subido.
        filename: el nombre del archivo a ser subido.
    Returns:
        None
    """
    client = app.storage.client
    size = fstat(file.fileno()).st_size
    client.put_object(
        app.config["MINIO_BUCKET_NAME"],
        filename,
        file,
        size,
        content_type=file.content_type,
    )


def delete_file_minio(file) -> None:
    """
    Elimina un archivo de Minio.
    Args:
        file: archivo a ser subido.

    Returns:
        None
    """
    filename = file.filename
    client = app.storage.client
    client.remove_object(app.config["MINIO_BUCKET_NAME"], filename)


@bp.get("/")
@h.authenticated_route(
    module="equipo",
    permissions=(
        "index",
        "show",
        "create",
        "update",
        "destroy",
    ),
)
def show_members():
    """
    Renderiza la página principal de miembros con paginación, filtrado y orden.
    Returns:
        render_template:
            Renderiza el HTML index del módulo equipo, con las variables de contexto.
    """
    order_field: str = request.args.get("order_by", "nombre")
    order_type: str = request.args.get("toggle_order", "asc")
    job: str = request.args.get("job", "")
    field: str = request.args.get("filter_field", "nombre")
    filter_input: str = request.args.get("filter_input", "")
    page, per_page = h.url_pagination_args(default_per_page=10)

    members, total = MemberService.all_members(
        order_field, order_type, job, field, filter_input, page, per_page
    )

    return render_template(
        "equipo/index.html",
        members=members,
        order_by=order_field,
        order=order_type,
        job=job,
        filter_field=field,
        filter_input=filter_input,
        page=page,
        per_page=per_page,
        total=total,
    )


@bp.get("/create")
@h.authenticated_route(module="equipo", permissions=("create",))
def register_member():
    """
    Renderiza el formulario para dar de alta a un miembro.
    Returns:
        render_template:
            Renderiza el HTML del formulario para dar de alta a un miembro.
    """
    form = MemberForm()
    return render_template("equipo/member.html", form=form, longitud=len(form.data))


@bp.post("/create")
def register_member_post():
    """
    Registra a un nuevo miembro en la base de datos, validando la información ingresada en el formulario.

    Returns:
        redirect:
            Redirecciona a la página donde se muestran los miembros si el registro es exitoso.
            Redirecciona al formulario de edición si ocurre un error.

    Raises:
        Exception:
            Si ocurre un error en la creación del miembro en la base de datos.

    Errores:
        Si la fecha de cese es posterior a la fecha de inicio.
        Si los datos de email, DNI o número de afiliado ya existen en la base de datos.
        Si se ingresó una obra social sin número de afiliado o un número de afiliado sin obra social.
        Si la información del formulario no es válida.
    """
    params = request.form

    missing_fields = [field for field in required_fields if not params.get(field)]

    if missing_fields:
        h.flash_error(f"Faltan campos requeridos")
        return redirect(url_for("member.register_member"))

    member_data = {
        "nombre": params.get("nombre"),
        "apellido": params.get("apellido"),
        "dni": params.get("dni"),
        "domicilio": params.get("domicilio"),
        "email": params.get("email"),
        "localidad": params.get("localidad"),
        "telefono": params.get("telefono"),
        "profesion": params.get("profesion"),
        "puesto_laboral": params.get("puesto_laboral"),
        "fecha_inicio": params.get("fecha_inicio"),
        "fecha_cese": params.get("fecha_cese") or None,
        "nombre_emergencia": params.get("nombre_emergencia"),
        "telefono_emergencia": params.get("telefono_emergencia"),
        "obra_social": params.get("obra_social") or None,
        "num_afiliado": params.get("num_afiliado") or None,
        "condicion": params.get("condicion"),
    }

    filtered_validation_rules = {
        key: value
        for key, value in validation_rules.items()
        if key not in optional_fields or params.get(key)
    }
    ok, errors = formulario_valido(params, filtered_validation_rules)

    if not ok:
        for field, error_list in errors.items():
            for error in error_list:
                h.flash_error(f"El campo {field} tiene un error: {error}")
                break
        return redirect(url_for("member.register_member"))

    if params.get("fecha_cese"):
        inicio = datetime.strptime(params.get("fecha_inicio"), "%Y-%m-%d")
        cese = datetime.strptime(params.get("fecha_cese"), "%Y-%m-%d")
        if cese <= inicio:
            h.flash_error("La fecha de cese debe ser posterior a la fecha de inicio")
            return redirect(url_for("member.register_member"))

    repeated = validate_possible_repeated(
        [params.get("email"), params.get("dni"), params.get("num_afiliado")]
    )
    if repeated:
        return redirect(url_for("member.register_member"))

    form = MemberForm(data=member_data)
    if not form.validate_on_submit():
        h.flash_error("Error con la información ingresada")
        return redirect(url_for("member.register_member"))

    if (form.obra_social.data and not form.num_afiliado.data) or (
        not form.obra_social.data and form.num_afiliado.data
    ):
        h.flash_error("Error con la información de la obra social")
        return redirect(url_for("member.register_member"))

    try:
        member, user = MemberUser.create_miembro(**member_data)
        h.flash_success("Miembro registrado exitosamente")
        if user:
            h.flash_success("Se asoció al miembro con una cuenta de usuario")
    except Exception as e:
        print(e)
        h.flash_error("Error de base de datos")
        return redirect(url_for("member.register_member"))

    return redirect(url_for("member.show_members"))


@bp.get("/<int:member_id>")
@h.authenticated_route(
    module="equipo",
    permissions=(
        "show",
        "update",
    ),
)
@validate_member_decorator
def member_id_get(member, *args, **kwargs):
    """
    Renderiza el formulario para editar la información de un miembro válido, con los campos llenos con su información.

    Args:
        member:
            Miembro cuya información se va a editar.
        *args:
            Argumentos adicionales en forma de tupla.
        **kwargs:
            Argumentos claves adicionales en forma de diccionario.

    Returns:
        render_template:
            Renderiza el formulario con la información del miembro seleccionado.
    """
    form = MemberForm(
        nombre=member.nombre,
        apellido=member.apellido,
        dni=member.dni,
        domicilio=member.domicilio,
        email=member.email,
        localidad=member.localidad,
        telefono=member.telefono,
        profesion=member.profesion,
        puesto_laboral=member.puesto_laboral,
        fecha_inicio=member.fecha_inicio,
        fecha_cese=member.fecha_cese,
        nombre_emergencia=member.nombre_emergencia,
        telefono_emergencia=member.telefono_emergencia,
        obra_social=member.obra_social,
        num_afiliado=member.num_afiliado,
        condicion=member.condicion,
    )

    return render_template(
        "equipo/editMiembro.html", form=form, longitud=len(form.data), member=member
    )


@bp.post("/<int:member_id>")
@h.authenticated_route(module="equipo", permissions=("update",))
@validate_member_decorator
def edit_member(member, *args, **kwargs):
    """
    Edita la información de un miembro válido, validando que la nueva información ingresada sea válida.

    Args:
        member:
            Miembro cuya información se va a editar.
        *args:
            Argumentos adicionales en forma de tupla.
        **kwargs:
            Argumentos claves adicionales en forma de diccionario.

    Returns:
        redirect:
            Redirecciona a la página donde se muestran los miembros si la edición es exitosa o si ocurre un error.
    """
    params = request.form

    missing_fields = [field for field in required_fields if not params.get(field)]

    if missing_fields:
        h.flash_error(f"Faltan campos requeridos")
        return redirect(url_for("member.register_member"))

    email = params.get("email")
    dni = int(params.get("dni"))
    num_afiliado = params.get("num_afiliado")
    fecha_inicio = params.get("fecha_inicio")
    fecha_cese = params.get("fecha_cese")
    obra_social = params.get("obra_social")

    filtered_validation_rules = {
        key: value
        for key, value in validation_rules.items()
        if key not in optional_fields or params.get(key)
    }

    ok, errors = formulario_valido(params, filtered_validation_rules)
    if not ok:
        for field, error_list in errors.items():
            for error in error_list:
                h.flash_error(f"El campo {field} tiene un error: {error}")
                break
        return redirect(url_for("member.register_member"))

    new_fields = []
    new_fields.append(email if member.email != email else None)
    new_fields.append(dni if member.dni != dni else None)
    new_fields.append(num_afiliado if member.num_afiliado != num_afiliado else None)

    repeated = validate_possible_repeated(new_fields)
    if repeated:
        return redirect(url_for("member.member_id_get", member_id=member.id))

    if obra_social and not num_afiliado or not obra_social and num_afiliado:
        h.flash_error("Error con la información de la obra social")
        return redirect(url_for("member.member_id_get", member_id=member.id))

    if fecha_cese:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        cese = datetime.strptime(fecha_cese, "%Y-%m-%d")
        if cese <= inicio:
            h.flash_error("La fecha de cese debe ser posterior a la fecha de inicio")
            return redirect(url_for("member.member_id_get", member_id=member.id))

    try:
        MemberService.update_member(member.id, request.form)
        h.flash_success("Miembro actualizado con éxito!")
        return redirect(url_for("member.show_members"))
    except Exception as e:
        print(e)
        h.flash_error("Error actualizando al miembro")
        return redirect(url_for("member.member_id_get", member_id=member.id))


@bp.post("/deleteMember/<int:member_id>")
@h.authenticated_route(module="equipo", permissions=("destroy",))
@validate_member_decorator
def delete_member(member, *args, **kwargs):
    """
    Elimina lógicamente a un miembro válido de la base de datos.

    Args:
        member:
            Miembro a ser eliminado.
        *args:
            Argumentos adicionales en forma de tupla.
        **kwargs:
            Argumentos claves adicionales en forma de diccionario.

    Returns:
        redirect:
            Redirecciona a la página donde se muestran los miembros si el eliminado es exitoso o ocurre un error.

    Errores:
        Si el formulario no es válido.
        Si hay un error eliminando al miembro.
    """
    form = DeleteMemberForm()
    if not form.validate_on_submit():
        h.flash_error("Error")
        return redirect(url_for("member.show_members"))

    delete = MemberService.delete_member(member.id)
    if not delete:
        h.flash_error("Error eliminando el miembro")
        return redirect(url_for("member.show_members"))
    h.flash_success("Miembro eliminado con éxito!")
    return redirect(url_for("member.show_members"))


@bp.post("/changeStatus/<int:member_id>")
@h.authenticated_route(module="equipo", permissions=("update",))
@validate_member_decorator
def change_status(member, *args, **kwargs):
    """
    Cambia el estado de un miembro válido.

    Args:
        member:
            Miembro cuyo estado se va a cambiar.
        *args:
            Argumentos adicionales en forma de tupla.
        **kwargs:
            Argumentos claves adicionales en forma de diccionario.

    Returns:
        redirect:
            Redirecciona a la página donde se muestran todos los miembros si el cambio de estado es exitoso u ocurre un error.

    Errores:
        Si ocurre un error al cambiar el estado.
    """
    change = MemberService.change_status(member.id)
    if not change:
        h.flash_error("No se pudo cambiar el estado del miembro")
        return redirect(url_for("member.show_members"))
    h.flash_success("Estado del miembro actualizado!")
    return redirect(url_for("member.show_members"))


@bp.get("/showFiles/<int:member_id>")
@h.authenticated_route(
    module="equipo", permissions=("index", "show", "create", "update", "destroy")
)
@validate_member_decorator
def show_files(member, *args, **kwargs):
    """
    Muestra los archivos de un miembro válido.

    Args:
        member:
            Miembro cuyos archivos se van a mostrar.
        *args:
            Argumentos adicionales en forma de tupla.
        **kwargs:
            Argumentos claves adicionales en forma de diccionario.

    Returns:
        render_template:
            Renderiza el HTML donde se muestran los archivos subidos por el miembro con las variables de contexto.
    """
    order_type: str = request.args.get("toggle_order", "asc")
    filter_type: str = request.args.get("filter_type", "")
    filter_input: str = request.args.get("filter_input", "")
    page, per_page = h.url_pagination_args(default_per_page=10)

    archivos, total = ArchivoService.files_of_member(
        member.id, page, per_page, order_type, filter_type, filter_input
    )

    return render_template(
        "equipo/filesMiembro.html",
        member=member,
        archivos=archivos,
        page=page,
        per_page=per_page,
        total=total,
        filter_input=filter_input,
        filter_type=filter_type,
        order_type=order_type,
    )


@bp.get("/uploadFiles/<int:member_id>")
@h.authenticated_route(module="equipo", permissions=("create",))
@validate_member_decorator
def upload_files(member, *args, **kwargs):
    """
    Muestra el formulario para subir un archivo a un miembro válido.

    Args:
        member:
            Miembro al cual se va a subir un archivo.
        *args:
            Argumentos adicionales en forma de tupla.
        **kwargs:
            Argumentos claves adicionales en forma de diccionario.

    Returns:
        render_template:
            Renderiza el HTML del formulario para subir archivos.
    """

    form = ArchivoMiembroForm()
    return render_template(
        "equipo/uploadFile.html",
        titulo="archivo",
        function="member.insert_file",
        form=form,
        id=member.id,
    )


@bp.post("/uploadFiles/<int:member_id>")
@h.authenticated_route(module="equipo", permissions=("create",))
@validate_member_decorator
def insert_file(member, *args, **kwargs):
    """
    Sube un archivo correspondiente a un miembro válido a la base de datos.

    Args:
        member:
            Miembro al cual se la va a subir el archivo.
        *args:
            Argumentos adicionales en forma de tupla.
        **kwargs:
            Argumentos claves adicionales en forma de diccionario.

    Returns:
        redirect:
            Redirecciona a la página donde se muestran los archivos si se subió correctamente o hubo un error.

    Errores:
        Información del formulario no válida.
        Error al subir el archivo a la base de datos.
    """
    if "archivo" not in request.files or request.files["archivo"].filename == "":
        h.flash_error(
            "El campo 'archivo' es requerido y debe contener un archivo válido"
        )
        return redirect(url_for("member.upload_files", member_id=member.id))

    params = request.form
    required = ["titulo", "tipo_archivo"]
    missing_fields = [field for field in required if not params.get(field)]
    if missing_fields:
        h.flash_error(f"Faltan campos requeridos")
        return redirect(url_for("member.upload_files", member_id=member.id))

    validation_rules = {
        "titulo": letras_y_numeros,
        "tipo_archivo": solo_letras,
    }
    ok, errors = formulario_valido(params, validation_rules)
    if not ok:
        for field, error_list in errors.items():
            for error in error_list:
                h.flash_error(f"El campo {field} tiene un error: {error}")
                break
        return redirect(url_for("member.upload_files", member_id=member.id))

    form = ArchivoMiembroForm()
    if not form.validate_on_submit():
        h.flash_error("Información de archivo incorrecta")
        return redirect(url_for("member.show_files", member_id=member.id))

    file = {
        "titulo": form.titulo.data,
        "filename": f"{member.id}_{request.files['archivo'].filename}",
        "enlace": "No se subió un enlace",
        "tipo": form.tipo_archivo.data,
    }

    try:
        save_file_minio(request.files["archivo"], file["filename"])
        ArchivoService.upload_file(member.id, **file)
        h.flash_success("Archivo subido correctamente")
    except:
        h.flash_error("Error al subir el archivo")

    return redirect(url_for("member.show_files", member_id=member.id))


@bp.get("/uploadLink/<int:member_id>")
@h.authenticated_route(module="equipo", permissions=("create",))
@validate_member_decorator
def upload_link(member, *args, **kwargs):
    """
    Muestra el formulario para subir un enlace a un miembro válido.

    Args:
        member:
            Miembro al cual se le va a subir un enlace.
        *args:
            Argumentos adicionales en forma de tupla.
        **kwargs:
            Argumentos claves adicionales en forma de diccionario.

    Returns:
        render_template:
            Renderiza el HTML del formulario para subir un enlace.
    """
    form = EnlaceForm()

    return render_template(
        "equipo/uploadFile.html",
        titulo="enlace",
        function="member.insert_link",
        form=form,
        id=member.id,
    )


@bp.post("/uploadLink/<int:member_id>")
@h.authenticated_route(module="equipo", permissions=("create",))
@validate_member_decorator
def insert_link(member, *args, **kwargs):
    """
    Sube un enlace a la base de datos a un miembro válido.

    Args:
        member:
            Miembro al cual se le va a subir un enlace.
        *args:
            Argumentos adicionales en forma de tupla.
        **kwargs:
            Argumentos claves adicionales en forma de diccionario.

    Returns:
        redirect:
            Redirecciona a la página para ver los archivos del miembro si se subió el enlace correctamente o hubo un error.

    Errores:
        Información de enlace incorrecta.
        Error subiendo el enlace a la base de datos.
    """
    params = request.form
    required = ["enlace", "titulo"]
    missing_fields = [field for field in required if not params.get(field)]
    if missing_fields:
        h.flash_error(f"Faltan campos requeridos")
        return redirect(url_for("member.upload_link", member_id=member.id))

    validation_rules = {
        "enlace": es_enlace_valido,
        "titulo": letras_y_numeros,
    }
    ok, errors = formulario_valido(params, validation_rules)
    if not ok:
        for field, error_list in errors.items():
            for error in error_list:
                h.flash_error(f"El campo {field} tiene un error: {error}")
                break
        return redirect(url_for("member.upload_link", member_id=member.id))

    form = EnlaceForm()
    if not form.validate_on_submit():
        h.flash_error("Información de enlace incorrecta")
        return redirect(url_for("member.show_files", member_id=member.id))

    file = {
        "titulo": form.titulo.data,
        "filename": "No se subió ningún archivo",
        "enlace": form.enlace.data,
        "tipo": "enlace",
    }

    try:
        ArchivoService.upload_file(member.id, **file)
        h.flash_success("Enlace subido correctamente")
    except Exception as e:
        print(e)
        h.flash_error("Error al subir el enlace")
    return redirect(url_for("member.show_files", member_id=member.id))


@bp.post("deleteFile/<int:member_id>/<int:archivo_id>")
@h.authenticated_route(module="equipo", permissions=("destroy",))
@validate_member_decorator
def delete_file(member, archivo_id: int):
    """
    Elimina físicamente un archivo de la base de datos de un miembro válido.

    Args:
        member:
            Miembro al cual se le va a eliminar un archivo.
        archivo_id: int
            ID del archivo a ser borrado.

    Returns:
        redirect:
            Redirecciona a la página para ver los archivos del miembro si se eliminó el archivo correctamente o hubo un error.

    Errores:
        Información de formulario incorrecta.
        Archivo no existente.
        Error al eliminar el archivo.
    """
    form = DeleteMemberForm()
    if not form.validate_on_submit():
        h.flash_error("Error")
        return redirect(url_for("member.show_files", member_id=member.id))

    archivo = ArchivoService.getArchivo(archivo_id)
    if not archivo:
        h.flash_error("Error al recuperar el archivo")
        return redirect(url_for("member.show_files", member_id=member.id))

    try:
        if archivo.tipo != "enlace":
            delete_file_minio(archivo)
        ArchivoService.borrarArchivoMiembro(archivo_id)
        h.flash_success("Se eliminó el archivo!")
    except Exception as e:
        print(e)
        h.flash_error("Error al eliminar el archivo")

    return redirect(url_for("member.show_files", member_id=member.id))


@bp.get("/editFile/<int:member_id>/<int:archivo_id>")
@h.authenticated_route(module="equipo", permissions=("update",))
@validate_member_decorator
def update_file(member, archivo_id: int):
    """
    Muestra el formulario para editar a un archivo de un miembro válido, con los campos llenos con su información.

    Args:
        member:
            Miembro del cual se va a editar un archivo.
        archivo_id: int
            ID del archivo a ser editado.

    Returns:
        render_template:
            Renderiza el HTML del formulario para editar el archivo.
        redirect:
            Muestra la página donde se muestran los archivos del miembro si hay un error al recuperar el archivo.
    """
    archivo = ArchivoService.getArchivo(archivo_id)
    if not archivo:
        h.flash_error("Error al recuperar el archivo")
        return redirect(url_for("member.show_files", member_id=member.id))

    if archivo.tipo == "enlace":
        form = EnlaceForm(obj=archivo)
    else:
        form = ArchivoMiembroForm(obj=archivo)

    return render_template(
        "equipo/editFile.html",
        form=form,
        archivo=archivo,
        member=member,
    )


@bp.post("/editFile/<int:member_id>/<int:archivo_id>")
@h.authenticated_route(module="equipo", permissions=("update",))
@validate_member_decorator
def insert_updated_file(member, archivo_id: int):
    """
    Edita un archivo de un miembro válido en la base de datos.

    Args:
        member:
            Miembro al cual se le va a editar un archivo.
        archivo_id: int
            ID del archivo a ser editado.

    Returns:
        redirect:
            Redirecciona a la página para ver los archivos del miembro si se editó el archivo correctamente o hubo un error en el formulario o recuperando el archivo.
            Redirecciona a la página de edición del archivo si hay un error en la base de datos.
    """
    archivo = ArchivoService.getArchivo(archivo_id)
    if not archivo:
        h.flash_error("Error al recuperar el archivo")
        return redirect(url_for("member.show_files", member_id=member.id))

    ok, errors = formulario_valido(
        request.form,
        validation_rules={
            "titulo": letras_y_numeros,
        },
    )
    if not ok:
        for field, error_list in errors.items():
            for error in error_list:
                h.flash_error(f"El campo {field} tiene un error: {error}")
                break
        return redirect(
            url_for("member.update_file", member_id=member.id, archivo_id=archivo.id)
        )

    if archivo.tipo == "enlace":
        form = EnlaceForm(obj=archivo)
    else:
        form = ArchivoMiembroForm(obj=archivo)
        del form.archivo

    if not form.validate_on_submit():
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error en el campo {field}: {error}")
        h.flash_error("Error con la información actualizada")
        return redirect(url_for("member.show_files", member_id=member.id))

    update = ArchivoService.editArchivo(archivo, form.titulo.data)
    if not update:
        h.flash_error("Error al actualizar")
        return redirect(
            url_for("member.update_file", member_id=member.id, archivo_id=archivo.id)
        )

    updated_type = "Enlace" if archivo.tipo == "enlace" else "Archivo"
    h.flash_success(f"{updated_type} actualizado exitosamente!")
    return redirect(url_for("member.show_files", member_id=member.id))


@bp.get("/downloadFile/<int:member_id>/<int:archivo_id>")
@h.authenticated_route(module="equipo", permissions=("show",))
@validate_member_decorator
def download_file(member, archivo_id: int):
    """
    Descarga un archivo de un miembro válido.

    Args:
        member:
            Miembro dueño del archivo a ser descargado.
        archivo_id: int
            ID del archivo a ser descargado.

    Returns:
        send_file:
            Descarga el archivo con su titulo y extensión.
        redirect:
            Redirecciona a la página donde se muestran los archivos del miembro si hay un error.
    """
    client = app.storage.client
    bucket_name = app.config["MINIO_BUCKET_NAME"]
    archivo = ArchivoService.getArchivo(archivo_id)
    if not archivo:
        h.flash_error("Error al recuperar el archivo")
        return redirect(url_for("member.show_files", member_id=member.id))

    try:
        extension = os.path.splitext(archivo.filename)[1]

        response = client.get_object(bucket_name, archivo.filename)

        file_data = io.BytesIO(response.read())
        response.close()
        response.release_conn()
        return send_file(
            file_data, download_name=f"{archivo.titulo}{extension}", as_attachment=True
        )
    except Exception as e:
        print(e)
        h.flash_error("Error al descargar el archivo")
        return redirect(url_for("member.show_files", member_id=member.id))
