import enum


# Roles específicos para CEDICA
class RoleEnum(enum.Enum):
    ADMINISTRACION = "ADMINISTRACION"
    VOLUNTARIADO = "VOLUNTARIADO"
    ECUESTRE = "ECUESTRE"
    TECNICA = "TECNICA"
    SYSTEM_ADMIN = "SYSTEM_ADMIN"
    SIN_ROL = "SIN_ROL"


# Acciones adicionales específicas de CEDICA
class ActionEnum(enum.Enum):
    INDEX = "index"
    SHOW = "show"
    CREATE = "create"
    UPDATE = "update"
    DESTROY = "destroy"
    ACCEPT = "accept"


# Módulos adicionales relevantes a CEDICA
class ModuleEnum(enum.Enum):
    USUARIOS = "usuarios"
    JYA = "jinete-y-amazona"
    EQUIPO = "equipo"
    PAGOS = "pagos"
    COBROS = "cobros"
    ECUESTRE = "ecuestre"
    REPORTES = "reportes"
    CONTENIDO = "contenido"
    CONTACTO = "contacto"


# Definición de acciones permitidas por módulo
MODULE_ACTIONS = {
    ModuleEnum.USUARIOS: (
        ActionEnum.INDEX,
        ActionEnum.SHOW,
        ActionEnum.CREATE,
        ActionEnum.UPDATE,
        ActionEnum.DESTROY,
        ActionEnum.ACCEPT,
    ),
    ModuleEnum.JYA: (
        ActionEnum.INDEX,
        ActionEnum.SHOW,
        ActionEnum.CREATE,
        ActionEnum.UPDATE,
        ActionEnum.DESTROY,
    ),
    ModuleEnum.ECUESTRE: (
        ActionEnum.INDEX,
        ActionEnum.SHOW,
        ActionEnum.CREATE,
        ActionEnum.UPDATE,
        ActionEnum.DESTROY,
    ),
    ModuleEnum.PAGOS: (
        ActionEnum.INDEX,
        ActionEnum.SHOW,
        ActionEnum.CREATE,
        ActionEnum.UPDATE,
        ActionEnum.DESTROY,
    ),
    ModuleEnum.COBROS: (
        ActionEnum.INDEX,
        ActionEnum.SHOW,
        ActionEnum.CREATE,
        ActionEnum.UPDATE,
        ActionEnum.DESTROY,
    ),
    ModuleEnum.EQUIPO: (
        ActionEnum.INDEX,
        ActionEnum.SHOW,
        ActionEnum.CREATE,
        ActionEnum.UPDATE,
        ActionEnum.DESTROY,
    ),
    ModuleEnum.REPORTES: (
        ActionEnum.INDEX,
        ActionEnum.SHOW,
        ActionEnum.CREATE,
        ActionEnum.UPDATE,
        ActionEnum.DESTROY,   
    ),
    ModuleEnum.CONTENIDO: tuple(ActionEnum.__members__.values()),
    ModuleEnum.CONTACTO:(
        ActionEnum.INDEX,
        ActionEnum.SHOW,
        ActionEnum.UPDATE,
        ActionEnum.DESTROY,
    ),
}


# Permisos por rol
ROLE_MODULE_PERMISSIONS = {
    RoleEnum.ADMINISTRACION: {

        ModuleEnum.USUARIOS: (
            ActionEnum.ACCEPT,
        ),

        ModuleEnum.JYA: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
        ModuleEnum.EQUIPO: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
        ModuleEnum.COBROS: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
        ModuleEnum.ECUESTRE: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
        ),
        ModuleEnum.PAGOS: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
        ModuleEnum.REPORTES: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
        ),
        ModuleEnum.CONTENIDO: MODULE_ACTIONS[ModuleEnum.CONTENIDO],
        ModuleEnum.CONTACTO:(
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        )

    },
    RoleEnum.ECUESTRE: {
        ModuleEnum.JYA: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
        ),
        ModuleEnum.ECUESTRE: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
    },
    RoleEnum.VOLUNTARIADO: {},
    RoleEnum.TECNICA: {
        ModuleEnum.ECUESTRE: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
        ),
        ModuleEnum.JYA: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
        ModuleEnum.COBROS: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
        ),
        ModuleEnum.REPORTES: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
        ),
    },
    RoleEnum.SYSTEM_ADMIN: {
        ModuleEnum.JYA: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
        ModuleEnum.EQUIPO: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
        ModuleEnum.COBROS: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
        ModuleEnum.ECUESTRE: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
        ModuleEnum.PAGOS: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
        ModuleEnum.USUARIOS: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
            ActionEnum.ACCEPT,
        ),
        ModuleEnum.REPORTES: (
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.CREATE,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        ),
        ModuleEnum.CONTENIDO: MODULE_ACTIONS[ModuleEnum.CONTENIDO],
        ModuleEnum.CONTACTO:(
            ActionEnum.INDEX,
            ActionEnum.SHOW,
            ActionEnum.UPDATE,
            ActionEnum.DESTROY,
        )
    },
}
