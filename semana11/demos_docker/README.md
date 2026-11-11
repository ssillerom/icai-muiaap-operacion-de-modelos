# Demos · Docker desde cero (S11)

Requisito: Docker Desktop instalado y arrancado ("Engine running").

## Gestión de librerías con uv

Las demos con Python usan **uv**: las dependencias están en `pyproject.toml` (no hay `requirements.txt`).
Dentro del Dockerfile se copia el binario de uv desde su imagen oficial y se instala todo con `uv sync`:

```dockerfile
FROM python:3.11-slim
# trae el binario de uv desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /bin/
WORKDIR /app
# uv.lock es opcional: se copia solo si existe
COPY pyproject.toml uv.lock* ./
# crea /app/.venv con las dependencias del pyproject
RUN uv sync
COPY . .
CMD ["uv", "run", "main.py"]
```

- Recomendado: ejecuta `uv lock` en local antes del build para tener versiones exactas (`uv.lock`).
  Con lock puedes usar `RUN uv sync --frozen` para garantizar que no se resuelve nada nuevo.
- `.dockerignore` excluye `.venv/`: la venv local (Windows) no sirve dentro del contenedor (Linux).
- Fuera de Docker funciona igual: `uv run train.py`.

## Cómo usar las demos

Abre una terminal en la carpeta de cada demo y sigue `comandos.sh` paso a paso.

| Demo | Carpeta | Qué enseña |
|------|---------|------------|
| 1 | `01_hola_docker` | `docker run`, imágenes vs contenedores, Python sin instalarlo |
| 2 | `02_limites_memoria` | límites de RAM con cgroups, OOM (código 137), `docker stats` |
| 3 | `03_dockerfile_entrenamiento` | primer Dockerfile con uv, `docker build`, volúmenes (`-v`) |
| 4 | `04_api_modelo` | servir un modelo con FastAPI, puertos (`-p`), `.dockerignore` |
| 5 | `05_compose_api_ui` | Docker Compose: API + interfaz Streamlit que se hablan por nombre |
| 6 | `06_llm_local_ollama` | un LLM local (Ollama + Open WebUI) con volúmenes persistentes |

Notas para Windows (PowerShell):
- `${PWD}` funciona igual que en bash.
- En vez de `echo $?` usa `$LASTEXITCODE`.
- Para probar la API es más cómodo abrir http://localhost:8000/docs que usar `curl`.
- La demo 6 necesita ~4 GB de RAM libres para Docker (Settings > Resources o `.wslconfig`).

## Limpieza: borrar contenedores e imágenes

Cada `docker run` crea un contenedor que, al terminar, **se queda parado** (puedes verlo con `docker ps -a`).
Con el tiempo se acumulan contenedores e imágenes que ocupan disco. Para limpiar:

| Qué quieres | Comando |
|-------------|---------|
| Ver todos los contenedores (también parados) | `docker ps -a` |
| Borrar un contenedor | `docker rm <nombre>` (si sigue en marcha: `docker stop <nombre>` antes, o `docker rm -f`) |
| Borrar todos los contenedores parados | `docker container prune` |
| Ver las imágenes | `docker images` |
| Borrar una imagen | `docker image rm <imagen>` |
| Borrar imágenes sin nombre ni etiqueta | `docker image prune` |

Orden: **primero el contenedor, después la imagen.** Docker no deja borrar una imagen si algún contenedor
(aunque esté parado) la usa.

### Atajo opcional: `docker run --rm`

`--rm` hace que Docker **borre el contenedor automáticamente cuando termina** su comando principal (no toca la imagen).
Es útil para pruebas puntuales (entrenar, depurar, probar un comando) porque no deja contenedores parados.
No se usa en estas demos para que se vea el ciclo completo (crear, parar, borrar), y no conviene en servicios
(API, base de datos) porque al pararlos perderías sus logs. Ejemplo:

```bash
docker run --rm python:3.11-slim python -c "print('hola')"   # se ejecuta y el contenedor se borra solo
```

