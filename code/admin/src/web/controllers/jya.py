from src.web.forms.archivoForm import ArchivoJyAForm
from src.web.forms.enlaceForm import EnlaceJyAForm
from src.core.archivos.archivo import Archivo
from src.core.archivos import ArchivoService
from flask import (Blueprint, flash, redirect, render_template,
                   request, url_for, send_file)
from functools import wraps
from src.web.forms.jya import (JyAForm, DeleteJyAForm, JyAUpdateForm,
                               TutorUpdateForm, Tutor2UpdateForm, InstitucionEscolarUpdateForm)
from src.core.database import db
from src.core.jya import (JyA, InstitucionEscolar, Tutor, JyATutors, ServiceJyA as s)
from src.web.controllers import _helpers as h
import urllib.parse
from flask import current_app as app
import os
import io
from src.web.forms.validators import (
    formulario_valido,
    solo_letras,
    solo_numeros,
    solo_fechas,
)

bp = Blueprint("jya", __name__)

validation_rules={
    "name": solo_letras,
    "lastname": solo_letras,
    "document_number": solo_numeros,
    "age": solo_numeros,
    "birthdate": solo_fechas,
    "phone_number": solo_numeros,
    "emergy_contact": solo_letras,
    "phone_number_emergy": solo_numeros,
    "with_what_diagnosis": solo_letras,
    "disability_type": solo_letras,
    "allowance_type": solo_letras,
    "pension_type": solo_letras,
    "social_work": solo_letras,
    "affiliation_number": solo_numeros,
    "professionals": solo_letras,
    "institutional_work_proposal": solo_letras,
    "institution_phone_number": solo_numeros,
    "tutor_relationship": solo_letras,
    "tutor_name": solo_letras,
    "tutor_lastname": solo_letras,
    "tutor_document_number": solo_numeros,
    "tutor_phone_number": solo_numeros,
    "tutor_educational_level": solo_letras,
    "tutor_activity": solo_letras,
    "tutor_relationship2": solo_letras,
    "tutor_name2": solo_letras,
    "tutor_lastname2": solo_letras,
    "tutor_document_number2": solo_numeros,
    "tutor_phone_number2": solo_numeros,
    "tutor_educational_level2": solo_letras,
    "tutor_activity2": solo_letras,
}

optionals = [
    "is_scholarship_holder",
    "observations",
    "has_a_disability_certificate",
    "with_what_diagnosis",
    "other",
    "has_allowance",
    "allowance_type",
    "has_a_pension",
    "pension_type",
    "social_work",
    "affiliation_number",
    "has_conservatorship",
    "social_work_observation",
    "institution_observations",
    "tutor_relationship2",
    "tutor_name2",
    "tutor_lastname2",
    "tutor_document_number2",
    "tutor_phone_number2",
    "tutor_educational_level2",
    "tutor_activity2",
    "tutor_home_address2",
    "tutor_email2"
]

@bp.get("/jya-register")
@h.authenticated_route(module="jinete-y-amazona", permissions=("create",))
def register_jya_get():
    """
    Renderiza el formulario para registrar el legajo de un jinete o amazona.

    Returns:
        render_template: Renderiza el HTML con el formulario `JyAForm`.
    """
    jya_form = JyAForm()
    return render_template('jya/jya-register.html', form=jya_form, longitud=len(jya_form.data))


