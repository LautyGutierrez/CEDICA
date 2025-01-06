from enum import Enum


class GenderOptions(Enum):
    MALE = "Masculino"
    FEMALE = "Femenino"
    OTHER = "Otros(Por favor especifica)"
    NOT_SPECIFIED = "Prefiero no decir"


class DocumentTypes(Enum):
    DNI = "DNI"
    LC = "Libreta Civica"
    LE = "Libreta de Enrolamiento"


class ServiceTypes(Enum):
    THERAPY = "Terapia"
    HORSEBACK_RIDING = "Equitación"
    ADMINISTRATIVE = "Administración"
    TRAINING = "Capacitación"


class RequestStatus(Enum):
    ACCEPTED = "Aceptada"
    REJECTED = "Rechazada"
    IN_PROCESS = "En Proceso"
    COMPLETED = "Finalizada"
    CANCELED = "Cancelada"


class RegisterTypes(Enum):
    GOOGLE = "Google"
    MANUAL = "Manual"
