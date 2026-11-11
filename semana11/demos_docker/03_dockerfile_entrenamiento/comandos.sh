# Demo 3 · Tu primer Dockerfile (con uv)
# (Opcional, en local) uv run train.py   -> mismo script fuera de Docker
# (Recomendado) uv lock                  -> genera uv.lock y la imagen lo usará
docker build -t iris-train:1.0 .
docker images iris-train

# 1) Sin volumen: el modelo se guarda DENTRO del contenedor
docker run --name train iris-train:1.0
docker rm train                          # al borrar el contenedor, el modelo se pierde con él

# 2) Con volumen: el modelo aparece en ./models de tu PC
docker run --name train -v "${PWD}/models:/app/models" iris-train:1.0
docker rm train                          # el contenedor desaparece, models/model.joblib se queda

# Limpieza
docker image rm iris-train:1.0           # borra la imagen (antes hay que borrar sus contenedores)