@bp.post("/insertar-jya")
@h.authenticated_route(module="jinete-y-amazona", permissions=("create",))
def register_jya_post():
    """
    Registra a un nuevo Jinete/Amazona (JyA) en la base de datos, validando la información ingresada en el formulario.
    
    Returns:
        redirect:
            Redirecciona a la página de listado de JyA si el registro es exitoso.
            Redirecciona al formulario de registro en caso de error.
    
    Raises:
        Exception:
            Si ocurre un error en la creación del JyA, institución, o tutor en la base de datos.
    
    Errores:
        Si el JyA ya existe en la base de datos.
        Si el tutor 1 o el tutor 2 ya existen con el mismo correo electrónico en la base de datos.
        Si no se pudo crear la institución o el tutor.
        Si la información del formulario no es válida.
    """
    jya_form = JyAForm()
    
    params = request.form
    filtered_validation_rules = {
        key: value
        for key, value in validation_rules.items()
        if key not in optionals or params.get(key)
    }
    ok, errors = formulario_valido(params, filtered_validation_rules)
   
    if ok:
        if s.exist_jya(jya_form.document_number.data):
            h.flash_error("El Jinete/Amazona ya existe")
            return redirect(url_for("jya.register_jya_get"))

        institucion_data = {
            "institution_name": jya_form.institution_name.data,
            "institution_address": jya_form.institution_address.data,
            "institution_phone_number": jya_form.institution_phone_number.data
        }
        
        institucion = s.get_or_create_institution(**institucion_data)
        if not institucion:
            h.flash_error("No se pudo crear la institución")
            return redirect(url_for("jya.register_jya_get"))
        
        jya_data = {
            "name": jya_form.name.data,
            "lastname": jya_form.lastname.data,
            "document_number": jya_form.document_number.data,
            "age": jya_form.age.data,
            "birthdate": jya_form.birthdate.data,
            "place_of_birth": jya_form.place_of_birth.data,
            "current_address": jya_form.current_address.data,
            "phone_number": jya_form.phone_number.data,
            "emergy_contact": jya_form.emergy_contact.data,
            "phone_number_emergy": jya_form.phone_number_emergy.data,
            "is_scholarship_holder": jya_form.is_scholarship_holder.data,
            "observations": jya_form.observations.data,
            "has_a_disability_certificate": jya_form.has_a_disability_certificate.data,
            "with_what_diagnosis": jya_form.with_what_diagnosis.data,
            "other": jya_form.other.data,
            "disability_type": jya_form.disability_type.data,
            "has_allowance": jya_form.has_allowance.data,
            "allowance_type": jya_form.allowance_type.data,
            "has_a_pension": jya_form.has_a_pension.data,
            "pension_type": jya_form.pension_type.data,
            "social_work": jya_form.social_work.data,
            "affiliation_number": jya_form.affiliation_number.data,
            "has_conservatorship": jya_form.has_conservatorship.data,
            "social_work_observation": jya_form.social_work_observation.data,
            "professionals": jya_form.professionals.data,
            "fk_institution_id": institucion.id,
            "current_year_institution": jya_form.institution_current_year.data,
            "institution_observations": jya_form.institution_observations.data,
            "institutional_work_proposal": jya_form.institutional_work_proposal.data,
            "condition": jya_form.condition.data,
            "headquarters": jya_form.headquarters.data,
            "days": jya_form.days.data,
            "teacher_or_therapist": jya_form.teacher_or_therapist.data.id,
            "horse": jya_form.horse.data.id,
            "horse_driver": jya_form.horse_driver.data.id,
            "runway_assistant": jya_form.runway_assistant.data.id
        }
        
        jya = s.create_jya(**jya_data)
        if not jya:
            h.flash_error("No se pudo crear al jinete/amazona")
            return redirect(url_for("jya.register_jya_get"))
        
        tutor1_data = {
            "tutor_relationship": jya_form.tutor_relationship.data,
            "tutor_name": jya_form.tutor_name.data,
            "tutor_lastname": jya_form.tutor_lastname.data,
            "tutor_document_number": jya_form.tutor_document_number.data,
            "tutor_home_address": jya_form.tutor_home_address.data,
            "tutor_phone_number": jya_form.tutor_phone_number.data,
            "tutor_email": jya_form.tutor_email.data,
            "tutor_educational_level": jya_form.tutor_educational_level.data,
            "tutor_activity": jya_form.tutor_activity.data
        }
        if not s.compare_tutors(**tutor1_data):
            h.flash_error("Ya existe un tutor con ese mail")
            return redirect(url_for("jya.register_jya_get"))
       
        tutor1 = s.get_or_create_tutor(**tutor1_data)
        if not tutor1:
            h.flash_error("No se pudo crear al tutor")
            return redirect(url_for("jya.register_jya_get"))
        
        if all([
            jya_form.tutor_relationship2,
            jya_form.tutor_name2.data,
            jya_form.tutor_lastname2.data,
            jya_form.tutor_document_number2.data,
            jya_form.tutor_home_address2.data,
            jya_form.tutor_phone_number2.data,
            jya_form.tutor_email2.data,
            jya_form.tutor_educational_level2.data,
            jya_form.tutor_activity2.data]
        ):
            tutor2_data = {
                "tutor_relationship": jya_form.tutor_relationship2.data,
                "tutor_name": jya_form.tutor_name2.data,
                "tutor_lastname": jya_form.tutor_lastname2.data,
                "tutor_document_number": jya_form.tutor_document_number2.data,
                "tutor_home_address": jya_form.tutor_home_address2.data,
                "tutor_phone_number": jya_form.tutor_phone_number2.data,
                "tutor_email": jya_form.tutor_email2.data,
                "tutor_educational_level": jya_form.tutor_educational_level2.data,
                "tutor_activity": jya_form.tutor_activity2.data
            }
            tutor2 = s.get_or_create_tutor(**tutor2_data)
            if not tutor2:
                h.flash_error("No se pudo crear al tutor 2")
                return redirect(url_for("jya.register_jya_get"))
            jya_tutor_data = {
                "jya_id": jya.id,
                "tutor_id1": tutor1.id,
                "tutor_id2": tutor2.id
            }
        else:
            tutor2 = None
            jya_tutor_data = {
                "jya_id": jya.id,
                "tutor_id1": tutor1.id,
                "tutor_id2": tutor2
            }

        jya_tutor = s.create_jya_tutor(**jya_tutor_data)
        if not jya_tutor:
            h.flash_error("Hubo un error interno")
            return redirect(url_for("jya.register_jya_get"))
        flash("Jinete/Amazona registrado exitosamente.", "success")
    else:
        """
        En el caso de no ser válido el formulario,
        se muestra nuevamente el formulario con los errores.
        """
        for field, error_list in errors.items():
            for error in error_list:
                flash(f"El campo {field} tiene un error: {error}", "error")

        return render_template('jya/jya-register.html', form=jya_form, longitud=len(jya_form.data))
    return redirect(url_for("jya.jya_list_view"))


