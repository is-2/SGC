Documentacion de SGC
====================

Comenzando con el Sistema Gestor de Cambios (SGC)
-------------------------------------------------

Este programa es un gestor de proyectos que maneja diversas modalidades. Gestiona los usuarios del proyecto, el estado de las fases y la gestion de los items respectivos.

### Quickstart para el manejo del software
Para que el software esté funcional. Se debe mover el proyecto en el directorio `/var/www/`. **Obs:** Acuerdese de cambiar los permisos de la carpeta a los permisos que utiliza apache (por defecto es www-data:www-data).
```bash
cp -R /mi/directorio/a/copiar /var/www/aqui
sudo chown -R www-data:www-data /var/www/aqui 
```
Donde `aqui` es el nombre de tu directorio. En nuestro caso `SGC`.

Una vez hecho estos pasos. Hay que configurar el apache para que sirva el proyecto.

### Autores
Akira Shimosoeda, Marcos Aquino.
