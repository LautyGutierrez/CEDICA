from datetime import datetime, timedelta
import random
from src.core.ecuestre import EcuestreService as e
from core.equipo import MemberService
from core.charge import ChargeService
from core.payment import PaymentService
from core.payment_method import PaymentMethodService
from core.type_of_payment import TypeOfPaymentService
from src.core.auth import roles, AuthService as auth
from src.core.database import db
from src.core.equipo.member_user_controller import MemberUser
from src.core.jya import ServiceJyA as s
from src.core.jya.institucion_escolar import InstitucionEscolar
from src.core.jya.jya import JyA
from src.core.jya.tutor import Tutor
import string
from src.core.equipo.miembro import Miembro
from src.core.contact.contactModel import Contacto
from src.core.contact import ContactoService as c
from src.core.content import ContentService

names = [
    "Juan",
    "Lautaro",
    "Franco",
    "Giovanni",
    "Zoe",
    "Maria",
    "Florencia",
    "Gerardo",
    "Facundo",
    "Felipe",
    "Juan Cruz",
    "Francisco",
    "Pilar",
    "Rosa",
    "Sofia",
    "Camila",
    "Mateo",
    "Agustina",
    "Ignacio",
    "Valentina",
    "Joaquin",
    "Emilia",
    "Lucia",
    "Martin",
    "Victoria",
    "Agustin",
    "Luciano",
    "Ana",
    "Tomas",
    "Julieta",
]
surnames = [
    "Gutierrez",
    "Rodriguez",
    "Hernandez",
    "Fernandez",
    "Dominguez",
    "Morales",
    "Ali",
    "Gomez",
    "Gonzalez",
    "Lopez",
    "Sanchez",
    "Martinez",
    "Perez",
    "Diaz",
    "Ramirez",
    "Vargas",
    "Jimenez",
    "Ortiz",
    "Castro",
    "Ruiz",
    "Silva",
    "Torres",
    "Mendoza",
    "Cruz",
    "Flores",
    "Rojas",
    "Alvarez",
]
professions = [
    "psicologo",
    "psicomotricista",
    "medico",
    "kinesiologo",
    "ocupacional",
    "psicopedagogo",
    "docente",
    "profesor",
    "fonoaudiologo",
    "veterinario",
    "otro",
]

all_roles = [
    "ADMINISTRACION",
    "VOLUNTARIADO",
    "ECUESTRE",
    "TECNICA",
    "SIN_ROL",
]