@bp.get("/jya-list")
@h.authenticated_route(module="jinete-y-amazona", permissions=("index", "show",))
def jya_list_view():
    """
    Renderiza la tabla para mostrar los legajos de los jinetes y amazonas (JyA), 
    con sus filtros, orden y paginación.

    Returns:
        render_template:
            Renderiza la plantilla jya/jya-show.html con la lista de jinetes/amazonas filtrada, 
            ordenada y paginada.

    Args:
        criterio (str): Criterio de búsqueda (nombre, apellido, número de documento, o profesionales).
        busqueda (str): Término a buscar en el campo especificado por el criterio.
        ordenar_por (str): Campo por el cual se ordenarán los resultados (nombre o apellido).
        orden (str): Dirección del orden (ascendente o descendente).
        page (int): Número de página a mostrar en la paginación.
        per_page (int): Cantidad de registros a mostrar por página.

    Raises:
        Exception:
            Si ocurre un error en el filtrado o paginación de los datos.

    Errores:
        Si los datos de criterio, búsqueda u ordenamiento no son válidos.
        Si ocurre un problema en la consulta a la base de datos.
    """
    criterio = request.args.get('criterio', '')
    busqueda = request.args.get('busqueda', '')
    ordenar_por = request.args.get('ordenar_por', 'nombre')
    orden = request.args.get('orden', 'asc')
    page, per_page = h.url_pagination_args(default_per_page=10)
    if request.args.get('toggle_order'):
        orden = 'desc' if orden == 'asc' else 'asc'

    criterios = {
        'name': JyA.name,
        'lastname': JyA.lastname,
        'document_number': JyA.document_number,
        'professionals': JyA.professionals
    }

    campos_ordenamiento = {
        'name': JyA.name,
        'lastname': JyA.lastname,
    }

    atributo = criterios.get(criterio)
    campo_ordenamiento = campos_ordenamiento.get(ordenar_por, JyA.name)

    if atributo:
        jya = s.do_filter(atributo, busqueda, orden, campo_ordenamiento)
    else:
        jya = s.all_jya()
    form = JyAForm()
    total = len(jya)
    start = (page - 1) * per_page
    end = start + per_page
    jya = jya[start:end]

    return render_template(
        "jya/jya-show.html",
        jya=jya,
        form=form,
        page=page,
        per_page=per_page,
        total=total,
        criterio=criterio,
        busqueda=busqueda,
        ordenar_por=ordenar_por,
        orden=orden,
        urllib=urllib
    )


