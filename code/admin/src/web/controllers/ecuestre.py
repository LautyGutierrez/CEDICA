from web.forms.ecuestreForm import EcuestreForm, DeleteEcuestreForm
from web.forms.archivoForm import ArchivoEcuestreForm
from web.forms.enlaceForm import EnlaceForm
from src.core.ecuestre import EcuestreService as e
from src.core.archivos import ArchivoService as a
from src.core.ecuestre.ecuestreModel import Ecuestre
from src.core.archivos.archivo import Archivo
from src.web.forms.validators import formulario_valido
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    send_file,
)
from src.core.database import db
from src.web.controllers import _helpers as h
from flask import current_app as app
import os
from os import fstat
import urllib.parse
import io
from functools import wraps
from src.web.forms.validators import (
    solo_letras,
    solo_numeros,
    solo_fechas,
    solo_letras_caracteres,
    es_enlace_valido,
    es_raza_valida,
    es_sexo_valido,
    es_pelaje_valido,
    entrenador_valido,
    conductor_valido,
    )


bp = Blueprint("ecuestre", __name__, url_prefix="/ecuestre")

validation_rules = {
        "nombre": solo_letras,
        "fecha_nacimiento": solo_fechas,
        "fecha_ingreso": solo_fechas,
        "compra_o_donacion": solo_letras,
        "sede": solo_letras,
        "sexo_id": es_sexo_valido,
        "raza_id": es_raza_valida,
        "pelaje_id": es_pelaje_valido,
        "tipo_JA": solo_letras_caracteres,
        "entrenador": entrenador_valido,
        "conductor": conductor_valido,

    }

required_fields = [
    "nombre",
    "fecha_nacimiento",
    "fecha_ingreso",
    "compra_o_donacion",
    "sede",
    "sexo_id",
    "raza_id",
    "pelaje_id",
    "tipo_JA",
    "entrenador",
    "conductor",
]


