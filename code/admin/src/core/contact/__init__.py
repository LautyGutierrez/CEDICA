from src.core.contact.contactModel import Contacto
from src.core.database import db


class ContactoService:

    @classmethod
    def index(cls, estado, orden, page, per_page):
        """
        Obtiene una lista paginada de contactos filtrados por estado y ordenados por fecha de creación.

        Args:
            estado (str): Estado del contacto para filtrar.
            orden (str): Orden de la lista ('asc' para ascendente, 'desc' para descendente).
            page (int): Número de la página actual.
            per_page (int): Número de contactos por página.

        Returns:
            tuple: Una tupla que contiene la lista de contactos y el total de contactos.
        """
        query = db.session.query(Contacto)
        if estado:
            query = query.filter(Contacto.estado == estado)

        if orden == "asc":
            query = query.order_by(Contacto.fecha_creacion.asc())
        else:
            query = query.order_by(Contacto.fecha_creacion.desc())

        total = query.count()

        consulta = query.offset((page - 1) * per_page).limit(per_page).all()

        return consulta, total

    @classmethod
    def create(cls, **kwargs):
        """
        Crea un nuevo contacto con los datos proporcionados.

        Args:
            **kwargs: Diccionario con los datos del nuevo contacto.

        Returns:
            Contacto: El objeto contacto creado.
        """
        contacto = Contacto(**kwargs)
        db.session.add(contacto)
        db.session.commit()
        return contacto

    @classmethod
    def getContacto(cls, contacto_id):
        """
        Obtiene un contacto específico por su ID.

        Args:
            contacto_id (int): ID del contacto a obtener.

        Returns:
            Contacto: El objeto contacto correspondiente al ID proporcionado.
        """
        return db.session.query(Contacto).get(contacto_id)

    @classmethod
    def borrarContacto(cls, contacto):
        """
        Elimina un contacto específico de la base de datos.

        Args:
            contacto (Contacto): El objeto contacto a eliminar.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        db.session.delete(contacto)
        db.session.commit()
        return contacto

    @classmethod
    def updateContacto(cls, contacto, form):
        """
        Actualiza un contacto con los datos del formulario, informando el éxito o error de la operación.

        Args:
            contacto (Contacto): El objeto contacto a actualizar.
            form (dict): Diccionario con los datos del formulario.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        ok = False
        try:
            for field, value in form.items():
                if hasattr(contacto, field) and value != "":
                    setattr(contacto, field, value)

            db.session.commit()
            ok = True
        except Exception as e:
            db.session.rollback()
        return ok

    @classmethod
    def getMensaje(cls, contacto_id):
        """
        Obtiene el mensaje de un contacto específico.

        Args:
            contacto_id (int): ID del contacto del cual se desea obtener el mensaje.

        Returns:
            str: El mensaje del contacto.
        """
        contacto = db.session.query(Contacto).get(contacto_id)
        return contacto.mensaje