@bp.post("/jya-delete/<int:id>")
@h.authenticated_route(module="jinete-y-amazona", permissions=("destroy",))
def delete_jya(id: int):
    """
    Valida el formulario de eliminación de un legajo y borra el registro correspondiente.

    Args:
        id (int): ID del jinete/amazona a eliminar.

    Returns:
        redirect:
            Redirecciona a la vista de lista de jinetes/amazonas si la eliminación es exitosa.

    Errores:
        Si el formulario de eliminación no es válido.
        Si el registro a eliminar no existe en la base de datos.
    """
    form = DeleteJyAForm()
    if form.validate_on_submit():
        s.logical_delete_jya(id)
        flash("Jitene/Amazona eliminado exitosamente.", "success")
    return redirect(url_for('jya.jya_list_view'))


@bp.route('/jya-edit/<int:id>', methods=['GET', 'POST'])
@h.authenticated_route(module="jinete-y-amazona", permissions=("update",))
def edit_jya(id: int):
    """
    Renderiza el formulario de edición para los datos del jinete/amazona, mostrando la información precargada.

    Args:
        id (int): ID del jinete/amazona a editar.

    Returns:
        render_template: 
            Renderiza la plantilla 'jya/jya-edit.html' con los datos del formulario de edición.

    Raises:
        Exception:
            Si ocurre un error al consultar la información del jinete/amazona o sus tutores.

    Errores:
        Si el ID no corresponde a ningún jinete/amazona existente en la base de datos.
        Si la consulta de tutores o institución falla.
        Si la información precargada del formulario es inválida.
    """
    jya = JyA.query.get(id)
    jya = jya if jya != None else JyA()
    jya_tutor = s.get_tutors_by_jya(id)
    jya_tutors = jya_tutor if jya_tutor != None else JyATutors()
    tutor1 = Tutor.query.get(
        jya_tutors.tutor_id1) if jya_tutors.tutor_id1 else Tutor()
    tutor2 = Tutor.query.get(
        jya_tutors.tutor_id2) if jya_tutors.tutor_id2 else Tutor()
    institucion = InstitucionEscolar.query.get(
        jya.fk_institution_id) if jya.fk_institution_id else InstitucionEscolar()
    form = JyAForm(
        name=jya.name,
        lastname=jya.lastname,
        document_number=jya.document_number,
        age=jya.age,
        birthdate=jya.birthdate,
        place_of_birth=jya.place_of_birth,
        current_address=jya.current_address,
        phone_number=jya.phone_number,
        emergy_contact=jya.emergy_contact,
        phone_number_emergy=jya.phone_number_emergy,
        is_scholarship_holder=jya.is_scholarship_holder,
        observations=jya.observations,
        has_a_disability_certificate=jya.has_a_disability_certificate,
        with_what_diagnosis=jya.with_what_diagnosis,
        other=jya.other,
        disability_type=jya.disability_type,
        has_allowance=jya.has_allowance,
        allowance_type=jya.allowance_type,
        has_a_pension=jya.has_a_pension,
        pension_type=jya.pension_type,
        social_work=jya.social_work,
        affiliation_number=jya.affiliation_number,
        has_conservatorship=jya.has_conservatorship,
        social_work_observation=jya.social_work_observation,
        professionals=jya.professionals,
        tutor_relationship=tutor1.tutor_relationship,
        tutor_name=tutor1.tutor_name,
        tutor_lastname=tutor1.tutor_lastname,
        tutor_document_number=tutor1.tutor_document_number,
        tutor_home_address=tutor1.tutor_home_address,
        tutor_phone_number=tutor1.tutor_phone_number,
        tutor_email=tutor1.tutor_email,
        tutor_educational_level=tutor1.tutor_educational_level,
        tutor_activity=tutor1.tutor_activity,
        tutor_relationship2=tutor2.tutor_relationship,
        tutor_name2=tutor2.tutor_name,
        tutor_lastname2=tutor2.tutor_lastname,
        tutor_document_number2=tutor2.tutor_document_number,
        tutor_home_address2=tutor2.tutor_home_address,
        tutor_phone_number2=tutor2.tutor_phone_number,
        tutor_email2=tutor2.tutor_email,
        tutor_educational_level2=tutor2.tutor_educational_level,
        tutor_activity2=tutor2.tutor_activity,
        institution_name=institucion.institution_name,
        institution_address=institucion.institution_name,
        institution_phone_number=institucion.institution_phone_number,
        institution_current_year=jya.current_year_institution,
        institution_observations=jya.institution_observations,
        institutional_work_proposal=jya.institutional_work_proposal,
        condition=jya.condition,
        headquarters=jya.headquarters,
        days=jya.days,
        teacher_or_therapist=jya.teacher_or_therapist,
        horse_driver=jya.horse_driver,
        horse=jya.horse,
        runway_assistant=jya.runway_assistant
    )
    return render_template("jya/jya-edit.html", form=form, jya=jya, tutor1=tutor1, tutor2=tutor2, i=institucion, longitud=len(form.data))


