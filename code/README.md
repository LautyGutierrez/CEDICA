# CEDICA

Proyecto del **Grupo 21** para la materia **Proyecto de Software 2024** 

El objetivo de este trabajo integrador es desarrollar una Aplicación Web que permita contar con mucha de la información en formato digital que contienen los diferentes procesos de trabajo de una institución de TACAs. Los usuarios directos serían los integrantes del equipo de CEDICA.

La solución tendrá un aplicación interna de administración (para usuarios y administradores) desarrollada en Python y Flask, y un portal web desarrollado en Vue.js donde se podrán visualizar los servicios ofrecidos por la institución. Utilizaremos una base de datos PostgreSQL y se implementará una API con los endpoints necesarios para la integración de estas dos aplicaciones.


## Aplicacion privada

    
La aplicación permitirá:

- Mantener un registro histórico de los legajos de los J&A (Jinetes y Amazonas), incluyendo anexos de documentación necesaria.

- Mantener un registro de los Legajos de los profesionales del equipo.

- Registrar la información de los caballos.

- Obtener reportes estadísticos: la aplicación debe producir reportes que presenten estadísticas relevantes sobre los datos manejados.

#### El panel se encuentra en [este link](https://admin-grupo21.proyecto2024.linti.unlp.edu.ar/login).

#### El codigo fuente se encuentra en la carpeta [admin](./admin).

```bash

code/
├── admin/
│   ├── src/
│   │   ├── core/
│   │   ├── utils/
│   │   └── web/
│   │       ├── controllers/
│   │       ├── forms/
│   │       ├── templates/
│   │       └── __init__.py
│   ├── .env
│   ├── static/
│   ├── tests/
│   └── __init__.py
├── README.md
└── ...

```

#### Para mas información sobre la aplicación privada, ver el [README.md](./admin/README.md) de la misma.




## Desarrolladores
- [Cirielli Franco Giovanni](https://github.com/FrancoCirielli16)
- [de Urquiza Juan Cruz](https://github.com/deurquizajuancruz)
- [Gutierrez Lautaro Joaquin](https://github.com/LautyGutierrez)
- [Zapettini Zoe](https://github.com/zoezapettini)

