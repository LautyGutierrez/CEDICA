from datetime import datetime
from src.core.database import db
from src.core.content.content import Content
from src.core.content.content_user import ContentUser
from src.core.auth import User


class ContentService:

    @classmethod
    def all_contents(
        cls,
        page: int = 1,
        per_page: int = 8,
        state: str = None,
        filter_input: str = None,
        author: str = None,
        published_from: str = None,
        published_to: str = None,
    ):
        """
        Devuelve todos los contenidos subidos a la base de datos, haciendo un join con las tablas ContentUser y User para saber quién subió cada contenido, aplicando paginación.

        Args:
            page: int
                Página actual para la paginación, por defecto 1
            per_page: int
                Cantidad de resultados por página para la paginación, por defecto 10
            state: str
                Estado del contenido a buscar, por defecto None.
            filter_input: str
                Filtro de búsqueda, por defecto None.
            author: str
                Email del autor del contenido, por defecto None.
            published_from: str
                Fecha de publicación desde la cual buscar, por defecto None.
            published_to: str
                Fecha de publicación hasta la cual buscar, por defecto None.

        Returns:
            contents:
                Un array de tuplas que contiene:
                    - Contenido, su registro en la tabla ContentUser (si existe, sino None) y su usuario (si existe, sino None).
            total: int
                Un entero que representa el número total de contenidos encontrados.
        """
        query = (
            db.session.query(Content, ContentUser, User)
            .select_from(Content)
            .outerjoin(ContentUser, Content.id == ContentUser.id_content)
            .outerjoin(User, ContentUser.id_user == User.id)
            .filter(Content.deleted == False)
        )

        if state:
            query = query.filter(Content.state == state)
        if filter_input:
            query = query.filter(
                db.or_(
                    Content.title.ilike(f"%{filter_input}%"),
                    Content.summary.ilike(f"%{filter_input}%"),
                    Content.content_text.ilike(f"%{filter_input}%"),
                )
            )

        if author:
            query = query.filter(User.email == author)
        
        if published_from:
            published_from = datetime.strptime(published_from, "%Y-%m-%d")
            query = query.filter(Content.date_publication >= published_from)
        if published_to:
            published_to = datetime.strptime(published_to, "%Y-%m-%d")
            query = query.filter(Content.date_publication <= published_to)

        total: int = query.count()
        contents = query.offset((page - 1) * per_page).limit(per_page).all()
        return contents, total

    @classmethod
    def create_content_user(cls, **kwargs):
        """
        Crea un nuevo registro en la tabla ContentUser, con el ID del contenido a publicar y el ID del usuario que lo subió.

        Args:
            **kwargs:
                id_content: int
                    ID del contenido a publicar
                id_user: int
                    ID del usuario que subió el contenido

        Returns:
            content_user:
                El registro creado en la tabla ContentUser.
        """
        content_user = ContentUser(**kwargs)
        db.session.add(content_user)
        db.session.commit()
        return content_user

    @classmethod
    def create_content(cls, user_id: int, **kwargs):
        """
        Crea un nuevo contenido en la base de datos y lo asocia con el usuario que lo subió.

        Args:
            user_id: int
                ID del usuario que subió el contenido.
            **kwargs:
                title: str
                    Título del contenido.
                summary: str
                    Resumen del contenido.
                content_text: str
                    Contenido del contenido.

        Returns:
            content:
                El contenido creado en la base de datos.
        """
        content = Content(**kwargs)
        db.session.add(content)
        db.session.commit()
        cls.create_content_user(**{"id_content": content.id, "id_user": user_id})
        return content

    @classmethod
    def change_status(cls, content_id: int) -> bool:
        """
        Cambia el estado de un contenido en la base de datos.
        Si el contenido estaba en estado borrador, lo cambia a publicado.
        Si el contenido estaba en estado publicado, lo cambia a archivado.
        Si el contenido estaba en estado archivado, lo cambia a publicado.

        Args:
            content_id: int
                ID del contenido a cambiar de estado.

        Returns:
            bool:
                True si se pudo cambiar el estado;
                False si el contenido no existe o no se pudo completar la operación.

        Raises:
            Exception:
                Si hay un error al editar la BD.
        """
        content = cls.get_content(content_id)
        if not content:
            return False

        try:
            if content.state == "borrador":
                content.state = "publicado"
                content.date_publication = db.func.current_timestamp()
            elif content.state == "publicado":
                content.state = "archivado"
            else:
                content.state = "publicado"
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

        return True

    @classmethod
    def delete(cls, content_id: int) -> bool:
        """
        Elimina lógicamente un contenido de la base de datos.

        Args:
            content_id: int
                ID del contenido a eliminar.

        Returns:
            bool:
                True si se pudo eliminar el contenido;
                False si el contenido no existe o no se pudo completar la operación.

        Raises:
            Exception:
                Si hay un error al editar la BD.
        """
        content = cls.get_content(content_id)
        if not content:
            return False

        try:
            content.deleted = True
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

        return True

    @classmethod
    def get_content(cls, content_id: int):
        """
        Devuelve un contenido de la base de datos.

        Args:
            content_id: int
                ID del contenido a buscar.

        Returns:
            El contenido encontrado si existe, None sino.
        """
        return db.session.query(Content).get(content_id)

    @classmethod
    def edit_content(cls, content_id: int, form):
        """
        Actualiza la información de un contenido en la base de datos.

        Args:
            content_id: int
                ID del contenido a actualizar.
            form: dict
                Formulario con los campos a actualizar.

        Returns:
            Contenido actualizado, None si no se encuentra o si se produce un error.

        Raises:
            Exception:
                Si hay un error al actualizar la información del contenido en la base de datos.
        """
        content = cls.get_content(content_id)
        if not content:
            return None

        try:
            for key, value in form.items():
                if hasattr(content, key):
                    setattr(content, key, value)
            content.date_update = db.func.current_timestamp()
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return None
        return content
