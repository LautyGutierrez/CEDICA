from datetime import datetime
from src.core.ecuestre.ecuestreModel import Ecuestre
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    EmailField,
    SelectField,
    StringField,
    IntegerField,
    DateField,
    SelectMultipleField
)
from wtforms import validators as v
from typing import TypedDict
from wtforms import HiddenField
import json
from wtforms_sqlalchemy.fields import QuerySelectField
from src.core.equipo import Miembro
from sqlalchemy import or_


class DeleteJyAForm(FlaskForm):
    csrf_token = HiddenField()


class JyAFormValues(TypedDict):
    name: str
    lastname: str
    document_number: str
    age: int
    birthdate: datetime
    place_of_birth: str
    current_address: str
    phone_number: str
    emergy_contact: str
    phone_number_emergy: str
    is_scholarship_holder: bool
    observations: str
    has_a_disability_certificate: bool
    with_what_diagnosis: str
    other: str
    disability_type: str
    has_allowance: bool
    allowance_type: str
    has_a_pension: bool
    pension_type: str
    social_work: str
    affiliation_number: str
    has_conservatorship: bool
    social_work_observation: str
    professionals: str
    # campos para el tutor 1
    tutor_relationship: str
    tutor_name: str
    tutor_lastname: str
    tutor_document_number: str
    tutor_home_address: str
    tutor_phone_number: str
    tutor_email: str
    tutor_educational_level: str
    tutor_activity: str
    # campos para el tutor 2
    tutor_relationship2: str
    tutor_name2: str
    tutor_lastname2: str
    tutor_document_number2: str
    tutor_home_address2: str
    tutor_phone_number2: str
    tutor_email2: str
    tutor_educational_level2: str
    tutor_activity2: str
    # campos para la institucion escolar
    institution_name: str
    institution_address: str
    institution_phone_number: str
    institution_current_year: str
    institution_observations: str
    institutional_work_proposal: str
    condition: str
    headquarters: str
    days: list
    teacher_or_therapist: object
    horse_driver: object
    horse: object
    runway_assistant: object


class JyAForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=30)
        ],
    )
    lastname = StringField(
        "Apellido",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=30)
        ],
    )
    document_number = StringField(
        "Número de documento",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=10)
        ],
    )
    age = IntegerField(
        "Edad",
        validators=[
            v.DataRequired("Este campo es requerido")
        ],
    )
    birthdate = DateField(
        "Fecha de nacimiento",
        format="%Y-%m-%d",
        validators=[
            v.DataRequired("Este campo es requerido")
        ]
    )
    place_of_birth = StringField(
        "Lugar de nacimiento (localidad y provincia)",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    current_address = StringField(
        "Dirección actual",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    phone_number = StringField(
        "Número de teléfono",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=20)
        ]
    )
    emergy_contact = StringField(
        "Contacto de emergencia",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    phone_number_emergy = StringField(
        "Número de teléfono de emergencia",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=20)
        ]
    )
    is_scholarship_holder = BooleanField(
        "¿Es becado?",
        validators=[

        ]
    )
    observations = StringField(
        "Observaciones de la beca",
        validators=[

        ]
    )
    has_a_disability_certificate = BooleanField(
        "¿Posee certificado de discapacidad?",
        validators=[

        ]
    )
    with_what_diagnosis = SelectField(
        "¿Con qué diagnostico?",
        choices=[
            ("Ninguno", "*"),
            ("ECNE", "ECNE"),
            ("LPT", "Lesión post-traumática"),
            ("Mielomeningocele", "Mielomeningocele"),
            ("EM", "Esclerosis Mutiple"),
            ("EL", "Esclerosis Leve"),
            ("ACV", "Secuelas de ACV"),
            ("DI", "Discapacidad Intelectual"),
            ("TEA", "Trastorno del Espectro Autista"),
            ("TApren", "Trastorno de Aprendizaje"),
            ("TDAH", "Trastorno por Déficit de Atención/Hiperactividad"),
            ("TComu", "Trastorno de la Comunicación"),
            ("TAns", "Trastorno de Ansiedad"),
            ("SD", "Síndrome de Down"),
            ("RM", "Retraso Madurativo"),
            ("Psicosis", "Psicosis"),
            ("TCond", "Trastorno de Conducta"),
            ("TAA", "Transtornos del Animo y Afectivos"),
            ("TAli", "Transtorno Alimentario"),
            ("Otro", "Otro"),
        ],
        validators=[
            v.DataRequired("Este campo es requerido")
        ]
    )
    other = StringField(
        "En caso de elegir la opción 'otro', indicar cuál",
        validators=[

        ]
    )
    disability_type = SelectField(
        "Tipo de discapacidad",
        choices=[
            ("Otro", "*"),
            ("Mental", "Mental"),
            ("Motora", "Motora"),
            ("Sensorial", "Sensorial"),
            ("Visceral", "Visceral")
        ],
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=20)
        ]
    )
    has_allowance = BooleanField(
        "¿Percibe alguna Asignación Familiar?",
        validators=[

        ]
    )
    allowance_type = SelectField(
        "En caso afirmativo, ¿cuál?",
        choices=[
            ("Ninguno", "*"),
            ("AUH", "Asignación Universal por Hijo"),
            ("AUHD", "Asignación Universal por Hijo con Discapacidad"),
            ("AAEA", "Asignación por Ayuda Escolar Anual")
        ],
        validators=[
            v.Length(max=100)
        ]
    )
    has_a_pension = BooleanField(
        "¿Es beneficiario de alguna pensión?",
        validators=[

        ]
    )
    pension_type = SelectField(
        "¿Cuál?",
        choices=[
            ("Otra", "*"),
            ("Provincial", "Provincial"),
            ("Nacional", "Nacional")
        ],
        validators=[
            v.Length(max=15)
        ]
    )
    social_work = StringField(
        "Obra Social del Alumno",
        validators=[
            v.Length(max=20)
        ]
    )
    affiliation_number = StringField(
        "Número de Afiliación",
        validators=[
            v.Length(max=20)
        ]
    )
    has_conservatorship = BooleanField(
        "¿Posee curatela?",
        validators=[

        ]
    )
    social_work_observation = StringField(
        "Observaciones",
        validators=[
            v.Length(max=100)
        ]
    )
    professionals = StringField(
        "Profesionales que lo atienden",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=200)
        ]
    )
    # campos para el tutor 1
    tutor_relationship = StringField(
        "Parentesco del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    tutor_name = StringField(
        "Nombre del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    tutor_lastname = StringField(
        "Apellido del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    tutor_document_number = StringField(
        "DNI del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=10)
        ]
    )
    tutor_home_address = StringField(
        "Dirección del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    tutor_phone_number = StringField(
        "Número de teléfono del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=20)
        ]
    )
    tutor_email = EmailField(
        "Email del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    tutor_educational_level = SelectField(
        "Nivel de escolaridad del tutor",
        choices=[
            ("Ninguno", "*"),
            ("Primario", "Primario"),
            ("Secundario", "Secundario"),
            ("Terciario", "Terciario"),
            ("Universitario", "Universitario")
        ],
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    tutor_activity = StringField(
        "Actividad u ocupación del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    # campos para el tutor 2
    tutor_relationship2 = StringField(
        "Parentesco del tutor 2",
        validators=[
            v.Length(max=50),
        ]
    )
    tutor_name2 = StringField(
        "Nombre del tutor 2",
        validators=[
            v.Length(max=50),
        ]
    )
    tutor_lastname2 = StringField(
        "Apellido del tutor 2",
        validators=[
            v.Length(max=50),
        ]
    )
    tutor_document_number2 = StringField(
        "DNI del tutor 2",
        validators=[
            v.Length(max=10),
        ]
    )
    tutor_home_address2 = StringField(
        "Dirección del tutor 2",
        validators=[
            v.Length(max=50),
        ]
    )
    tutor_phone_number2 = StringField(
        "Número de teléfono del tutor 2",
        validators=[
            v.Length(max=20),
        ]
    )
    tutor_email2 = EmailField(
        "Email del tutor 2",
        validators=[
            v.Length(max=50),
        ]
    )
    tutor_educational_level2 = SelectField(
        "Nivel de escolaridad del tutor 2",
        choices=[
            ("Ninguno", "*"),
            ("Primario", "Primario"),
            ("Secundario", "Secundario"),
            ("Terciario", "Terciario"),
            ("Universitario", "Universitario")
        ],
        validators=[
            v.Length(max=50)
        ]
    )
    tutor_activity2 = StringField(
        "Actividad u ocupación del tutor 2",
        validators=[
            v.Length(max=50),
        ]
    )
    # campos para la institucion escolar
    institution_name = StringField(
        "Nombre de la institución",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    institution_address = StringField(
        "Dirección de la institución",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    institution_phone_number = StringField(
        "Número de teléfono de la institución",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=20)
        ]
    )
    institution_current_year = StringField(
        "Grado/Año actual",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=10)
        ]
    )
    institution_observations = StringField(
        "Observaciones",
        validators=[
            v.Length(max=50)
        ]
    )
    institutional_work_proposal = SelectField(
        "Propuesta de Trabajo Institucional",
        choices=[
            ("Ninguna", "*"),
            ("Hipoterapia", "Hipoterapia"),
            ("Monta Terapeutica", "Monta Terapeutica"),
            ("Deporte Ecuestre Adaptado", "Deporte Ecuestre Adaptado"),
            ("Actividades Recreativas", "Actividades Recreativas"),
            ("Equitacion", "Equitacion")
        ],
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=30)
        ]
    )
    condition = SelectField(
        "Condición",
        choices=[
            ("Ninguna", "*"),
            ("Regular", "Regular"),
            ("De Baja", "De Baja")
        ],
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=8)
        ]
    )
    headquarters = SelectField(
        "Sede",
        choices=[
            ("Otra", "*"),
            ("CASJ", "CASJ"),
            ("HLP", "HLP"),
            ("Otro", "Otro")
        ],
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=5)
        ]
    )
    days = SelectMultipleField(
        "Dias",
        choices=[
            ("Lunes", "Lunes"),
            ("Martes", "Martes"),
            ("Miercoles", "Miercoles"),
            ("Jueves", "Jueves"),
            ("Viernes", "Viernes"),
            ("Sabado", "Sabado"),
            ("Domingo", "Domingo")
        ],
        validators=[v.DataRequired("Este campo es requerido")]
    )
    teacher_or_therapist = QuerySelectField(
        "Profesor/a o Terapeuta",
        query_factory=lambda: Miembro.query.filter(or_(
            Miembro.puesto_laboral == "terapeuta",
            Miembro.puesto_laboral == "profesor")).all(),
        get_label='nombre',
        validators=[v.DataRequired("Este campo es requerido")]
    )
    horse_driver = QuerySelectField(
        "Conductor del Caballo",
        query_factory=lambda: Miembro.query.filter_by(
            puesto_laboral="conductor").all(),
        get_label='nombre',
        validators=[v.DataRequired("Este campo es requerido")]
    )
    horse = QuerySelectField(
        "Caballo",
        query_factory=lambda: Ecuestre.query.all(),
        get_label='nombre',
        validators=[v.DataRequired("Este campo es requerido")]
    )
    runway_assistant = QuerySelectField(
        "Auxiliar de Pista",
        query_factory=lambda: Miembro.query.filter_by(
            puesto_laboral="pista").all(),
        get_label='nombre',
        validators=[v.DataRequired("Este campo es requerido")]
    )

    def values(self) -> JyAFormValues:
        return {
            "name": self.name.data,
            "lastname": self.lastname.data,
            "document_number": self.document_number.data,
            "age": self.age.data,
            "birthdate": self.birthdate.data,
            "place_of_birth": self.place_of_birth.data,
            "current_address": self.current_address.data,
            "phone_number": self.phone_number.data,
            "emergy_contact": self.emergy_contact.data,
            "phone_number_emergy": self.phone_number_emergy.data,
            "is_scholarship_holder": self.is_scholarship_holder.data,
            "observations": self.observations.data,
            "has_a_disability_certificate": self.has_a_disability_certificate.data,
            "with_what_diagnosis": self.with_what_diagnosis.data,
            "other": self.other.data,
            "disability_type": self.disability_type.data,
            "has_allowance": self.has_allowance.data,
            "allowance_type": self.allowance_type.data,
            "has_a_pension": self.has_a_pension.data,
            "pension_type": self.pension_type.data,
            "social_work": self.social_work.data,
            "affiliation_number": self.affiliation_number.data,
            "has_conservatorship": self.has_conservatorship.data,
            "social_work_observation": self.social_work_observation.data,
            "professionals": self.professionals.data,
            "tutor_relationship": self.tutor_relationship.data,
            "tutor_name": self.tutor_name.data,
            "tutor_lastname": self.tutor_lastname.data,
            "tutor_document_number": self.tutor_document_number.data,
            "tutor_home_address": self.tutor_home_address.data,
            "tutor_phone_number": self.tutor_phone_number.data,
            "tutor_email": self.tutor_email.data,
            "tutor_educational_level": self.tutor_educational_level.data,
            "tutor_activity": self.tutor_activity.data,
            "tutor_relationship2": self.tutor_relationship2.data,
            "tutor_name2": self.tutor_name2.data,
            "tutor_lastname2": self.tutor_lastname2.data,
            "tutor_document_number2": self.tutor_document_number2.data,
            "tutor_home_address2": self.tutor_home_address2.data,
            "tutor_phone_number2": self.tutor_phone_number2.data,
            "tutor_email2": self.tutor_email2.data,
            "tutor_educational_level2": self.tutor_educational_level2.data,
            "tutor_activity2": self.tutor_activity2.data,
            "institution_name": self.institution_name.data,
            "institution_address": self.institution_address.data,
            "institution_phone_number": self.institution_phone_number.data,
            "institution_current_year": self.institution_current_year.data,
            "institution_observations": self.institution_observations.data,
            "institutional_work_proposal": self.institutional_work_proposal.data,
            "condition": self.condition.data,
            "headquarters": self.headquarters.data,
            "days": self.days.data,
            "teacher_or_therapist": self.teacher_or_therapist.data,
            "horse_driver": self.horse_driver.data,
            "runway_assistant": self.runway_assistant.data
        }


class JyAUpdateForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=30)
        ],
    )
    lastname = StringField(
        "Apellido",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=30)
        ],
    )
    document_number = StringField(
        "Número de documento",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=10)
        ],
    )
    age = IntegerField(
        "Edad",
        validators=[
            v.DataRequired("Este campo es requerido")
        ],
    )
    birthdate = DateField(
        "Fecha de nacimiento",
        format="%Y-%m-%d",
        validators=[
            v.DataRequired("Este campo es requerido")
        ]
    )
    place_of_birth = StringField(
        "Lugar de nacimiento (localidad y provincia)",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    current_address = StringField(
        "Dirección actual",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    phone_number = StringField(
        "Número de teléfono",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=20)
        ]
    )
    emergy_contact = StringField(
        "Contacto de emergencia",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    phone_number_emergy = StringField(
        "Número de teléfono de emergencia",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=20)
        ]
    )
    is_scholarship_holder = BooleanField(
        "¿Es becado?",
        validators=[

        ]
    )
    observations = StringField(
        "Observaciones de la beca",
        validators=[

        ]
    )
    has_a_disability_certificate = BooleanField(
        "¿Posee certificado de discapacidad?",
        validators=[

        ]
    )
    with_what_diagnosis = SelectField(
        "¿Con qué diagnostico?",
        choices=[
            ("ECNE", "ECNE"),
            ("LPT", "Lesión post-traumática"),
            ("Mielomeningocele", "Mielomeningocele"),
            ("EM", "Esclerosis Mutiple"),
            ("EL", "Esclerosis Leve"),
            ("ACV", "Secuelas de ACV"),
            ("DI", "Discapacidad Intelectual"),
            ("TEA", "Trastorno del Espectro Autista"),
            ("TApren", "Trastorno de Aprendizaje"),
            ("TDAH", "Trastorno por Déficit de Atención/Hiperactividad"),
            ("TComu", "Trastorno de la Comunicación"),
            ("TAns", "Trastorno de Ansiedad"),
            ("SD", "Síndrome de Down"),
            ("RM", "Retraso Madurativo"),
            ("Psicosis", "Psicosis"),
            ("TCond", "Trastorno de Conducta"),
            ("TAA", "Transtornos del Animo y Afectivos"),
            ("TAli", "Transtorno Alimentario"),
            ("Otro", "Otro"),
        ],
        validators=[
            v.DataRequired("Este campo es requerido")
        ]
    )
    other = StringField(
        "En caso de elegir la opción 'otro', indicar cuál",
        validators=[

        ]
    )
    disability_type = SelectField(
        "Tipo de discapacidad",
        choices=[
            ("Mental", "Mental"),
            ("Motora", "Motora"),
            ("Sensorial", "Sensorial"),
            ("Visceral", "Visceral")
        ],
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=20)
        ]
    )
    has_allowance = BooleanField(
        "¿Percibe alguna Asignación Familiar?",
        validators=[

        ]
    )
    allowance_type = SelectField(
        "En caso afirmativo, ¿cuál?",
        choices=[
            ("AUH", "Asignación Universal por Hijo"),
            ("AUHD", "Asignación Universal por Hijo con Discapacidad"),
            ("AAEA", "Asignación por Ayuda Escolar Anual")
        ],
        validators=[
            v.Length(max=100)
        ]
    )
    has_a_pension = BooleanField(
        "¿Es beneficiario de alguna pensión?",
        validators=[

        ]
    )
    pension_type = SelectField(
        "¿Cuál?",
        choices=[
            ("Provincial", "Provincial"),
            ("Nacional", "Nacional")
        ],
        validators=[
            v.Length(max=15)
        ]
    )
    social_work = StringField(
        "Obra Social del Alumno",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=20)
        ]
    )
    affiliation_number = StringField(
        "Número de Afiliación",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=20)
        ]
    )
    has_conservatorship = BooleanField(
        "¿Posee curatela?",
        validators=[

        ]
    )
    social_work_observation = StringField(
        "Observaciones",
        validators=[
            v.Length(max=100)
        ]
    )
    professionals = StringField(
        "Profesionales que lo atienden",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=200)
        ]
    )
    institution_current_year = StringField(
        "Grado/Año actual",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=10)
        ]
    )
    institution_observations = StringField(
        "Observaciones de la institución",
        validators=[
            v.Length(max=50)
        ]
    )
    institutional_work_proposal = SelectField(
        "Propuesta de Trabajo Institucional",
        choices=[
            ("Ninguna", "*"),
            ("Hipoterapia", "Hipoterapia"),
            ("Monta Terapeutica", "Monta Terapeutica"),
            ("Deporte Ecuestre Adaptado", "Deporte Ecuestre Adaptado"),
            ("Actividades Recreativas", "Actividades Recreativas"),
            ("Equitacion", "Equitacion")
        ],
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=30)
        ]
    )
    condition = SelectField(
        "Condición",
        choices=[
            ("Ninguna", ""),
            ("Regular", "Regular"),
            ("De Baja", "De Baja")
        ],
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=8)
        ]
    )
    headquarters = SelectField(
        "Sede",
        choices=[
            ("Otro", "Otro"),
            ("CASJ", "CASJ"),
            ("HLP", "HLP"),
        ],
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=5)
        ]
    )
    days = SelectMultipleField(
        "Dias",
        choices=[
            ("Lunes", "Lunes"),
            ("Martes", "Martes"),
            ("Miercoles", "Miercoles"),
            ("Jueves", "Jueves"),
            ("Viernes", "Viernes"),
            ("Sabado", "Sabado"),
            ("Domingo", "Domingo")
        ],
        validators=[v.DataRequired("Este campo es requerido")]
    )
    teacher_or_therapist = QuerySelectField(
        "Profesor/a o Terapeuta",
        query_factory=lambda: Miembro.query.filter(or_(
            Miembro.puesto_laboral == "terapeuta",
            Miembro.puesto_laboral == "profesor")).all(),
        get_label='nombre',
        validators=[v.DataRequired("Este campo es requerido")]
    )
    horse_driver = QuerySelectField(
        "Conductor del Caballo",
        query_factory=lambda: Miembro.query.filter_by(
            puesto_laboral="conductor").all(),
        get_label='nombre',
        validators=[v.DataRequired("Este campo es requerido")]
    )
    runway_assistant = QuerySelectField(
        "Auxiliar de Pista",
        query_factory=lambda: Miembro.query.filter_by(
            puesto_laboral="pista").all(),
        get_label='nombre',
        validators=[v.DataRequired("Este campo es requerido")]
    )