@bp.post('/jya-update/<int:id>')
@h.authenticated_route(module="jinete-y-amazona", permissions=("update",))
def update_jya(id: int):
    """
    Actualiza los datos editados de un jinete/amazona, sus tutores, e institución escolar.

    Args:
        id (int): ID del jinete/amazona a actualizar.

    Returns:
        render_template o redirect: 
            Redirige a la vista de lista de jinetes/amazonas si se actualiza correctamente.
            En caso de error en la validación, se renderiza la página de edición con los mensajes de error.
    """
    params = request.form
    filtered_validation_rules = {
        key: value
        for key, value in validation_rules.items()
        if key not in optionals or params.get(key)
    }
    ok, errors = formulario_valido(params, filtered_validation_rules)
    #ok, errors = formulario_valido_opcional(request.form, validation_rules, optionals)
    form = JyAForm()
    jya = JyA.query.get(id)
    jya_tutors = s.get_tutors_by_jya(jya.id)
    tutor1 = Tutor.query.get(jya_tutors.tutor_id1)
    tutor2 = Tutor.query.get(
        jya_tutors.tutor_id2) if jya_tutors.tutor_id2 else None
    institucion = InstitucionEscolar.query.get(jya.fk_institution_id)
    if ok:
        jya_update_form = JyAUpdateForm(request.form)
        s.edit_jya_data(jya, jya_update_form)

        tutor1_update_form = TutorUpdateForm(request.form)
        s.edit_tutor1(tutor1, tutor1_update_form)

        tutor2_update_form = Tutor2UpdateForm(request.form)
        if tutor2 is None:
            if all([
                tutor2_update_form.tutor_relationship2,
                tutor2_update_form.tutor_name2.data,
                tutor2_update_form.tutor_lastname2.data,
                tutor2_update_form.tutor_document_number2.data,
                tutor2_update_form.tutor_home_address2.data,
                tutor2_update_form.tutor_phone_number2.data,
                tutor2_update_form.tutor_email2.data,
                tutor2_update_form.tutor_educational_level2.data,
                tutor2_update_form.tutor_activity2.data]
            ):
                tutor2_data = {
                    "tutor_relationship": tutor2_update_form.tutor_relationship2.data,
                    "tutor_name": tutor2_update_form.tutor_name2.data,
                    "tutor_lastname": tutor2_update_form.tutor_lastname2.data,
                    "tutor_document_number": tutor2_update_form.tutor_document_number2.data,
                    "tutor_home_address": tutor2_update_form.tutor_home_address2.data,
                    "tutor_phone_number": tutor2_update_form.tutor_phone_number2.data,
                    "tutor_email": tutor2_update_form.tutor_email2.data,
                    "tutor_educational_level": tutor2_update_form.tutor_educational_level2.data,
                    "tutor_activity": tutor2_update_form.tutor_activity2.data
                }
                tutor2 = s.get_or_create_tutor(**tutor2_data)
                jya_tutors.tutor_id2 = tutor2.id
        else:
            s.edit_tutor2(tutor2, tutor2_update_form)

        institucion_update_form = InstitucionEscolarUpdateForm(request.form)
        okey = s.edit_institution(institucion, institucion_update_form)
        if okey:
            flash("Jinete/Amazona actualizado exitosamente.", "success")
            return redirect(url_for('jya.jya_list_view', id=id))
    else:
        for field, error_list in errors.items():
            for error in error_list:
                flash(f"El campo {field} tiene un error: {error}", "error")
    return render_template("jya/jya-edit.html", form=form, jya=jya, tutor1=tutor1, tutor2=tutor2, i=institucion, longitud=len(form.data))


