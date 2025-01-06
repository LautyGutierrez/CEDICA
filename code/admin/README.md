
## Comandos para TailwindCSS

En este proyecto, utilizamos **TailwindCSS** para gestionar los estilos. A continuación, te explicamos los dos comandos principales que puedes utilizar para generar y observar los archivos CSS.

### 1. Desarrollo: `tailwindcss --watch`

Este comando se utiliza en el entorno de desarrollo para que TailwindCSS observe cambios en tiempo real y regenere el archivo CSS cada vez que se modifiquen los estilos. Utilizamos el flag `--watch` para que esté en modo de observación constante y detecte cambios automáticamente.

```bash
tailwindcss --watch -i ./static/.dev/global.css -o ./static/.dev/tailwind_development.css
```

- i: Indica el archivo de entrada (input), que en este caso es ./static/.dev/global.css.
- o: Define el archivo de salida (output), que será generado en ./static/.dev/tailwind_development.css.

Este comando es útil durante el desarrollo para ver los cambios de forma inmediata sin tener que regenerar manualmente los estilos cada vez que modificamos el CSS.


### 2. Producción: tailwindcss --minify

Este comando se utiliza para generar la versión optimizada y minificada del archivo CSS que será usada en el entorno de producción.

```bash

tailwindcss -i ./static/.dev/global.css -o ./static/tailwind_prod.css --minify
```
- i: Archivo de entrada que toma los estilos desde ./static/.dev/global.css.
- o: Archivo de salida para el CSS minificado que será guardado en ./static/tailwind_prod.css.
- --minify: Esta opción asegura que el archivo CSS generado esté minificado, reduciendo su tamaño y optimizando la carga para un entorno de producción.

Este comando debe ejecutarse previo al despliegue del proyecto para optimizar los estilos CSS y mejorar el rendimiento en el entorno de producción.

## Usuarios de prueba  
Se han creado usuarios con roles diferentes para poder testear las funcionalidades de la aplicación:

| Email | Contraseña | Rol | 
|:----------:|:----------:|:----------:|
| admin@gmail.com   | password123   | ADMINISTRACION   |
| sysa@gmail.com    | password123   | SYSTEM_ADMIN   |
| uservoluntariado@gmail.com    | password123   | VOLUNTARIADO   |
| userecuestre@gmail.com | password123 | ECUESTRE
| usertecnica@gmail.com | password123 | TECNICA
| usersinrol@gmail.com | password123 | SIN_ROL