class TutorUpdateForm(FlaskForm):
    tutor_relationship = StringField(
        "Parentesco del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    tutor_name = StringField(
        "Nombre del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    tutor_lastname = StringField(
        "Apellido del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    tutor_document_number = StringField(
        "DNI del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=10)
        ]
    )
    tutor_home_address = StringField(
        "Dirección del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    tutor_phone_number = StringField(
        "Número de teléfono del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=20)
        ]
    )
    tutor_email = EmailField(
        "Email del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    tutor_educational_level = SelectField(
        "Nivel de escolaridad del tutor",
        choices=[
            ("Primario", "Primario"),
            ("Secundario", "Secundario"),
            ("Terciario", "Terciario"),
            ("Universitario", "Universitario")
        ],
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    tutor_activity = StringField(
        "Actividad u ocupación del tutor",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )


class Tutor2UpdateForm(FlaskForm):
    tutor_relationship2 = StringField(
        "Parentesco del tutor 2",
        validators=[
            v.Length(max=50),
        ]
    )
    tutor_name2 = StringField(
        "Nombre del tutor 2",
        validators=[
            v.Length(max=50),
        ]
    )
    tutor_lastname2 = StringField(
        "Apellido del tutor 2",
        validators=[
            v.Length(max=50),
        ]
    )
    tutor_document_number2 = StringField(
        "DNI del tutor 2",
        validators=[
            v.Length(max=10),
        ]
    )
    tutor_home_address2 = StringField(
        "Dirección del tutor 2",
        validators=[
            v.Length(max=50),
        ]
    )
    tutor_phone_number2 = StringField(
        "Número de teléfono del tutor 2",
        validators=[
            v.Length(max=20),
        ]
    )
    tutor_email2 = EmailField(
        "Email del tutor 2",
        validators=[
            v.Length(max=50),
        ]
    )
    tutor_educational_level2 = SelectField(
        "Nivel de escolaridad del tutor 2",
        choices=[
            ("Primario", "Primario"),
            ("Secundario", "Secundario"),
            ("Terciario", "Terciario"),
            ("Universitario", "Universitario")
        ],
        validators=[
            v.Length(max=50)
        ]
    )
    tutor_activity2 = StringField(
        "Actividad u ocupación del tutor 2",
        validators=[
            v.Length(max=50),
        ]
    )


class InstitucionEscolarUpdateForm(FlaskForm):
    institution_name = StringField(
        "Nombre de la institución",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    institution_address = StringField(
        "Dirección de la institución",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=50)
        ]
    )
    institution_phone_number = StringField(
        "Número de teléfono de la institución",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(max=20)
        ]
    )
