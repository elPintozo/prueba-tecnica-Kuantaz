# prueba-tecnica-Kuantaz
Repositorio con un breve proyecto desarrollado con el framework Flask

## Solicitudes
* Crear servicios para listar instituciones,proyectos y usuarios.
    -   [GET].../instituciones 
    -   [GET].../proyectos
    -   [GET].../usuarios
* Crear servicio para listar una institución (Filtró por id) con sus respectivos proyectos y responsable del proyecto.
    -   [GET].../instituciones/detalle-proyecto-y-responsables/{id_institucion}
* Crear servicio para listar un usuario (filtro por Rut) con sus respectivos proyectos.
    -   [GET].../usuarios/{id_ususario}
    -   [GET].../usuarios/por-rut/{rut_ususario}
* Crear servicio para listar instituciones donde a cada institución se agregue a la dirección la ubicación de google maps ejemplo: “https://www.google.com/maps/search/+ direccion ” y la abreviación del nombre (solo los primeros tres caracteres).
    -   [GET].../instituciones/con-direccion
* Crear servicio para listar los proyectos que la respuesta sea el nombre del proyecto y los días que faltan para su término. 
    -   [GET].../proyectos/tiempo-restante

## Suma Puntos
* Crear documentación con Swagger
    - http://127.0.0.1:5000/api/docs/
* Crear archivo Postman u otro.
    - /Kuantaz.postman_collection.json
* Ocupa ORM de preferencia sqlalchemy
    - prueba-tecnica-kuantaz/models/modelos.py
* Test unitarios
    - Comando: python -m unittest discover -s tests