def check_ecuestre(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ecuestre_id = kwargs.get("ecuestre_id")
        if (
            not ecuestre_id
            or not e.findEcuestreById(ecuestre_id)
            or e.findEcuestreById(ecuestre_id).borrado
        ):
            flash("Ecuestre no encontrado o eliminado.", "error")
            return redirect(url_for("ecuestre.show_ecuestre"))
        return f(*args, **kwargs)

    return decorated_function


@bp.get("/ecuestreRegister")
@h.authenticated_route(module="ecuestre", permissions=("create",))
def ecuestreRegister_get():
    """
    Muestra la página de registro del ecuestre, enviando una instancia del formulario del mismo.

    Returns:
        render_template:
            Renderiza la plantilla "ecuestre/ecuestreRegister.html" con una instancia del formulario EcuestreForm.
    """
    form = EcuestreForm()

    return render_template("ecuestre/ecuestreRegister.html", form=form)


@bp.post("/insertarTuplaEcuestre")
@h.authenticated_route(module="ecuestre", permissions=("create",))
def insertar_tupla_ecuestre():
    form = EcuestreForm()
    """
    Valida que los datos ingresados en el formulario sean correctos
    y en caso de ser válidos, crea un diccionario con los datos del formulario.


    Returns:
        render_template:
            Renderiza el formulario con la información del ecuestre registrado o con los errores si la validación falla.
    """
    filtered_validation_rules = {
        key: value
        for key, value in validation_rules.items()
    }
    ok, errors = formulario_valido(request.form, filtered_validation_rules)

    if ok:

        ecuestre = {
            "nombre": form.nombre.data,
            "fecha_nacimiento": form.fecha_nacimiento.data,
            "compra_o_donacion": form.compra_o_donacion.data,
            "fecha_ingreso": form.fecha_ingreso.data,
            "sede": form.sede.data,
            "sexo_id": form.sexo_id.data.id_sexo,
            "raza_id": form.raza_id.data.id_raza,
            "pelaje_id": form.pelaje_id.data.id_pelaje,
            "tipo_JA": form.tipo_JA.data,
            "entrenador": form.entrenador.data.id,
            "conductor": form.conductor.data.id,
        }
        try:
            """ 

            Llama a la función create_ecuestre del servicio de ecuestre,
            pasando el diccionario con los datos del formulario y muestra un mensaje de éxito
            o error segun corresponda.

            """
            e.create_ecuestre(**ecuestre)
            flash("Ecuestre registrado exitosamente.", "success")
            return redirect(url_for("ecuestre.show_ecuestre"))
        except Exception:
            return render_template("ecuestre/ecuestreRegister.html", form=form)
    else:
        """

        En el caso de no ser válido el formulario,
        se muestra nuevamente el formulario con los errores.
        
        """
        for field, error_list in errors.items():
            for error in error_list:
                flash(f"El campo {field} tiene un error: {error}", "error")

        return render_template("ecuestre/ecuestreRegister.html", form=form)


@bp.get("/showEcuestre")
@h.authenticated_route(
    module="ecuestre",
    permissions=(
        "show",
        "index",
    ),
)
def show_ecuestre():
    archivoform = ArchivoEcuestreForm()
    """
        Muestra la página de listado de ecuestres, obteniendo los parámetros de búsqueda,
        ordenamiento y paginación desde la URL.

        Returns:
            render_template:
                Renderiza la plantilla "ecuestre/showEcuestre.html" con los ecuestres filtrados,
                el formulario de ecuestre, el formulario de archivo, y los parámetros de paginación.
        """
    criterio = request.args.get("criterio", "")
    busqueda = request.args.get("busqueda", "")
    ordenar_por = request.args.get("ordenar_por", "nombre")
    orden = request.args.get("orden", "asc")
    tipo_JA = request.args.get("tipo_JA", "")

    page, per_page = h.url_pagination_args(default_per_page=10)

    if request.args.get("toggle_order"):
        orden = "desc" if orden == "asc" else "asc"

    #Mapea los criterios a los atributos del modelo
    criterios = {"nombre": Ecuestre.nombre, "tipoJA": Ecuestre.tipo_JA}

    #Mapea los campos de ordenamiento a los atributos del modelo
    campos_ordenamiento = {
        "nombre": Ecuestre.nombre,
        "fecha_nacimiento": Ecuestre.fecha_nacimiento,
        "fecha_ingreso": Ecuestre.fecha_ingreso,
    }

    """
    Obtiene el atributo y el campo de ordenamiento 
    correspondiente a los parametros de la url

    """
    atributo = criterios.get(criterio)
    campo_ordenamiento = campos_ordenamiento.get(ordenar_por, Ecuestre.nombre)

    """
    
    Realiza la consulta de los ecuestres realizando 
    segun corresponda la busqueda y el ordenamiento y se obtiene el total de ecuestres
    para la paginación.

    """
    ecuestres, total = e.doFilter(
        atributo, busqueda, orden, campo_ordenamiento, tipo_JA, page, per_page
    )

    form = EcuestreForm()
    return render_template(
        "ecuestre/showEcuestre.html",
        ecuestre=ecuestres,
        form=form,
        formarchivo=archivoform,
        page=page,
        per_page=per_page,
        total=total,
        criterio=criterio,
        busqueda=busqueda,
        ordenar_por=ordenar_por,
        orden=orden,
        tipo_JA=tipo_JA,
    )


@bp.get("/show_files/<int:ecuestre_id>")
@h.authenticated_route(
    module="ecuestre",
    permissions=(
        "show",
        "index",
    ),
)
@check_ecuestre
def show_files(ecuestre_id):
    #Mismo procedimiento que en show_ecuestre
    criterio = request.args.get("criterio", "")
    busqueda = request.args.get("busqueda", "")
    ordenar_por = request.args.get("ordenar_por", "nombre")
    orden = request.args.get("orden", "asc")
    tipo = request.args.get("tipo", "")
    page, per_page = h.url_pagination_args(default_per_page=10)
    if request.args.get("toggle_order"):
        orden = "desc" if orden == "asc" else "asc"

    criterios = {"titulo": Archivo.titulo, "tipo": Archivo.tipo}

    campos_ordenamiento = {
        "titulo": Archivo.titulo,
        "fecha_subida": Archivo.fecha_subida,
    }

    atributo = criterios.get(criterio)
    campo_ordenamiento = campos_ordenamiento.get(ordenar_por, Archivo.titulo)
    query, total = a.doFilterArchivo(
        atributo, busqueda, orden, campo_ordenamiento, tipo, ecuestre_id, page, per_page
    )
    #Se envia urrlib para codificar los nombres de los archivos
    return render_template(
        "ecuestre/showFiles.html",
        archivos=query,
        tipo=tipo,
        criterio=criterio,
        busqueda=busqueda,
        ordenar_por=ordenar_por,
        orden=orden,
        ecuestre=ecuestre_id,
        urllib=urllib,
        page=page,
        per_page=per_page,
        total=total,
        form=ArchivoEcuestreForm(),
    )


@bp.post("/deleteEcuestre/<int:ecuestre_id>")
@h.authenticated_route(module="ecuestre", permissions=("destroy",))
@check_ecuestre
def delete_ecuestre(ecuestre_id: int):
    """
        Elimina lógicamente al ecuestre recibido como parámetro a través de un POST.

        Returns:
            redirect:
                Redirige a la vista de listado de ecuestres después de eliminar el ecuestre.
    """
    form = DeleteEcuestreForm()
    if form.validate_on_submit():
        e.logical_delete_ecuestre(ecuestre_id)
        flash("Ecuestre eliminado exitosamente.", "success")
    return redirect(url_for("ecuestre.show_ecuestre"))


@bp.route("/editEcuestre/<int:ecuestre_id>", methods=["GET", "POST"])
@h.authenticated_route(module="ecuestre", permissions=("update",))
@check_ecuestre
def edit_ecuestre(ecuestre_id: int):
    ecuestre = e.findEcuestreById(ecuestre_id)
    form = EcuestreForm(obj=ecuestre)
    """
    Muestra la página de edición de un ecuestre, enviando los datos correspondientes
    a diferentes select para poder mostrar el que tiene actualmente cargado el ecuestre a editar.

    Args:
        ecuestre_id (int): ID del ecuestre a editar.

    Returns:
        render_template:
            Renderiza la plantilla "ecuestre/editEcuestre.html" con el formulario de edición
            y los datos del ecuestre a editar.
    """
    pelajes = [(pelaje.id_pelaje, pelaje.descripcion)
               for pelaje in e.getPelajes()]
    razas = [(raza.id_raza, raza.descripcion) for raza in e.getRazas()]
    sexos = [(sexo.id_sexo, sexo.descripcion) for sexo in e.getSexos()]
    conductores = [(conductor.id, conductor.nombre)
                   for conductor in e.getConductores()]
    entrenadores = [
        (entrenador.id, entrenador.nombre) for entrenador in e.getEntrenadores()
    ]

    return render_template(
        "ecuestre/editEcuestre.html",
        form=form,
        ecuestre=ecuestre,
        pelajes=pelajes,
        razas=razas,
        sexos=sexos,
        conductores=conductores,
        entrenadores=entrenadores,
    )


@bp.post("/updateEcuestre/<int:ecuestre_id>")
@h.authenticated_route(module="ecuestre", permissions=("update",))
@check_ecuestre
def update_ecuestre(ecuestre_id: int):
    ecuestre = e.findEcuestreById(ecuestre_id)
    """
    Actualiza el ecuestre con los datos del formulario, informando el éxito o error de la operación.

    Args:
        ecuestre_id (int): ID del ecuestre a actualizar.

    Returns:
        redirect:
            Redirige a la vista de listado de ecuestres después de actualizar el ecuestre,
            o redirige a la vista de edición del ecuestre si hay errores en el formulario.
    """
    filtered_validation_rules = {
        key: value
        for key, value in validation_rules.items()
    }
    ok, errors = formulario_valido(request.form, filtered_validation_rules)

    if ok:
          editado = e.editEcuestre(ecuestre, request.form)
          if editado:
               flash("Ecuestre actualizado exitosamente.", "success")
          else:
               flash("No se pudo actualizar el ecuestre: ", "error")
    else:
        for field, error_list in errors.items():
            for error in error_list:
                flash(f"El campo {field} tiene un error: {error}", "error")
        return redirect(url_for("ecuestre.edit_ecuestre", ecuestre_id=ecuestre_id))
    return redirect(url_for("ecuestre.show_ecuestre"))


@bp.get("/download_file/<int:file_id>")
@h.authenticated_route(
    module="ecuestre",
    permissions=(
        "show",
        "index",
    ),
)
def download_file(file_id):
    client = app.storage.client
    bucket_name = app.config["MINIO_BUCKET_NAME"]
    """
    Genera una descarga desde MinIO del archivo correspondiente al ID recibido.

    Args:
        file_id (int): ID del archivo a descargar.

    Returns:
        send_file:
            Envía el archivo para ser descargado.
        str:
            Mensaje de error si ocurre un problema durante la descarga.
    """
    archivo = a.getArchivo(file_id)

    try:
        #Se descarga el archivo desde minio
        response = client.get_object(bucket_name, archivo.filename)
        extension = os.path.splitext(archivo.filename)[1]

        #Se guarda el archivo en un buffer
        file_data = io.BytesIO(response.read())
        response.close()
        response.release_conn()

        #Se envia el archivo para ser descargado
        return send_file(file_data, download_name=f"{archivo.titulo}{extension}", as_attachment=True)
    except Exception:
        return f"Error al descargar el archivo", 500


def save_file_minio(file, name):
    #Se sube el archivo a minio
    client = app.storage.client
    bucket_name = app.config["MINIO_BUCKET_NAME"]

    size = fstat(file.fileno()).st_size
    filename = name
    client.put_object(bucket_name, filename, file, size,
                      content_type=file.content_type)


def insertar_tupla_archivo(file, ecuestreID):
    """
    Inserta una tupla en la tabla archivo y archivo_ecuestre, almacenando en el campo de filename
    la concatenación del nombre real del archivo junto al ID del ecuestre al que pertenece,
    tal como se guardó en MinIO. Se deja registro que no se subió un enlace.

    Args:
        file (dict): Diccionario con los datos del archivo a guardar.
        ecuestreID (int): ID del ecuestre al que pertenece el archivo.

    Returns:
        None
    """

    arch = a.saveFile(**file)
    a.saveFileEcuestre(arch.id, ecuestreID)


@bp.get("/edit_files/<int:file_id>/<int:ecuestre_id>")
@check_ecuestre
@h.authenticated_route(module="ecuestre", permissions=("update",))
def edit_file(file_id, ecuestre_id):
    archivo = a.getArchivo(file_id)
    """
    Obtiene el tipo del archivo para renderizar el formulario correspondiente.

    Args:
        file_id (int): ID del archivo a editar.
        ecuestre_id (int): ID del ecuestre al que pertenece el archivo.

    Returns:
        render_template:
            Renderiza la plantilla "ecuestre/editFile.html" con el formulario correspondiente
            y los datos del archivo y del ecuestre.
    """
    tipo = archivo.tipo
    if tipo == "enlace":
        form = EnlaceForm(obj=archivo)
    else:
        form = ArchivoEcuestreForm(obj=archivo)

    return render_template(
        "ecuestre/editFile.html", form=form, archivo=archivo, ecuestre=ecuestre_id
    )


@bp.post("/updateFile/<int:file_id>/<int:ecuestre_id>")
@check_ecuestre
@h.authenticated_route(module="ecuestre", permissions=("update",))
def update_file(file_id, ecuestre_id):
    archivo = a.getArchivo(file_id)
    tipo = archivo.tipo
    """
    Actualiza el archivo con los datos del formulario, informando el éxito o error de la operación.

    Args:
        file_id (int): ID del archivo a actualizar.
        ecuestre_id (int): ID del ecuestre al que pertenece el archivo.

    Returns:
        redirect:
            Redirige a la vista de listado de archivos después de actualizar el archivo,
            o redirige a la vista de edición del archivo si hay errores en el formulario.
    """
    if tipo == "enlace":
        form = EnlaceForm()
    else:
        form = ArchivoEcuestreForm()
        del form.archivo

    ok, errors = formulario_valido(request.form, validation_rules={
        "titulo": solo_letras_caracteres,
    })
    
    if ok:
        """
        
        Se actualiza el archivo con los datos del formulario.
        En el caso de haber error, se informa al usuario.
        
        """
        titulo = form.titulo.data

        editado = a.editArchivo(archivo, titulo)

        if editado:
            if tipo == "enlace":
                flash("Enlace actualizado exitosamente.", "success")
            else:
                flash("Archivo actualizado exitosamente.", "success")
        else:
            flash("No se pudo actualizar el archivo: " + str(e), "error")
        return redirect(url_for("ecuestre.show_files", ecuestre_id=ecuestre_id))
    else:
        for field, error_list in errors.items():
            for error in error_list:
                flash(f"El campo {field} tiene un error: {error}", "error")
    return render_template(
        "ecuestre/editFile.html", form=form, archivo=archivo, ecuestre=ecuestre_id
    )


@bp.get("/subir_documento/<int:ecuestre_id>")
@check_ecuestre
@h.authenticated_route(module="ecuestre", permissions=("create",))
def subir_documento(ecuestre_id):
    """
    Renderiza el formulario de archivos para subir un documento.

    Args:
        ecuestre_id (int): ID del ecuestre al que se le va a subir el documento.

    Returns:
        render_template:
            Renderiza la plantilla "ecuestre/subirDocumento.html" con el formulario de archivos
            y los errores del formulario si los hay.
    """
    archivoform = ArchivoEcuestreForm()
    return render_template(
        "ecuestre/subirDocumento.html",
        form=archivoform,
        ecuestre=ecuestre_id,
        form_errors=archivoform.errors,
    )


@bp.get('/subir_enlace/<int:ecuestre_id>')
@check_ecuestre
@h.authenticated_route(module="ecuestre", permissions=("create",))
def subir_enlace(ecuestre_id):
    """
    Renderiza el formulario de enlace para subir un enlace.

    Args:
        ecuestre_id (int): ID del ecuestre al que se le va a subir el enlace.

    Returns:
        render_template:
            Renderiza la plantilla "ecuestre/subirEnlace.html" con el formulario de enlace
            y los errores del formulario si los hay.
    """
    enlaceform = EnlaceForm()
    return render_template(
        "ecuestre/subirEnlace.html",
        form=enlaceform,
        ecuestre=ecuestre_id,
        form_errors=enlaceform.errors,
    )


@bp.post("/insertar_documento/<int:ecuestre_id>")
@h.authenticated_route(module="ecuestre", permissions=("create",))
@check_ecuestre
def upload_file(ecuestre_id):
    archivoform = ArchivoEcuestreForm()
    """
    Valida el formulario y sube el archivo a MinIO, registrándolo en la base de datos.

    Args:
        ecuestre_id (int): ID del ecuestre al que se le va a subir el documento.

    Returns:
        redirect:
            Redirige a la vista de listado de archivos después de subir el archivo,
            o redirige a la vista de subir documento si hay errores en el formulario.
    """
    
    ok, errors = formulario_valido(request.form, validation_rules={
        "titulo": solo_letras_caracteres,
        "tipo_archivo": solo_letras_caracteres,

    })
    if "archivo" not in request.files or request.files["archivo"].filename == "":
        ok = False
    if ok:
        archivo = {
            "titulo": archivoform.titulo.data,
            "filename": f"{ecuestre_id}_{request.files['archivo'].filename}",
            "enlace": "No se subió un enlace",
            "tipo": archivoform.tipo_archivo.data,
        }
        insertar_tupla_archivo(archivo, ecuestre_id)
        save_file_minio(request.files["archivo"], archivo["filename"])
        flash("Archivo subido exitosamente.", "success")
        return redirect(url_for("ecuestre.show_files", ecuestre_id=ecuestre_id))
    else:
        """
        
        En el caso de no ser válido el formulario, se
        informa al usuario de los errores.
        
        """
        for field, errors in errors.items():
            for error in errors:
                flash(
                    f"Error en el campo {getattr(archivoform, field).label.text}: {error}",
                    "error",
                )
        return redirect(url_for("ecuestre.subir_documento", ecuestre_id=ecuestre_id))


@bp.post("/subir_enlace/<int:ecuestre_id>")
@h.authenticated_route(module="ecuestre", permissions=("create",))
@check_ecuestre
def upload_enlace(ecuestre_id):
    form = EnlaceForm()

    """
    Valida el formulario y sube el enlace a la base de datos.

    Args:
        ecuestre_id (int): ID del ecuestre al que se le va a subir el enlace.

    Returns:
        redirect:
            Redirige a la vista de listado de archivos después de subir el enlace,
            o redirige a la vista de subir enlace si hay errores en el formulario.
    """
    ok, errors = formulario_valido(request.form, validation_rules={
        "titulo": solo_letras_caracteres,
        "enlace": es_enlace_valido,
    })
    if ok:
        #Se sube el enlace a la base de datos.
        insertar_tupla_enlace(ecuestre_id, form)
        flash("Enlace subido exitosamente.", "success")
        return redirect(url_for("ecuestre.show_files", ecuestre_id=ecuestre_id))
    else:
        """
        
        En el caso de no ser válido el formulario, se
        informa al usuario de los errores.
        
        """
        for field, errors in errors.items():
            for error in errors:
                flash(
                    f"Error en el campo {getattr(form, field).label.text}: {error}",
                    "error",
                )
        return redirect(url_for("ecuestre.subir_enlace", ecuestre_id=ecuestre_id))


@bp.post("/delete_file/<int:file_id>/<int:ecuestre_id>")
@h.authenticated_route(module="ecuestre", permissions=("destroy",))
@check_ecuestre
def delete_file(file_id, ecuestre_id):
    """
    Elimina el archivo de MinIO y de la base de datos físicamente.

    Args:
        file_id (int): ID del archivo a eliminar.
        ecuestre_id (int): ID del ecuestre al que pertenece el archivo.

    Returns:
        redirect:
            Redirige a la vista de listado de archivos después de eliminar el archivo.
    """
    archivo = a.getArchivo(file_id)
    filename = archivo.filename
    client = app.storage.client
    bucket_name = app.config["MINIO_BUCKET_NAME"]
    client.remove_object(bucket_name, filename)
    a.borrarArchivoEcuestre(file_id)
    flash("Archivo eliminado exitosamente.", "success")
    return redirect(url_for("ecuestre.show_files", ecuestre_id=ecuestre_id))


@bp.post("/delete_enlace/<int:file_id>/<int:ecuestre_id>")
@h.authenticated_route(module="ecuestre", permissions=("destroy",))
@check_ecuestre
def delete_enlace(file_id, ecuestre_id):
    """
    Elimina el enlace de la base de datos físicamente.

    Args:
        file_id (int): ID del enlace a eliminar.
        ecuestre_id (int): ID del ecuestre al que pertenece el enlace.

    Returns:
        redirect:
            Redirige a la vista de listado de archivos después de eliminar el enlace.
    """
    a.borrarArchivoEcuestre(file_id)
    flash("Enlace eliminado exitosamente.", "success")
    return redirect(url_for("ecuestre.show_files", ecuestre_id=ecuestre_id))


def insertar_tupla_enlace(ecuestreID, form):
    """
    Inserta una tupla en la tabla archivo y archivo_ecuestre, correspondiente a un enlace.
    En este caso se completará el campo 'enlace' con el enlace recibido en el formulario
    y en 'filename' se deja registro de que no se subió un archivo.

    Args:
        ecuestreID (int): ID del ecuestre al que pertenece el enlace.
        form (Form): Formulario con los datos del enlace a guardar.

    Returns:
        None
    """
    enlace = {
        "titulo": form.titulo.data,
        "enlace": form.enlace.data,
        "filename": "No se subió un archivo",
        "tipo": "enlace",
    }
    enlaceSaved = a.saveFile(**enlace)
    a.saveFileEcuestre(enlaceSaved.id, ecuestreID)
