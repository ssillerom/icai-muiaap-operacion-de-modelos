# Demo 4 · API de un modelo (con uv)
# (Opcional, en local) uv run train.py && uv run uvicorn main:app --reload
docker build -t iris-api:1.0 .
docker run -d --name iris -p 8000:8000 iris-api:1.0
docker logs iris
# Navegador: http://localhost:8000/docs  (Swagger, la forma más cómoda de probar)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5,
       "petal_length": 1.4, "petal_width": 0.2}'

# Limpieza
docker stop iris && docker rm iris   # primero el contenedor...
docker image rm iris-api:1.0          # ...después la imagen