@bp.get('/download_jya_file/<id>/<filename>')
@h.authenticated_route(module="jinete-y-amazona", permissions=("index", "show",))
def download_file_jya(filename, id):
    """
    Descarga un documento desde MinIO con su título y extensión adecuados.

    Args:
        filename (str): El nombre del archivo a descargar.
        id (int): ID del archivo en la base de datos.

    Returns:
        send_file o tuple: 
            Retorna el archivo como adjunto para su descarga si se encuentra.
            En caso de error, retorna un mensaje y un código de estado 500.
    """
    client = app.storage.client
    bucket_name = app.config['MINIO_BUCKET_NAME']

    archivo = ArchivoService.get_archivo(id)
    try:
        extension = os.path.splitext(archivo.filename)[1]

        download_name = f"{archivo.titulo}{extension}"
        response = client.get_object(bucket_name, archivo.filename)

        file_data = io.BytesIO(response.read())
        response.close()
        response.release_conn()

        return send_file(file_data, download_name=download_name, as_attachment=True)
    except Exception:
        return + "Error al descargar el archivo", 500


@bp.get('/jya_show_files/<int:id>')
@h.authenticated_route(module="jinete-y-amazona", permissions=("index", "show",))
def show_files_jya(id):
    """
    Renderiza la tabla de archivos de un jinete o amazona con filtros, orden y paginación.

    Args:
        id (int): ID del jinete o amazona.

    Query Params:
        criterio (str): Criterio de búsqueda (ej., 'titulo' o 'tipo').
        busqueda (str): Término de búsqueda específico.
        ordenar_por (str): Campo por el cual ordenar (ej., 'titulo', 'fecha_subida').
        orden (str): Orden de clasificación ('asc' o 'desc').
        toggle_order (bool): Alterna el orden entre ascendente y descendente.

    Returns:
        Template: Renderiza `jya/jya-show-files.html` con los archivos filtrados.
    """
    criterio = request.args.get('criterio', '')
    busqueda = request.args.get('busqueda', '')
    ordenar_por = request.args.get('ordenar_por', 'nombre')
    orden = request.args.get('orden', 'asc')
    page, per_page = h.url_pagination_args(default_per_page=10)
    if request.args.get('toggle_order'):
        orden = 'desc' if orden == 'asc' else 'asc'

    criterios = {
        'titulo': Archivo.titulo,
        'tipo': Archivo.tipo
    }

    campos_ordenamiento = {
        'titulo': Archivo.titulo,
        'fecha_subida': Archivo.fecha_subida,
    }

    atributo = criterios.get(criterio)
    campo_ordenamiento = campos_ordenamiento.get(ordenar_por, Archivo.titulo)
    query, total = ArchivoService.do_filter_archivo(
        atributo, busqueda, orden, campo_ordenamiento, id, page, per_page)

    return render_template('jya/jya-show-files.html',
                           archivos=query,
                           criterio=criterio,
                           busqueda=busqueda,
                           ordenar_por=ordenar_por,
                           orden=orden,
                           jya=id,
                           urllib=urllib,
                           page=page,
                           per_page=per_page,
                           total=total,
                           form=ArchivoJyAForm)


def save_file_minio(file, filename):
    """
    Guarda un archivo en Minio.

    Args:
        file: Objeto de archivo que se va a guardar (debe tener un método `fileno()` y atributo `content_type`).
        filename (str): Nombre con el que se guardará el archivo en Minio.

    Raises:
        Exception: Si ocurre un error al guardar el archivo en Minio.
    """
    client = app.storage.client
    size = os.fstat(file.fileno()).st_size
    client.put_object("grupo21", filename, file, size,
                      content_type=file.content_type)


@bp.get('/jya_edit_files/<int:id>/<int:jya>/<filename>')
@h.authenticated_route(module="jinete-y-amazona", permissions=("update",))
def edit_file_jya(id, jya,  filename):
    """
    Renderiza el formulario para editar los archivos de un jinete/amazona.

    Args:
        id (int): Identificador del archivo a editar.
        jya (int): Identificador del jinete/amazona relacionado.
        filename (str): Nombre del archivo a editar.

    Returns:
        Renderizado de la plantilla con el formulario de edición del archivo.
    """
    archivo = ArchivoService.get_archivo(id)
    form = ArchivoJyAForm(titulo=archivo.titulo, tipo=archivo.tipo)
    del form.archivo
    return render_template("jya/jya-edit-files.html", form=form, archivo=archivo, jya=jya)


