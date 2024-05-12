# APP para TFG:
Con esta aplicación se puede subir documentos con los temas de las oposiciones que quiera uno y generar examenes tipo test.

# Información útil sobre la creación del contenedor Docker y la ejecución del proyecto:
* Descargamos el proyecto del repositorio.
  
* Abriremos la terminal y nos situaremos en el directorio 'aplicacion_diego'.

* A continuación, ejecutaremos el siguiente comando:

      docker compose -f .\.devcontainer\docker-compose.yml up -d

* Finalmente, accederemos a un navegador y pondremos la siguiente url:

      http://localhost:8000
