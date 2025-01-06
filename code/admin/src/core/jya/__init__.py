from src.core.ecuestre.ecuestreModel import Ecuestre
from src.core.archivos.archivo_jya import ArchivoJyA
from src.core.archivos.archivo import Archivo
from src.core.equipo.miembro import Miembro
from src.core.database import db
from src.core.jya.jya import JyA
from src.core.jya.institucion_escolar import InstitucionEscolar
from src.core.jya.tutor import Tutor
from src.core.jya.jyatutor import JyATutors
import typing as t
import typing_extensions as te
from src.web.forms.jya import (
    JyAForm,
    DeleteJyAForm,
    JyAUpdateForm,
    TutorUpdateForm,
    Tutor2UpdateForm,
    InstitucionEscolarUpdateForm,
)
from sqlalchemy import func, asc, desc, String
from core.charge.charge import Charge


class ServiceJyA:

    @classmethod
    def list_jya(cls):
        """
        Devuelve todos los jinetes y amazonas de la base de datos.

        Returns:
            List[JyA]: Una lista de objetos JyA que representan a todos los jinetes y amazonas en la base de datos.
        """
        return JyA.query.all()

    @classmethod
    def create_jya(cls, **kwargs) -> t.Optional[JyA]:
        """
        Crea un legajo de jinete/amazona en la base de datos.

        Args:
            **kwargs: Atributos del nuevo objeto JyA que se pasarán como parámetros clave-valor.

        Returns:
            Optional[JyA]: Devuelve el objeto JyA creado si la operación es exitosa; de lo contrario, devuelve None.
        """
        jya = JyA(**kwargs)
        db.session.add(jya)
        db.session.commit()
        return jya

    @classmethod
    def get_jya_by_id(cls, id):
        """
        Busca un jinete/amazona en la base de datos por su ID.

        Args:
            id (int): El identificador único del jinete/amazona a buscar.

        Returns:
            Optional[JyA]: Devuelve el objeto JyA correspondiente al ID proporcionado si existe; de lo contrario, devuelve None.
        """
        return JyA.query.filter_by(id=id).first()

    @classmethod
    def exist_jya(cls, document_number) -> t.Optional[JyA]:
        """
        Busca si existe un jinete/amazona en la base de datos por su número de documento.

        Args:
            document_number (str): El número de documento del jinete/amazona a buscar.

        Returns:
            Optional[JyA]: Devuelve el objeto JyA correspondiente al número de documento proporcionado si existe;
            de lo contrario, devuelve None.
        """
        return JyA.query.filter_by(document_number=document_number).first()

    @classmethod
    def create_jya_tutor(cls, **kwargs) -> t.Optional[JyATutors]:
        """
        Crea una relación entre una jinete/amazona y un tutor en la base de datos.

        Args:
            **kwargs: Argumentos clave-valor que representan los atributos de la relación
                    entre el jinete/amazona y el tutor.

        Returns:
            Optional[JyATutors]: Devuelve el objeto JyATutors creado si la relación se crea correctamente;
            de lo contrario, devuelve None.
        """
        jya_tutor = JyATutors(**kwargs)
        db.session.add(jya_tutor)
        db.session.commit()
        return jya_tutor

    @classmethod
    def create_institution(cls, **kwargs) -> t.Optional[InstitucionEscolar]:
        """
        Crea una institución escolar en la base de datos.

        Args:
            **kwargs: Argumentos clave-valor que representan los atributos de la institución escolar.

        Returns:
            Optional[InstitucionEscolar]: Devuelve el objeto InstitucionEscolar creado si la institución se
            crea correctamente; de lo contrario, devuelve None.
        """
        institution = InstitucionEscolar(**kwargs)
        db.session.add(institution)
        db.session.commit()
        return institution

    @classmethod
    def get_or_create_institution(cls, **kwargs) -> t.Optional[InstitucionEscolar]:
        """
        Busca si existe la institución escolar en la base de datos; si no existe, la crea.

        Args:
            **kwargs: Argumentos clave-valor que representan los atributos de la institución escolar.

        Returns:
            Optional[InstitucionEscolar]: Devuelve el objeto InstitucionEscolar encontrado o creado.
            Si se encontró la institución, se devuelve la existente; si no, se crea y devuelve una nueva.
        """
        institution = InstitucionEscolar.query.filter_by(
            institution_name=kwargs.get("institution_name"),
            institution_address=kwargs.get("institution_addres"),
            institution_phone_number=kwargs.get("institution_phone_number"),
        ).first()
        if institution is None:
            institution = cls.create_institution(**kwargs)

        return institution

    @classmethod
    def create_tutor(cls, **kwargs) -> t.Optional[Tutor]:
        """
        Crea un tutor en la base de datos.

        Args:
            **kwargs: Argumentos clave-valor que representan los atributos del tutor.

        Returns:
            Optional[Tutor]: Devuelve el objeto Tutor que ha sido creado en la base de datos.
            Si la creación falla, se devolverá None.
        """
        tutor = Tutor(**kwargs)
        db.session.add(tutor)
        db.session.commit()
        return tutor

    @classmethod
    def get_or_create_tutor(cls, **kwargs) -> t.Optional[Tutor]:
        """
        Busca si existe un tutor en la base de datos por su número de documento.
        Si no existe, lo crea.

        Args:
            **kwargs: Argumentos clave-valor que representan los atributos del tutor.

        Returns:
            Optional[Tutor]: Devuelve el objeto Tutor que se ha encontrado o creado.
            Si no se puede crear el tutor, se devolverá None.
        """
        tutor = Tutor.query.filter_by(
            tutor_document_number=kwargs.get("tutor_document_number")
        ).first()
        if tutor is None:
            tutor = cls.create_tutor(**kwargs)
        return tutor

    @classmethod
    def logical_delete_jya(cls, jya_id):
        """
        Elimina lógicamente a un jinete/amazona modificando el campo "is_erased".

        Args:
            jya_id (int): El ID del jinete/amazona que se desea eliminar lógicamente.

        Returns:
            JyA: Devuelve el objeto JyA con el campo "is_erased" actualizado a True.
        """
        jya = JyA.query.get(jya_id)
        jya.is_erased = True
        db.session.commit()
        jya = JyA.query.get(jya_id)
        return jya

    @classmethod
    def get_tutors_by_jya(cls, jya_id) -> JyATutors:
        """
        Devuelve la relación entre un jinete/amazona y sus tutores.

        Args:
            jya_id (int): El ID del jinete/amazona para el cual se desea obtener la relación con sus tutores.

        Returns:
            JyATutors: Devuelve el objeto JyATutors que representa la relación entre el jinete/amazona y sus tutores.
        """
        return db.session.query(JyATutors).filter_by(jya_id=jya_id).first()

    @classmethod
    def all_jya(cls):
        """
        Devuelve todos los jinete/amazonas que no estén borrados lógicamente.

        Returns:
            List[JyA]: Devuelve una lista de objetos JyA que representan a los jinete/amazonas que no han sido borrados lógicamente.
        """
        return JyA.query.filter_by(is_erased=False).all()

    @classmethod
    def do_filter(cls, atributo, busqueda, orden, campo_ordenamiento):
        """
        Realiza una consulta filtrada en la base de datos.

        Args:
            atributo (Column): El atributo del modelo JyA sobre el cual se realizará el filtro.
            busqueda (str): El término de búsqueda que se utilizará para filtrar los resultados.
            orden (str): La dirección de ordenamiento, puede ser 'asc' para ascendente o 'desc' para descendente.
            campo_ordenamiento (Column): El campo que se utilizará para ordenar los resultados.

        Returns:
            List[JyA]: Devuelve una lista de objetos JyA que cumplen con los criterios de filtrado y ordenamiento.
        """
        consulta = JyA.query.filter(
            atributo.ilike("%" + busqueda + "%"), JyA.is_erased == False
        )
        if orden == "desc":
            consulta = consulta.order_by(campo_ordenamiento.desc())
        else:
            consulta = consulta.order_by(campo_ordenamiento.asc())
        jya = consulta.all()
        return jya

    @classmethod
    def edit_jya_data(cls, jya, form):
        """
        Edita los datos de un jinete/amazona en la base de datos.

        Args:
            jya (JyA): El objeto JyA que se desea editar.
            form (JyAForm): El formulario que contiene los datos a actualizar.

        Returns:
            bool: Devuelve True si la edición se realizó exitosamente, de lo contrario, devuelve False.
        """
        ok = False
        try:

            for field, value in form.data.items():
                if hasattr(jya, field) and value != "":
                    if isinstance(value, Miembro) or isinstance(value, Ecuestre):
                        setattr(jya, field, value.id)
                    else:
                        setattr(jya, field, value)

            db.session.commit()
            ok = True
        except Exception as e:

            db.session.rollback()
        return ok

    @classmethod
    def edit_tutor1(cls, tutor1, form):
        """
        Edita los datos de un tutor en la base de datos que están en el campo "tutor1" de la relación JyA/Tutor.

        Args:
            tutor1 (Tutor): El objeto Tutor que se desea editar.
            form (Form): El formulario que contiene los datos a actualizar.

        Returns:
            bool: Devuelve True si la edición se realizó exitosamente, de lo contrario, devuelve False.

        Errors:
            - Si ocurre un error durante la actualización, se lanza una excepción y se revierte la sesión de la base de datos.
        """
        ok = False
        try:
            for field, value in form.data.items():
                if hasattr(tutor1, field) and value != "":
                    setattr(tutor1, field, value)

            db.session.commit()
            ok = True
        except Exception as e:
            db.session.rollback()
        return ok

    @classmethod
    def edit_tutor2(cls, tutor2: Tutor, form):
        """
        Edita los datos de un tutor en la base de datos que están en el campo "tutor2" de la relación JyA/Tutor.

        Dado que los nombres de los campos del formulario no coinciden con los nombres de los campos de la tabla de la base de datos,
        se requiere un mapeo de los nombres de los campos.

        Args:
            tutor2 (Tutor): El objeto Tutor que se desea editar.
            form (Form): El formulario que contiene los datos a actualizar.

        Returns:
            bool: Devuelve True si la edición se realizó exitosamente, de lo contrario, devuelve False.

        Errors:
            - Si ocurre un error durante la actualización, se lanza una excepción y se revierte la sesión de la base de datos.
        """

        field_mapping = {
            "tutor_relationship2": "tutor_relationship",
            "tutor_name2": "tutor_name",
            "tutor_lastname2": "tutor_lastname",
            "tutor_document_number2": "tutor_document_number",
            "tutor_home_address2": "tutor_home_address",
            "tutor_phone_number2": "tutor_phone_number",
            "tutor_email2": "tutor_email",
            "tutor_educational_level2": "tutor_educational_level",
            "tutor_activity2": "tutor_activity",
        }

        ok = False
        try:
            for field, value in form.data.items():
                if field in field_mapping and value != "":
                    db_field = field_mapping[field]
                    if hasattr(tutor2, db_field):
                        if field != "csrf_token":
                            setattr(tutor2, db_field, value)
            db.session.commit()
            ok = True
        except Exception as e:
            db.session.rollback()
        return ok

    @classmethod
    def edit_institution(cls, institucion, form):
        """
        Edita los datos de una institución escolar en la base de datos.

        Args:
            institucion (InstitucionEscolar): El objeto InstitucionEscolar que se desea editar.
            form (Form): El formulario que contiene los nuevos datos a actualizar.

        Returns:
            bool: Devuelve True si la edición se realizó exitosamente, de lo contrario, devuelve False.

        Errors:
            - Si ocurre un error durante la actualización, se lanza una excepción y se revierte la sesión de la base de datos.
        """
        ok = False
        try:
            for field, value in form.data.items():
                if hasattr(institucion, field) and value != "":
                    if field != "csrf_token":
                        setattr(institucion, field, value)

            db.session.commit()
            ok = True
        except Exception as e:
            db.session.rollback()
        return ok

    @classmethod
    def compare_tutors(cls, **tutor1_data):
        """
        Compara si un tutor ya está en la base de datos según su email y número de documento.

        Args:
            tutor1_data (dict): Un diccionario que contiene la información del tutor,
                                que debe incluir las claves 'tutor_email' y 'tutor_document_number'.

        Returns:
            bool: True si el tutor existe y el número de documento coincide; False si existe pero
                el número de documento no coincide, o si no existe.
        """
        tutor = Tutor.query.filter(
            Tutor.tutor_email == tutor1_data["tutor_email"]
        ).first()
        if tutor:
            if tutor.tutor_document_number != tutor1_data["tutor_document_number"]:
                return False
        return True

    @classmethod
    def toggel_debtor_by_id(cls, jya_id):
        """
        Cambia el valor booleano del campo "is_debtor" de un jinete/amazona.

        Args:
            jya_id (int): El identificador del jinete/amazona cuyo estado de deudor se desea cambiar.

        Returns:
            JyA: El objeto actualizado del jinete/amazona con el nuevo estado de "is_debtor".
        """
        jya = JyA.query.get(jya_id)
        jya.is_debtor = not jya.is_debtor
        db.session.commit()
        return jya

    @classmethod
    def cantidad_becados(cls):
        """
        Devuelve la cantidad de jinetes y amazonas que tienen beca.

        Returns:
            int: La cantidad de jinetes y amazonas con beca.
        """
        return JyA.query.filter_by(is_scholarship_holder=True).count()

    @classmethod
    def cantidad_sin_beca(cls):
        """
        Devuelve la cantidad de jinetes y amazonas que no tienen beca.

        Returns:
            int: La cantidad de jinetes y amazonas sin beca.
        """
        return JyA.query.filter_by(is_scholarship_holder=False).count()

    @classmethod
    def cantidad_discapacidad(cls, discapacidad):
        """
        Devuelve la cantidad de jinetes y amazonas con una discapacidad específica.

        Args:
            discapacidad (str): El tipo de discapacidad a buscar.

        Returns:
            int: La cantidad de jinetes y amazonas con la discapacidad especificada.
        """
        return JyA.query.filter_by(disability_type=discapacidad).count()

    @classmethod
    def cantidad_propuestas_trabajo(cls):
        """
        Devuelve la cantidad de los tipos de propuestas de trabajo institucionales.
        Returns:
            List[tuple]: Una lista de tuplas con el tipo de propuesta y la cantidad de jinetes/amazonas que la tienen.
        """
        propuestas = (
            db.session.query(
                JyA.institutional_work_proposal,
                func.count(JyA.institutional_work_proposal).label("cantidad"),
            )
            .group_by(JyA.institutional_work_proposal)
            .order_by(func.count(JyA.institutional_work_proposal).desc())
            .all()
        )

        return propuestas

    @classmethod
    def deudores(
        cls,
        order_field: str = "pagos",
        order_type: str = "desc",
        filter_field: str = None,
        filter_input: str = None,
        page: int = 1,
        per_page: int = 10,
    ):
        """
        Devuelve la cantidad de jinetes y amazonas deudores.

        Returns:
            List[JyA]: 
                Una lista de objetos JyA que representan a los jinetes y amazonas deudores.
            total: int
                Un entero que representa el número total de la cantidad de jinetes y amazonas deudores.
        """
        query = (
            db.session.query(
                JyA.name.label("nombre"),
                JyA.lastname.label("apellido"),
                JyA.document_number.label("dni"),
                func.count(Charge.id).label("pagos"),
                func.min(Charge.date).label("fecha_mas_vieja"),
                func.sum(Charge.amount).label("valor"),
            )
            .join(Charge, JyA.id == Charge.id_jya)
            .filter(Charge.state == "Pendiente")
            .group_by(JyA.name, JyA.lastname, JyA.document_number)
        )

        order = asc(order_field) if order_type == "asc" else desc(order_field)

        if filter_field and filter_input:
            if filter_field == "dni":
                query = query.filter(
                    func.cast(JyA.document_number, String).ilike(f"%{filter_input}%")
                )
            elif filter_field == "pagos_minima":
                query = query.having(func.count(Charge.id) >= int(filter_input))
            elif filter_field == "pagos_maxima":
                query = query.having(func.count(Charge.id) <= int(filter_input))
            elif filter_field == "valor_minimo":
                query = query.having(func.sum(Charge.amount) >= int(filter_input))
            elif filter_field == "valor_maximo":
                query = query.having(func.sum(Charge.amount) <= int(filter_input))
            else:
                query = query.filter(getattr(JyA, filter_field).ilike(f"%{filter_input}%"))

        query = query.order_by(order)

        total: int = query.count()
        deudores = query.offset((page - 1) * per_page).limit(per_page).all()

        return deudores, total

    @classmethod
    def propuesta_trabajo_jya(
        cls, 
        propuesta,
        order_field: str = "name",
        order_type: str = "desc",
        filter_field: str = None,
        filter_input: str = None,
        page: int = 1,
        per_page: int = 10,
    ):
        """
        Devuelve los jinetes y amazonas con una propuesta de trabajo institucionale especifica.

        Returns:
            List[JyA]: Una lista de jinetes y amazonas con propuestas de trabajo institucionales igual al parametro.
        """
        jya = db.session.query(JyA).filter(JyA.institutional_work_proposal == propuesta)
        order = asc(order_field) if order_type == "asc" else desc(order_field)
        
        if filter_field and filter_input:
            if filter_field == "document_number":
                jya = jya.filter(
                    func.cast(JyA.document_number, String).ilike(f"%{filter_input}%")
                )
            elif filter_field == "lastname":
                jya = jya.filter(
                    func.cast(JyA.lastname, String).ilike(f"%{filter_input}%")
                )
            elif filter_field == "is_scholarship_holder":
                jya = jya.filter(
                    func.cast(JyA.is_scholarship_holder, String).ilike(f"%{filter_input}%")
                )
            elif filter_field == "disability_type":
                jya = jya.filter(
                    func.cast(JyA.disability_type, String).ilike(f"%{filter_input}%")
                )
            elif filter_field == "name":
                jya = jya.filter(
                    func.cast(JyA.name, String).ilike(f"%{filter_input}%")
                )
            else:
                jya = jya.filter(getattr(JyA, filter_field).ilike(f"%{filter_input}%"))

        jya = jya.order_by(order)
        total = jya.count()
        jya = jya.offset((page - 1) * per_page).limit(per_page).all()
       
        return jya, total