@bp.post('/updateFile-jya/<int:id>/<int:jya>')
@h.authenticated_route(module="jinete-y-amazona", permissions=("update",))
def update_file_jya(id, jya):
    """
    Actualiza los datos editados de los archivos.

    Args:
        id (int): Identificador del archivo a actualizar.
        jya (int): Identificador del jinete/amazona relacionado.

    Returns:
        Renderizado de la plantilla con el formulario actualizado o redirección en caso de error.
    """
    archivo = ArchivoService.get_archivo(id)
    form = ArchivoJyAForm()
    del form.archivo
    ok = ArchivoService.edit_archivo(archivo, request.form)
    if ok:
        flash("Archivo actualizado exitosamente.", "success")
    else:
        flash("No se pudo actualizar el archivo: ", "error")
        return redirect(url_for('jya.show_files_jya', id=id))
    return render_template("jya/jya-edit-files.html", form=form, formarchivo=ArchivoJyAForm(), archivo=archivo, jya=jya)


@bp.get('/subir_documento_jya/<int:id>')
@h.authenticated_route(module="jinete-y-amazona", permissions=("create",))
def subir_documento_jya(id):
    """
    Renderiza el formulario para subir un documento relacionado con un jinete/amazona.

    Args:
        id (int): Identificador del jinete/amazona al que se subirá el documento.

    Returns:
        Renderiza la plantilla con el formulario para subir un documento.
    """
    archivoform = ArchivoJyAForm()
    return render_template("jya/jya-subir-documento.html", form=archivoform, jya=id)


@bp.get('/subir_enlace_jya/<int:id>')
@h.authenticated_route(module="jinete-y-amazona", permissions=("create",))
def subir_enlace_jya(id):
    """
    Renderiza el formulario para subir un enlace relacionado con un jinete/amazona.

    Args:
        id (int): Identificador del jinete/amazona al que se subirá el documento.

    Returns:
        Renderiza la plantilla con el formulario para subir un documento.
    """
    enlaceform = EnlaceJyAForm()
    return render_template("jya/jya-subir-enlace.html", form=enlaceform, jya=id)


@bp.post('/insertar_documento_jya/<int:id>')
@h.authenticated_route(module="jinete-y-amazona", permissions=("create",))
def upload_file_jya(id):
    """
    Guarda tanto en Minio como en la base de datos la información relacionada con los archivos.

    Args:
        id (int): Identificador del jinete/amazona al que se subirá el archivo.

    Returns:
        Redirecciona a la lista de archivos si la carga es exitosa, o vuelve a mostrar el formulario en caso de error.
        
    Raises:
        Exception: Lanza una excepción genérica si ocurre un error durante 
                   el proceso de carga del archivo, ya sea en Minio o en la base de datos.

    Errors:
        - Si el formulario de archivo no es válido, se mostrará un mensaje de error y 
          se redirigirá al usuario al formulario de carga.
        - Si no se ha subido ningún archivo, se mostrará un mensaje de error específico.
        - Si ocurre un error durante la carga del archivo a Minio o al guardar en la 
          base de datos, se mostrará un mensaje de error general.
    """
    form = ArchivoJyAForm()

    if not form.validate_on_submit():
        h.flash_error("Información de archivo incorrecta.")
        return redirect(f"/subir_documento_jya/{id}")

    file = {
        "titulo": form.titulo.data,
        "filename": f"{id}_{request.files['archivo'].filename}",
        "enlace": "No se subió un enlace",
        "tipo": form.tipo.data,
    }

    try:
        save_file_minio(request.files["archivo"], file["filename"])
        ArchivoService.upload_file_jya(id, **file)
        h.flash_success("Archivo subido correctamente.")
        return redirect(url_for('jya.show_files_jya', id=id))
    except Exception as e:
        print(e)
        h.flash_error("Error al subir el archivo.")
        return redirect(f"/subir_documento_jya/{id}")


@bp.post('/delete_file_jya/<int:id>/<int:jya>')
@h.authenticated_route(module="jinete-y-amazona", permissions=("destroy",))
def delete_file_jya(id, jya):
    """
    Elimina físicamente un archivo del sistema y de Minio.

    Args:
        id (int): Identificador del archivo a eliminar.
        jya (int): Identificador del jinete/amazona al que pertenece el archivo.

    Returns:
        Response: Redirecciona a la lista de archivos después de eliminar el archivo.

    
    """
    archivo = ArchivoService.get_archivo(id)
    filename = archivo.filename
    client = app.storage.client
    client.remove_object("grupo21", filename)
    ArchivoService.delete_file(id)
    flash("Archivo eliminado exitosamente.", "success")
    return redirect(url_for('jya.show_files_jya', id=jya))