def seed_db():
    # Función auxiliar para generar datos aleatorios
    roles.seed_auth(db)
    print("Roles creados")

    # Tipos de pagos

    tipos_pagos = [
        {"name": "Honorarios"},
        {"name": "Proveedor"},
        {"name": "Gastos Varios"},
    ]

    for tipo_pago in tipos_pagos:
        TypeOfPaymentService.create_type_of_payment(**tipo_pago)
        print(f"Tipo de pago creado: {tipo_pago['name']}")

    print("Tipos de pagos creados💵")
    print("Creando medios de pagos...💵")
    # Medios de pagos
    print("Medios de pagos creados💵💰")

    print("Creando método de pagos...💵")
    metodos_pagos = [
        {"name": "Efectivo"},
        {"name": "Tarjeta de Crédito"},
        {"name": "Tarjeta de Débito"},
        {"name": "Transferencia Bancaria"},
        {"name": "Mercado Pago"},
    ]

    for metodo_pago in metodos_pagos:
        PaymentMethodService.create_payment_method(**metodo_pago)
        print(f"Método de pago creado: {metodo_pago['name']}")

    print("Métodos de pagos creados💵💰")

    print("Creando usuarios...✨✨")

    def random_user_data():

        first_name = random.choice(names)
        last_name = random.choice(surnames)
        beggining = datetime(1990, 1, 1).timestamp()
        end = datetime(2023, 12, 31).timestamp()

        password = "password123"

        username = f"user_{random.randint(1000, 9999)}"

        email = f"test_{random.randint(1000, 9999)}@gmail.com".lower()

        return {
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "alias": username,
            "email": email,
            "created_at": datetime.fromtimestamp(random.uniform(beggining, end)),
        }

    # Usuarios con roles determinados
    # ROL ADMINISTRACION
    user_data = random_user_data()
    user_data["email"] = "admin@gmail.com"
    user_data["rol_id"] = roles.get_role_by_name("ADMINISTRACION").id
    auth.create_user(**user_data)
    print(f"Usuario 1 creado: {user_data['email']} con rol ADMINISTRACION")

    # ROL SYSTEM_ADMIN
    user_data = random_user_data()
    user_data["email"] = "sysa@gmail.com"
    user_data["rol_id"] = roles.get_role_by_name("SYSTEM_ADMIN").id
    auth.create_user(**user_data)
    print(f"Usuario 2 creado: {user_data['email']} con rol SYSTEM_ADMIN")

    # ROL VOLUNTARIADO
    user_data = random_user_data()
    user_data["email"] = "uservoluntariado@gmail.com"
    user_data["rol_id"] = roles.get_role_by_name("VOLUNTARIADO").id
    auth.create_user(**user_data)
    print(f'Usuario 3 creado: {user_data["email"]} con rol VOLUNTARIADO')

    # ROL ECUESTRE
    user_data = random_user_data()
    user_data["email"] = "userecuestre@gmail.com"
    user_data["rol_id"] = roles.get_role_by_name("ECUESTRE").id
    auth.create_user(**user_data)
    print(f'Usuario 4 creado: {user_data["email"]} con rol ECUESTRE')

    # ROL TECNICA
    user_data = random_user_data()
    user_data["email"] = "usertecnica@gmail.com"
    user_data["rol_id"] = roles.get_role_by_name("TECNICA").id
    auth.create_user(**user_data)
    print(f'Usuario 5 creado: {user_data["email"]} con rol TECNICA')

    # ROL SIN ROL
    user_data = random_user_data()
    user_data["email"] = "usersinrol@gmail.com"
    user_data["rol_id"] = roles.get_role_by_name("SIN_ROL").id
    auth.create_user(**user_data)
    print(f'Usuario 6 creado: {user_data["email"]} SIN ROL')

    for i in range(7, 21):
        user_data = random_user_data()
        user_data["email"] = (
            f"{user_data["first_name"].replace(' ', '-')}{user_data["last_name"]}{random.randint(1, 99999)}@gmail.com".lower(),
        )
        user_data["rol_id"] = roles.get_role_by_name(random.choice(all_roles)).id
        user_data["is_active"] = random.choice([True, False])
        auth.create_user(**user_data)
        print(f"Usuario {i} creado: {user_data['email']}")

    # Usuario que tiene cuenta Miembro
    user_data = random_user_data()
    user_data["is_active"] = False
    user_data["first_name"] = "Zaira"
    user_data["last_name"] = "Zapetini"
    user_data["email"] = "pruebaMiembro@gmail.com"
    auth.create_user(**user_data)
    print(f"Usuario 21 creado: {user_data['email']}")

    # Miembros

    def random_member_data():
        jobs = [
            "administrativo",
            "terapeuta",
            "conductor",
            "pista",
            "herrero",
            "veterinario",
            "caballos",
            "domador",
            "profesor",
            "capacitacion",
            "mantenimiento",
            "otro",
        ]
        condition = ["voluntario", "rentado"]
        status = [True, False]

        name = random.choice(names)
        surname = random.choice(surnames)

        beggining = datetime(1990, 1, 1).timestamp()
        end = datetime(2023, 12, 31).timestamp()
        random1 = random.uniform(beggining, end)
        random2 = random.uniform(beggining, end)
        inicio = min(random1, random2)
        cese = max(random1, random2)

        return {
            "nombre": name,
            "apellido": surname,
            "dni": random.randint(1, 50000000),
            "domicilio": "".join(
                random.choice(string.ascii_letters) for _ in range(10)
            ),
            "email": f"{name.replace(' ', '-')}{surname}{random.randint(1, 99999)}@gmail.com".lower(),
            "localidad": "".join(random.choice(string.ascii_letters) for _ in range(6)),
            "telefono": "".join(random.choice(string.digits) for _ in range(13)),
            "profesion": random.choice(professions),
            "puesto_laboral": random.choice(jobs),
            "fecha_inicio": datetime.fromtimestamp(inicio),
            "fecha_cese": datetime.fromtimestamp(cese),
            "nombre_emergencia": random.choice(names),
            "telefono_emergencia": "".join(
                random.choice(string.digits) for _ in range(13)
            ),
            "obra_social": "".join(
                random.choice(string.ascii_letters) for _ in range(4)
            ),
            "num_afiliado": random.randint(0, 1000000),
            "condicion": random.choice(condition),
            "activo": random.choice(status),
            "fecha_creacion": datetime.fromtimestamp(random.uniform(beggining, end)),
        }

    print("Creando miembros...✨✨✨")
    miembros = []
    for i in range(21):
        member = random_member_data()
        m = MemberUser.create_miembro(**member)
        miembros.append(m[0])
        print(f'Miembro {i+1} creado: {member["email"]}')

    member = random_member_data()
    member["nombre"] = "Zaira"
    member["apellido"] = "Zapetini"
    member["email"] = "pruebaMiembro@gmail.com"
    MemberUser.create_miembro(**member)
    miembros.append(m[0])
    print(f"Miembro 22 creado: pruebaMiembro@gmail.com")

    # JYA

    def random_jya_data():
        emergy_contact = ["padre", "madre", "tutor"]
        disability_type = ["Mental", "Motora", "Sensorial", "Visceral"]
        headquarters = ["CASJ", "HLP", "Otro"]
        days = ["Lunes", "martes", "miercoles", "jueves", "viernes"]
        institutional_work_proposal = [
            "Equitacion",
            "Actividades Recreativas",
            "Hipoterapia",
            "Monta Terapeutica",
            "Deporte Ecuestre Adaptado",
        ]

        dnis = str(random.randint(10000000, 99999999))
        ages = random.randint(0, 100)
        beggining = datetime(1990, 1, 1).timestamp()
        end = datetime(2023, 12, 31).timestamp()
        random_date = random.uniform(beggining, end)
        place_of_birth = f"ciudad_{random.randint(1000, 9999)}"
        current_address = f"calle_{random.randint(1, 99)} nro_{random.randint(1, 9999)}"
        phone_number = str(random.randint(10000000, 99999999))
        phone_number_emergy = str(random.randint(10000000, 99999999))
        current_year = str(random.randint(1, 7))
        condition = "Regular" if random.choice([True, False]) else "De Baja"
        social_work_random = random.randint(100000, 999999)
        affiliation_random = random.randint(100000, 999999)

        return {
            "name": random.choice(names),
            "lastname": random.choice(surnames),
            "document_number": dnis,
            "age": ages,
            "birthdate": datetime.fromtimestamp(random_date),
            "place_of_birth": place_of_birth,
            "current_address": current_address,
            "phone_number": phone_number,
            "emergy_contact": random.choice(emergy_contact),
            "phone_number_emergy": phone_number_emergy,
            "is_scholarship_holder": random.choice([True, False]),
            "observations": "",
            "has_a_disability_certificate": random.choice([True, False]),
            "with_what_diagnosis": "",
            "other": None,
            "disability_type": random.choice(disability_type),
            "has_allowance": random.choice([True, False]),
            "allowance_type": "",
            "has_a_pension": random.choice([True, False]),
            "pension_type": "",
            "social_work": social_work_random,
            "affiliation_number": affiliation_random,
            "has_conservatorship": random.choice([True, False]),
            "social_work_observation": "",
            "professionals": f"{random.choice(names)}  {random.choice(surnames)}",
            "fk_institution_id": 0,
            "current_year_institution": current_year,
            "institution_observations": "",
            "institutional_work_proposal": random.choice(institutional_work_proposal),
            "condition": condition,
            "headquarters": random.choice(headquarters),
            "days": days,
            "teacher_or_therapist": 0,
            "horse_driver": 0,
            "runway_assistant": 0,
        }

    def random_institution_data():
        name = f"institucion_{random.randint(1, 100)}"
        address = f"calle_{random.randint(1, 99)} nro_{random.randint(1, 9999)}"
        phone_number = str(random.randint(10000000, 99999999))

        return {
            "institution_name": name,
            "institution_address": address,
            "institution_phone_number": phone_number,
        }

    def random_tutor_data():
        relationship = ["padre", "madre", "tutor_responsable"]
        educational_level = ["primario", "secundario", "terciario", "universitario"]

        dni = str(random.randint(10000000, 99999999))
        home_address = f"calle_{random.randint(1, 99)} nro_{random.randint(1, 9999)}"
        phone_number = f"calle_{random.randint(1, 99)} nro_{random.randint(1, 9999)}"
        email = f"test_{random.randint(1000, 9999)}@gmail.com"
        activity = ["Obrero", "Medico", "Programador"]

        return {
            "tutor_relationship": random.choice(relationship),
            "tutor_name": random.choice(names),
            "tutor_lastname": random.choice(surnames),
            "tutor_document_number": dni,
            "tutor_home_address": home_address,
            "tutor_phone_number": phone_number,
            "tutor_email": email,
            "tutor_educational_level": random.choice(educational_level),
            "tutor_activity": random.choice(activity),
        }

    print("Creando instituciones... 🏦")
    for i in range(6):
        institucion = random_institution_data()
        print(institucion)
        s.get_or_create_institution(**institucion)
        print(f"Instutución {i+1} creada: {institucion["institution_name"]}")

    print("Creando tutores...")
    for i in range(6):
        tutor = random_tutor_data()
        s.get_or_create_tutor(**tutor)
        print(f"Tutor {i+1} creado: {tutor["tutor_email"]}")

    instituciones = db.session.query(InstitucionEscolar).all()
    miembros = db.session.query(Miembro).all()
    print("Creando Jinetes y Amazonas...")
    for i in range(11):
        institucion_escolar = random.choice(instituciones)
        miembro_random1 = random.choice(miembros)
        miembro_random2 = random.choice(miembros)
        miembro_random3 = random.choice(miembros)
        jya = random_jya_data()
        jya["fk_institution_id"] = institucion_escolar.id
        jya["teacher_or_therapist"] = miembro_random1.id
        jya["horse_driver"] = miembro_random2.id
        jya["runway_assistant"] = miembro_random3.id
        s.create_jya(**jya)
        print(f"JyA {i+1} creado: {jya["name"]} {jya["lastname"]}")

    tutores = db.session.query(Tutor).all()
    jyas = db.session.query(JyA).all()

    print("Relacionando Jinetes y Amazonas con tutores...")
    for jinete in jyas:
        tutor1 = random.choice(tutores)
        tutor2 = random.choice(tutores) if random.choice([True, False]) else None

        relation = {
            "jya_id": jinete.id,
            "tutor_id1": tutor1.id,
            "tutor_id2": tutor2.id if tutor2 else None,
        }

        s.create_jya_tutor(**relation)
        print(f"El JyA {jinete.name} {jinete.lastname} ya tiene tutores")

    # Pagos

    print("Creando pagos...💵")

    description = [
        "Pago de honorarios",
        "Pago de proveedores",
        "Gastos varios",
        "Pago de servicios",
        "Pago de insumos",
        "Pago de mantenimiento",
        "Pago de software",
        "Pago de licencias",
        "Pago de servicios esenciales",
        "Pago de alquiler",
        "Pago de sueldos",
        "Pago de impuestos",
        "Pago de servicios de internet",
        "Pago de servicios de electricidad",
        "Pago de servicios de agua",
        "Pago de servicios de gas",
    ]

    for i in range(10):

        beggining = datetime(2023, 1, 1).timestamp()
        end = datetime(2024, 11, 22).timestamp()
        PaymentService.create_payment(
            id_member=random.randint(1, 6),
            id_type_of_payment=1,
            amount=random.randint(100, 1000),
            description=random.choice(description),
            date=datetime.fromtimestamp(random.uniform(beggining, end)),
        )
        print(f"Pago {i+1} creado 💰✨")

    for i in range(10):
        beggining = datetime(1990, 1, 1).timestamp()
        end = datetime(2023, 12, 31).timestamp()
        PaymentService.create_payment(
            id_type_of_payment=random.randint(2, 3),
            amount=random.randint(100, 1000),
            description=random.choice(description),
            date=datetime.fromtimestamp(random.uniform(beggining, end)),
        )
        print(f"Pago {i+1} creado 💰✨")

    # Ecuestres

    pelajes = [
        {"descripcion": "Alazán"},
        {"descripcion": "Tordillo"},
        {"descripcion": "Negro"},
        {"descripcion": "Bayo"},
        {"descripcion": "Zaino"},
    ]

    razas = [
        {"descripcion": "Árabe"},
        {"descripcion": "Pura Sangre"},
        {"descripcion": "Cuarto de Milla"},
        {"descripcion": "Percherón"},
        {"descripcion": "Appaloosa"},
    ]

    sexos = [{"descripcion": "Macho"}, {"descripcion": "Hembra"}]
    todos_los_sexos = []
    todos_los_pelajes = []
    todos_las_raza = []
    for pelaje in pelajes:
        todos_los_pelajes.append(e.create_pelaje(**pelaje))

    for raza in razas:
        todos_las_raza.append(e.create_raza(**raza))

    for sexo in sexos:
        todos_los_sexos.append(e.create_sexoEcuestre(**sexo))

    def random_ecuestre_data():
        nombres = [
            "Spirit",
            "Tornado",
            "Pegasus",
            "Bucephalus",
            "Rocinante",
            "Shadowfax",
            "Silver",
            "Marengo",
            "Copenhagen",
            "Comanche",
            "Zoe",
            "Alicia",
            "Facundo",
            "Brenda",
            "Oscar",
            "Luna",
            "Sol",
            "Estrella",
            "Canela",
            "Chocolate",
            "Vainilla",
            "Mora",
            "Frambuesa",
            "Ciruela",
            "Rayo",
            "Trueno",
            "Tormenta",
            "Huracán",
            "Tornado",
            "Ciclón",
        ]
        sedes = ["Sede Norte", "Sede Sur", "Sede Este", "Sede Oeste"]
        tipos_JA = [
            "hipoterapia",
            "monta_terapeutica",
            "deporte_ecuestre_adaptado",
            "actividades_recreativas",
            "equitacion",
        ]
        compra_o_donacion = ["compra", "donacion"]

        nombre = random.choice(nombres)
        sede = random.choice(sedes)
        tipo_JA = random.choice(tipos_JA)
        compra_donacion = random.choice(compra_o_donacion)

        fecha_nacimiento = datetime.now() - timedelta(
            days=random.randint(365, 365 * 20)
        )
        fecha_ingreso = datetime.now() - timedelta(days=random.randint(0, 365 * 5))

        sexo = random.choice(todos_los_sexos)
        raza = random.choice(todos_las_raza)
        pelaje = random.choice(todos_los_pelajes)
        entrenador = random_member_data()
        entrenador["puesto_laboral"] = "caballos"
        entrenador_creado = MemberUser.create_miembro(**entrenador)

        conductor = random_member_data()
        conductor["puesto_laboral"] = "conductor"
        conductor_creado = MemberUser.create_miembro(**conductor)

        return {
            "nombre": nombre,
            "fecha_nacimiento": fecha_nacimiento,
            "compra_o_donacion": compra_donacion,
            "fecha_ingreso": fecha_ingreso,
            "sede": sede,
            "sexo_id": sexo.id_sexo,
            "raza_id": raza.id_raza,
            "pelaje_id": pelaje.id_pelaje,
            "tipo_JA": tipo_JA,
            "entrenador": entrenador_creado[0].id,
            "conductor": conductor_creado[0].id,
        }

    print("Creando ecuestres...🏇🏼🏇🏼")
    ecuestres = []
    for i in range(20):
        ecuestre_data = random_ecuestre_data()
        ecuestre = e.create_ecuestre(**ecuestre_data)
        if ecuestre is None:
            print(f"Error al crear el ecuestre {i+1}")
        else:
            ecuestres.append(ecuestre)
            print(f"Ecuestre {i+1} creado: {ecuestre.nombre}")

    # Crear un ecuestre con un nombre específico para pruebas
    ecuestre_data = random_ecuestre_data()
    ecuestre_data["nombre"] = "PruebaEcuestre"
    ecuestre = e.create_ecuestre(**ecuestre_data)
    if ecuestre is None:
        print("Error al crear el ecuestre de prueba")
    else:
        ecuestres.append(ecuestre)
        print(f"Ecuestre de prueba creado: {ecuestre.nombre}")

    print("Creando Cobros...💵")

    for i in range(15):
        beggining = datetime(2023, 1, 1).timestamp()
        end = datetime(2024, 11, 22).timestamp()

        observations = [
            "Compra de insumos para proyectos específicos",
            "Donación de particulares o empresas",
            "Gastos administrativos varios",
            "Adquisición de equipos para mejora operativa",
            "Contribución por parte de socios",
            "Pagos de servicios esenciales",
            "Compra de software y licencias",
            "Gastos de mantenimiento de instalaciones",
        ]

        ChargeService.create_charge(
            id_member=random.randint(1, 20),
            id_payment_method=random.randint(1, 5),
            id_jya=random.randint(1, 10),
            amount=random.randint(10000, 100000),
            date=datetime.fromtimestamp(random.uniform(beggining, end)),
            observation=random.choice(observations),
        )
        print(f"Cobro {i+1} creado 💰✨")

    for i in range(10):
        beggining = datetime(2023, 1, 1).timestamp()
        end = datetime(2024, 11, 22).timestamp()

        ChargeService.create_charge(
            id_member=random.randint(1, 20),
            id_payment_method=random.randint(1, 5),
            id_jya=random.randint(1, 10),
            amount=random.randint(10000, 100000),
            date=datetime.fromtimestamp(random.uniform(beggining, end)),
        )
        print(f"Cobro {i+1} creado 💰✨")


    # Contactos
    contactos = []
    for i in range(15):
        nombre = random.choice(names)
        apellido = random.choice(surnames)
        email = f"{nombre.lower()}.{apellido.lower()}@example.com"
        cuerpo_mensaje = f"Mensaje de prueba {i + 1}"
        contacto = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "cuerpo_mensaje": cuerpo_mensaje,
        }
        contactos.append(contacto)
    print("Creando contactos...📇")
    for contacto_data in contactos:
        contacto = c.create(**contacto_data)
        print(f"Contacto creado: {contacto.nombre} {contacto.apellido}")
    print("Contactos creados exitosamente.")

    # Contenidos
    print("Creando contenidos... 📰📰📰")

    def random_content_data():
        states: list[str] = ["borrador", "publicado", "archivado"]

        titles_and_summaries = {
            "Cómo la equinoterapia ayuda en la rehabilitación física": "Descubre los beneficios físicos de la equinoterapia",
            "Historias de éxito en la equinoterapia": "Conoce historias inspiradoras de personas que han mejorado con la equinoterapia",
            "La importancia de la equinoterapia en niños con autismo": "Analizamos el impacto positivo de la equinoterapia en niños con autismo",
            "Equinoterapia: una terapia complementaria para la salud": "La equinoterapia como complemento en tratamientos de salud",
            "El impacto positivo de la equinoterapia en la vida de las personas": "Cómo la equinoterapia transforma vidas",
            "Equinoterapia y su papel en el tratamiento de la ansiedad": "El rol de la equinoterapia en la reducción de la ansiedad",
            "Cómo los caballos ayudan en la terapia de personas con discapacidad": "El apoyo de los caballos en terapias para personas con discapacidad",
            "Equinoterapia: un enfoque holístico para el bienestar": "Un enfoque integral de la equinoterapia para el bienestar",
            "La ciencia detrás de la equinoterapia y sus beneficios": "Investigamos la ciencia que respalda la equinoterapia",
            "Equinoterapia y su efectividad en el tratamiento de la depresión": "La equinoterapia como tratamiento para la depresión",
            "Cómo la equinoterapia mejora la calidad de vida de los pacientes": "Mejoras en la calidad de vida gracias a la equinoterapia",
            "Equinoterapia: una terapia innovadora para la salud mental": "Innovaciones en la equinoterapia para la salud mental",
            "El vínculo entre humanos y caballos en la equinoterapia": "La conexión especial entre humanos y caballos en la terapia",
            "Equinoterapia y su impacto en el desarrollo emocional de los niños": "El desarrollo emocional infantil a través de la equinoterapia",
        }
        random_state: str = random.choice(states)
        random_int: int = random.randint(1, 1000)
        random_title_summary = random.choice(list(titles_and_summaries.items()))

        return {
            "title": random_title_summary[0] + f" {random_int}",
            "summary": random_title_summary[1] + f" {random_int}",
            "content_text": f"Contenido del contenido {random_int}",
            "state": random_state,
            "date_publication": datetime.now() - timedelta(days=random.randint(0, 365 * 5)),
        }

    for i in range(12):
        content_data = random_content_data()
        content = ContentService.create_content(random.randint(1, 21), **content_data)
        print(f"Contenido {i+1} creado: {content.title}")

    print("Base de datos sembrada con éxito!🌱🌱🌱")