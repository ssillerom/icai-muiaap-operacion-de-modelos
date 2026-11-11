# Demo 1 · Hola Docker
docker --version                         # ¿está instalado?
docker run hello-world                   # descarga la imagen y la ejecuta
docker run -it python:3.11-slim python   # Python sin instalar nada (exit() para salir)
docker ps -a                             # los contenedores siguen ahí, parados (Exited)
docker images                            # imágenes descargadas

# Limpieza (ver también el README)
docker container prune                   # borra todos los contenedores parados (pide confirmación)
docker image rm hello-world              # borra la imagen hello-world