@bp.post('/jya-delete_enlace/<int:id>/<int:jya>')
@h.authenticated_route(module="jinete-y-amazona", permissions=("destroy",))
def delete_link_jya(id, jya):
    """
    Elimina un enlace físicamente de la base de datos.

    Args:
        id (int): Identificador del enlace a eliminar.
        jya (int): Identificador del jinete/amazona al que pertenece el enlace.

    Returns:
        redirect: Redirecciona a la lista de archivos después de eliminar el enlace.
    """
    ArchivoService.delete_file(id)
    flash("Enlace eliminado exitosamente.", "success")
    return redirect(url_for('jya.show_files_jya', id=jya))


@bp.post('/insertar_enlace_jya/<int:id>')
@h.authenticated_route(module="jinete-y-amazona", permissions=("create",))
def upload_link_jya(id):
    """
    Guarda un enlace en la base de datos.

    Args:
        id (int): Identificador del jinete/amazona al que se le está subiendo el enlace.

    Returns:
        redirect: Redirecciona a la lista de archivos después de intentar guardar el enlace.

    Raises:
        Exception: Lanza una excepción si ocurre un error durante la subida del enlace.

    Errors:
        - Si la información del formulario no es válida, se mostrará un mensaje de error.
        - Si ocurre un error al guardar el enlace en la base de datos, se mostrará un mensaje de error.
    """
    form = EnlaceJyAForm()

    if not form.validate_on_submit():
        h.flash_error("Información de archivo incorrecta.")
        return redirect(f"/subir_enlace_jya/{id}")

    file = {
        "titulo": form.titulo.data,
        "filename": "Sin filename",
        "enlace": form.enlace.data,
        "tipo": form.tipo.data,
    }

    try:
        ArchivoService.upload_file_jya(id, **file)
        h.flash_success("Archivo subido correctamente.")
        return redirect(url_for('jya.show_files_jya', id=id))
    except:
        h.flash_error("Error al subir el enlace.")
        return redirect(f"/subir_enlace_jya/{id}")


@bp.get('/jya_edit_link/<int:id>/<int:jya>')
@h.authenticated_route(module="jinete-y-amazona", permissions=("update",))
def edit_link_jya(id, jya):
    """
    Renderiza el formulario para editar un enlace con los datos ya cargados.

    Args:
        id (int): Identificador del enlace que se va a editar.
        jya (int): Identificador del jinete/amazona relacionado.

    Returns:
        render_template: Renderiza la plantilla con el formulario para editar el enlace.
    """
    archivo = ArchivoService.get_archivo(id)
    form = EnlaceJyAForm(enlace=archivo.enlace,
                         titulo=archivo.titulo, tipo=archivo.tipo)
    return render_template("jya/jya-edit-link.html", form=form, archivo=archivo, jya=jya)


@bp.post('/update-link-jya/<int:id>/<int:jya>')
@h.authenticated_route(module="jinete-y-amazona", permissions=("update",))
def update_link_jya(id, jya):
    """
    Actualiza los datos editados de un enlace.

    Args:
        id (int): Identificador del enlace que se va a actualizar.
        jya (int): Identificador del jinete/amazona relacionado.

    Returns:
        Response: Redirige a la lista de archivos si la actualización es exitosa,
                  o renderiza la plantilla de edición en caso de error.

    Errors:
        - Si la actualización falla, se notifica al usuario que no se pudo actualizar el enlace.
    """
    archivo = ArchivoService.get_archivo(id)
    form = EnlaceJyAForm()
    ok = ArchivoService.edit_archivo(archivo, request.form)
    if ok:
        flash("Enlace actualizado exitosamente.", "success")
    else:
        flash("No se pudo actualizar el enlace: ", "error")
        return redirect(url_for('jya.show_files_jya', id=id))
    return render_template("jya/jya-edit-link.html", form=form, formarchivo=ArchivoJyAForm(), archivo=archivo, jya=jya)


@bp.post('/toggel_debtor/<int:id>')
@h.authenticated_route(module="jinete-y-amazona", permissions=("update",))
def toggel_debtor(id):
    """
    Actualiza el estado deudor/no deudor de un jinete/amazona.

    Args:
        id (int): Identificador del jinete/amazona cuyo estado se actualizará.

    Returns:
        redirect: Redirige a la lista de deudores después de actualizar el estado.
    """
    s.toggel_debtor_by_id(id)
    h.flash_success("Estado de deudor actualizado exitosamente.")
    return redirect(url_for('cobros.debtors_get'))
