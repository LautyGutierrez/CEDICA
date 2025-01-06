from src.core.database import db
from src.core.ecuestre.ecuestreModel import Ecuestre
from src.core.archivos.archivo import Archivo
from src.core.archivos.archivoEcuestre import ArchivoEcuestre
from src.core.ecuestre.sexoEcuestre import Sexo
from src.core.ecuestre.raza import Raza
from src.core.ecuestre.pelaje import Pelaje
from src.core.equipo import Miembro


class EcuestreService:

    @classmethod
    def create_pelaje(cls, **kwargs):
        """"
        
        Almacena un nuevo pelaje en la base de datos
         a partir de los datos recibidos como parametro.

        """
        pelaje = Pelaje(**kwargs)
        db.session.add(pelaje)
        db.session.commit()
        return pelaje

    @classmethod
    def create_ecuestre(cls, **kwargs):
        """"
        Almacena un nuevo ecuestre en la base de datos
        a partir de los datos recibidos como parametro.

        """
        try:
            ecuestre = Ecuestre(**kwargs)
            db.session.add(ecuestre)
            db.session.commit()
            return ecuestre
        except Exception as e:
            db.session.rollback()
            return None

    @classmethod
    def create_raza(cls, **kwargs):
        """
        
        Almacena una nueva raza en la base de datos.
        a partir de los datos recibidos como parametro.

        """
        raza = Raza(**kwargs)
        db.session.add(raza)
        db.session.commit()
        return raza

    @classmethod
    def create_sexoEcuestre(cls, **kwargs):
        """
        Almacena un nuevo sexo en la base de datos.
        a partir de los datos recibidos como parametro.

        """
        sexo = Sexo(**kwargs)
        db.session.add(sexo)
        db.session.commit()
        return sexo

    @classmethod
    def logical_delete_ecuestre(cls, ecuestre_id):
        """

        Borra logicamente el ecuestre correspondiente
        al id recibido como parametro de la base de datos.
        
        """
        ecuestre = Ecuestre.query.get(ecuestre_id)
        ecuestre.borrado = True
        db.session.commit()
        return Ecuestre.query.get(ecuestre_id)

    @classmethod
    def findEcuestreById(cls, ecuestre_id):
        """
        Busca un ecuestre en la base de datos por su id que 
        fue enviado como parametro.
        
        """
        return Ecuestre.query.get(ecuestre_id)

    @classmethod
    def editEcuestre(cls, ecuestre, form):
        ok = False
        try:
            """"
            Recorre los campos del formulario a través de un ciclo for
            y los asigna al objeto ecuestre.
            
            """
            for field, value in form.items():
                if hasattr(ecuestre, field) and value != "":
                    setattr(ecuestre, field, value)

            db.session.commit()
            ok = True
        except Exception as e:
            db.session.rollback()
        return ok

    @classmethod
    def doFilter(cls, atributo, busqueda, orden, campo_ordenamiento, tipo_JA, page=1, per_page=10):
        consulta = Ecuestre.query.filter_by(borrado=False)

        if atributo:
            consulta = consulta.filter(atributo.ilike('%' + busqueda + '%'))

        if tipo_JA:
            consulta = consulta.filter(Ecuestre.tipo_JA == tipo_JA)

        if orden == 'desc':
            consulta = consulta.order_by(campo_ordenamiento.desc())
        else:
            consulta = consulta.order_by(campo_ordenamiento.asc())

        total = consulta.count()

        ecuestres = consulta.offset(
            (page - 1) * per_page).limit(per_page).all()

        return ecuestres, total

    @classmethod
    def getEcuestresWithDetails(cls):
        """
        
        Obtiene todos los ecuestres junto con su raza, pelaje y sexo d
        de la base de datos que no estén borrados.
        
        """
        return db.session.query(Ecuestre, Raza, Pelaje, Sexo).join(Raza, Ecuestre.raza_id == Raza.id) .join(Pelaje, Ecuestre.pelaje_id == Pelaje.id).join(Sexo, Ecuestre.sexo_id == Sexo.id).filter(Ecuestre.borrado == False)

    @classmethod
    def getRazas(cls):
        #Obtiene todas las razas de la base de datos.
        return Raza.query.all()

    @classmethod
    def getRaza(cls, raza_id):
        #Obtiene una raza de la base de datos por su id.
        raza = Raza.query.get(raza_id)
        if raza:
            return True
        return False
    
    @classmethod
    def getSexo(cls, sexo_id):
        #Obtiene una raza de la base de datos por su id.
        sexo = Sexo.query.get(sexo_id)
        if sexo:
            return True
        return False
    
    @classmethod
    def getPelaje(cls, pelaje_id):
        #Obtiene un pelake de la base de datos por su id.
        pelaje = Pelaje.query.get(pelaje_id)
        if pelaje:
            return True
        return False
    
    @classmethod
    def getSexos(cls):
        #Obtiene todos los sexos de la base de datos.
        return Sexo.query.all()

    @classmethod
    def getPelajes(cls):
        #Obtiene todos los pelajes de la base de datos.
        return Pelaje.query.all()

    @classmethod
    def getEntrenadores(cls):
        #Obtiene todos los entrenadores de la base de datos
        return Miembro.query.filter_by(borrado=False, puesto_laboral='caballos').all()

    @classmethod
    def getConductores(cls):
        #Obtiene todos los conductores de la base de datos.
        return Miembro.query.filter_by(borrado=False, puesto_laboral='conductor').all()
