# Demo 5 · Docker Compose: API + interfaz
docker compose up -d --build     # construye y arranca los dos servicios
docker compose ps                # estado
docker compose logs -f ui        # logs de un servicio (Ctrl+C para salir)
# Navegador: http://localhost:8501 (UI)  ·  http://localhost:8000/docs (API)
docker compose down              # para y borra los contenedores
docker compose down --rmi local  # además borra las imágenes construidas por el compose
