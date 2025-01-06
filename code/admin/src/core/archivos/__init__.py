from src.core.jya.jya import JyA
from src.core.archivos.archivo_jya import ArchivoJyA
from sqlalchemy import asc, desc
from src.core.archivos.archivo import Archivo
from src.core.archivos.archivoEcuestre import ArchivoEcuestre
from src.core.archivos.miembro_archivo import ArchivoMiembro
from src.core.database import db
from src.core.equipo.miembro import Miembro
import typing as t


class ArchivoService:

    @classmethod
    def doFilterArchivo(
        cls, atributo, busqueda, orden, campo_ordenamiento, tipo, id, page=1, per_page=10
    ):
        """
        Filtra los archivos de un ecuestre y en el caso de recibir un atributo, segun el atributo y la busqueda recibida como parametro
        y los ordena según el orden recibido como parametro. En el caso de no recibir un atributo,
        devuelve todos los archivos relacionados al ecuestre.

        Args:
            atributo:
                Criterio para buscar los archivos segun su título.
            busqueda:
                Query ingresada para buscar archivos según su titulo.
            orden:
                Orden en que se van a ver los resultados, de forma ascendente o descendente.
            campo_ordenamiento:
                Campo por el cual se van a ordenar los resultados.
            tipo:
                Tipo de archivo por el cual filtrar.
            id:
                ID del ecuestre del cual se van a obtener los archivos.
            page:
                Página actual para la paginación, por defecto 1
            per_page:
                Cantidad de resultados por página para la paginación, por defecto 10
        Returns:
            archivos: 
                Archivos del ecuestre solicitados con los filtros aplicados.
            total:
                Un entero que representa el número total de archivos del ecuestre encontrados.

        """
        consulta = cls.getArchivos(id)
        if atributo:
            consulta = consulta.filter(atributo.ilike("%" + busqueda + "%"))
        if tipo:
            consulta = consulta.filter(Archivo.tipo == tipo)
        if orden == "desc":
            consulta = consulta.order_by(campo_ordenamiento.desc())
        else:
            consulta = consulta.order_by(campo_ordenamiento.asc())

        total = consulta.count()
        archivos = consulta.offset((page - 1) * per_page).limit(per_page).all()
        return archivos, total

    @classmethod
    def getArchivos(cls, id):
        """
        Obtiene los archivos relacionados a un ecuestre.
        
        Args:
            id:
                ID del ecuestre del cual se obtienen los archivos.
        
        Returns:
            Devuelve todos los archivos del ecuestre.
        """
        return (
            db.session.query(Archivo)
            .join(ArchivoEcuestre, Archivo.id == ArchivoEcuestre.archivo_id)
            .filter(ArchivoEcuestre.ecuestre_id == id)
        )

    @classmethod
    def saveFile(cls, **kwargs):
        """
        Almacena un nuevo archivo/enlace en la base de datos.
        Args:
            **kwargs:
                Argumentos claves adicionales en forma de diccionario.
        
        Returns:
            Devuelve el archivo guardado en la BD.

        """
        archivo = Archivo(**kwargs)
        db.session.add(archivo)
        db.session.commit()
        return archivo

    @classmethod
    def saveFileEcuestre(cls, idArchivo, idEcuestre):
        """
        Almacena la relacion entre un archivo/enlace y un ecuestre en la base de datos.

        Args:
            idArchivo:
                ID del archivo a ser guardado.
            idEcuestre:
                ID del ecuestre al cual se le guardará un archivo.
        
        Returns:
            Devuelve el archivo asociado con el ecuestre.
        """
        archivoEcuestre = {"archivo_id": idArchivo, "ecuestre_id": idEcuestre}
        arch = ArchivoEcuestre(**archivoEcuestre)
        db.session.add(arch)
        db.session.commit()
        return archivoEcuestre

    @classmethod
    def getArchivo(cls, id):
        """
        Busca un archivo/enlace en la base de datos por su id.
        
        Args:
            id:
                ID del archivo a ser buscado.

        Returns:
            Devuelve el archivo del ID recibido, None si no existe.
        """
        return Archivo.query.get(id)

    @classmethod
    def editArchivo(cls, archivo, titulo) -> bool:
        """
        Edita el titulo de un archivo/enlace en la base de datos.
        Args:
            archivo:
                Archivo a ser modificado.
            titulo:
                El nuevo título que tendrá el archivo.
        
        Returns:
            bool
                True si se pudo editar correctamente, False si no.    
        """
        ok = False
        try:
            archivo.titulo = titulo
            db.session.commit()
            ok = True
        except Exception as e:
            db.session.rollback()
        return ok

    @classmethod
    def borrarArchivoEcuestre(cls, id: int):
        """
        Borra un archivo/enlace fisicamente en cascada de la base de datos, primero
        borrandolo de la tabla archivoEcuestre y luego de la tabla archivo.

        Args:
            id: int
                ID del archivo a ser borrado.
        
        Returns:
            Archivo eliminado.
        """
        ArchivoEcuestre.query.filter_by(archivo_id=id).delete()

        archivo = Archivo.query.get(id)
        if archivo:
            db.session.delete(archivo)

        db.session.commit()
        return archivo

    @classmethod
    def upload_file(cls, member_id: int, **kwargs) -> bool:
        """
        Sube un archivo y lo relaciona a un miembro.
        
        Args:
            member_id: int
                ID del miembro del cual se subirá un archivo.
            **kwargs:
                Argumentos claves adicionales en forma de diccionario.
        
        Returns:
            bool:
                True si se pudo subir el archivo, False si no.
        """
        member = db.session.query(Miembro).get(member_id)

        if not member:
            return False

        try:
            archivo = Archivo(**kwargs)
            db.session.add(archivo)
            db.session.commit()
            archivo_miembro = {"id_miembro": member_id,
                               "id_archivo": archivo.id}
            cls.file_member(**archivo_miembro)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return False
        return True

    @classmethod
    def file_member(cls, **kwargs):
        """
        Crea una relación entre un miembro y un archivo.

        Args:
            **kwargs:
                Argumentos claves adicionales en forma de diccionario.
        
        Returns:
            Devuelve la tabla intermedia entre archivo y miembro.
        """
        archivo_miembro = ArchivoMiembro(**kwargs)
        db.session.add(archivo_miembro)
        return archivo_miembro

    @classmethod
    def files_of_member(
        cls,
        member_id: int,
        page: int = 1,
        per_page: int = 10,
        order_type: str = "asc",
        filter_type: t.Optional[str] = None,
        filter_input: t.Optional[str] = None,
    ) -> t.Tuple[t.List[Archivo], int]:
        """
        Obtener todos los archivos subidos por un miembro determinado por su ID;
        realizando un join entre las tablas Archivo y ArchivoMiembro y filtrando por el ID del miembro.
        Args:
            member_id: int
                ID del miembro cuyos archivos se desean obtener.
            page: int
                página actual para la paginación, por defecto 1
            per_page: int
                cantidad de resultados por página para la paginación, por defecto 10
            order_type: str
                tipo de orden (ascendente o descendente), por defecto asc
            filter_type: str
                tipo de archivo para realizar el filtro de búsqueda, por defecto None
            filter_input: str
                input ingresado para realizar el filtro de búsqueda, por defecto None
        Returns:
            Tuple[List[Archivo], int]:
                Una tupla que contiene:
                    Un array de archivos
                    Un entero que representa el número total de miembros encontrados.
        """
        query = (
            db.session.query(Archivo)
            .outerjoin(ArchivoMiembro)
            .filter(ArchivoMiembro.id_miembro == member_id)
        )

        order = asc("titulo") if order_type == "asc" else desc("titulo")

        if filter_type:
            query = query.filter(Archivo.tipo == filter_type)

        if filter_input:
            query = query.filter(
                getattr(Archivo, "titulo").ilike(f"%{filter_input}%"))

        query = query.order_by(order)

        total = query.count()
        files = query.offset((page - 1) * per_page).limit(per_page).all()
        return files, total

    @classmethod
    def borrarArchivoMiembro(cls, id: int):
        """
        Borra un archivo/enlace fisicamente en cascada de la base de datos, primero
        borrandolo de la tabla archivoEcuestre y luego de la tabla archivo.

        Args:
            id: int
                ID del archivo a ser eliminado.
        
        Returns:
            Archivo a ser eliminado.
        """
        ArchivoMiembro.query.filter_by(id_archivo=id).delete()

        archivo = Archivo.query.get(id)
        if archivo:
            db.session.delete(archivo)

        db.session.commit()
        return archivo
    
    @classmethod
    def file_jya(cls, **kwargs):
        """
        Crea una relación entre un archivo y un jinete/amazona en la base de datos.

        Args:
            **kwargs: Argumentos que se usarán para crear el objeto ArchivoJyA. 
                    Debe incluir 'jya_id' y 'archivo_id'.

        Returns:
            ArchivoJyA: El objeto ArchivoJyA que se creó.
        """
        archivo_jya = ArchivoJyA(**kwargs)
        db.session.add(archivo_jya)
        return archivo_jya
    
    @classmethod
    def delete_file(cls, id):
        """
        Elimina físicamente un archivo y las relaciones que este tiene en la base de datos.

        Args:
            id (int): El identificador del archivo que se desea eliminar.

        Returns:
            Archivo: El objeto Archivo que fue eliminado, o None si no se encontró.
        """
        ArchivoJyA.query.filter_by(archivo_id=id).delete()

        archivo = Archivo.query.get(id)
        if archivo:
            db.session.delete(archivo)

        db.session.commit()
        return archivo
    
    @classmethod
    def upload_file_jya(cls, jya_id: int, **kwargs) -> bool:
        """
        Guarda en la base de datos a un archivo y su relación con un jinete/amazona.

        Args:
            jya_id (int): El identificador del jinete/amazona.
            **kwargs: Argumentos que se usarán para crear el objeto Archivo.

        Returns:
            bool: True si el archivo se guardó correctamente, False en caso contrario.
            
        Raises:
            Exception: Si ocurre un error al agregar el archivo o al crear la relación en la base de datos.
        """
        jya = db.session.query(JyA).get(jya_id)

        if not jya:
            return False

        try:
            archivo = Archivo(**kwargs)
            db.session.add(archivo)
            db.session.commit()
            archivo_jya = {"jya_id": jya_id, "archivo_id": archivo.id}
            cls.file_jya(**archivo_jya)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return False
        return True
    
    @classmethod
    def edit_archivo(cls, archivo, form):
        """
        Edita los datos de un archivo en la base de datos.

        Args:
            archivo: El objeto Archivo que se va a editar.
            form: Un formulario con los nuevos valores para los campos del archivo.

        Returns:
            bool: True si la edición fue exitosa, False en caso contrario.
        """
        ok = False
        try:
            for field, value in form.items():
                if hasattr(archivo, field) and value != "":
                    setattr(archivo, field, value)

            db.session.commit()
            ok = True
        except Exception as e:
            db.session.rollback()
        return ok
    
    @classmethod
    def do_filter_archivo(cls, atributo, busqueda, orden, campo_ordenamiento, id, page=1, per_page=10):
        """
        Filtra, ordena y pagina una consulta sobre los archivos.

        Args:
            atributo (str): El atributo por el cual se filtrará la consulta.
            busqueda (str): El valor que se buscará en el atributo especificado.
            orden (str): El orden de la consulta, puede ser 'asc' para ascendente o 'desc' para descendente.
            campo_ordenamiento: El campo por el cual se ordenará la consulta.
            id (int): El identificador que se usará para filtrar los archivos relacionados.
            page (int, opcional): El número de página que se desea obtener. Por defecto es 1.
            per_page (int, opcional): El número de archivos por página. Por defecto es 10.

        Returns:
            tuple: Un tuple que contiene dos elementos:
                - archivos (list): Una lista de archivos que cumplen con los criterios de búsqueda.
                - total (int): El número total de archivos que cumplen con los criterios de búsqueda.
        """
        consulta = cls.get_archivos(id)
        if atributo:
            consulta = consulta.filter(atributo.ilike("%" + busqueda + "%"))
            if orden == "desc":
                consulta = consulta.order_by(campo_ordenamiento.desc())
            else:
                consulta = consulta.order_by(campo_ordenamiento.asc())

        total = consulta.count()
        archivos = consulta.offset((page-1) * per_page).limit(per_page).all()
        return archivos, total
    
    
    @classmethod
    def get_archivo(cls, id):
        """
        Busca un archivo en la base de datos por su ID.

        Args:
            id (int): El identificador del archivo que se desea buscar.

        Returns:
            Archivo: El objeto Archivo correspondiente al ID proporcionado, o None si no se encuentra.
        """
        return Archivo.query.get(id)

    @classmethod
    def get_archivos(cls, id):
        """
        Busca todos los archivos asociados a un jinete/amazona en la base de datos.

        Args:
            id (int): El identificador del jinete/amazona cuyos archivos se desean buscar.

        Returns:
            list: Una lista de objetos Archivo asociados al jinete/amazona con el ID proporcionado.
        """
        return db.session.query(Archivo).join(ArchivoJyA, Archivo.id == ArchivoJyA.archivo_id).filter(ArchivoJyA.jya_id == id)


