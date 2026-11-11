# Demo 6 · Un LLM local con Ollama + Open WebUI
docker compose up -d
docker compose exec ollama ollama pull llama3.2:1b    # ~1,3 GB de descarga
docker compose exec ollama ollama run llama3.2:1b "Explica Docker en una frase"
# Navegador: http://localhost:3000  (crea un usuario local y elige el modelo)
docker stats                                          # mira cuánta RAM usa el LLM
docker compose down                                   # los modelos se conservan en el volumen
docker compose down -v                                # además borra los volúmenes (¡adiós modelos descargados!)
