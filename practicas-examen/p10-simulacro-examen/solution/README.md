# envios - solucion del simulacro (PROFESOR)

Solucion de referencia de la practica 10. No repartir.

```bash
uv sync
uv run entrenar
uv run python scripts/nota.py          # 10.00 / 10
cp .env.example .env
uv run uvicorn app.main:app --reload
uv run streamlit run frontend/app.py
```

## Rubrica automatica (scripts/nota.py)

| Bloque | Tests | Puntos | Que se evalua |
|---|---:|---:|---|
| A - Proyecto y entorno | 5 | 2 | `uvicorn` en dependencias, `pytest` en el grupo `dev`, script `entrenar`, `.gitignore` con `models/` y `.env`, `.env.example` sin secretos |
| B - Contrato y modelo | 40 | 4 | `EnvioEntrada` (rangos, `Literal`, `extra="forbid"`, `field_validator` before, `model_validator` nacional <= 1500 km), `PrediccionSalida`, carga unica del payload con `ModeloIncompatible`, `clasificar_nivel` y `predecir` |
| C - API e integracion | 24 | 4 | 503 en la dependencia, 401 con `compare_digest`, router protegido con `dependencies=[...]`, `responses` documentados, cliente `httpx` con `base_url`/cabecera/timeout y traduccion de 200/422/401/503/red |

Con el starter sin tocar la nota es de unos 0,8 puntos: algunos tests pasan
por defecto (limites validos con un modelo vacio, `/health`, que
`ModeloIncompatible` herede de `ValueError`).

## Diferencias con las practicas 1-9 (intencionadas)

- Dominio nuevo (envios) y artefacto distinto: un unico joblib con un
  diccionario (`payload`) en lugar de `model.joblib` + `manifest.json`.
- Campo booleano (`es_internacional`) y regla entre campos que depende de el.
- Los TODOs son escuetos: la especificacion esta en el enunciado.
- El bloque A se arregla con `uv add uvicorn`, `uv remove pytest`,
  `uv add --dev pytest` y editando `[project.scripts]`.

## Errores frecuentes que conviene revisar a mano

- `field_validator` en modo `after` sobre `transportista`: falla con `" RAPIDO "`.
- Capturar `Exception` en `obtener_modelo()` (oculta bugs como 503).
- Comparar la API key con `==` o devolver 403 en lugar de 401.
- Proteger la ruta con un parametro en lugar de en el router (funciona, pero
  conviene comentarlo).
- Crear el cliente HTTP dentro de `consultar()` ignorando el que se recibe: los
  tests con `TestClient` y `MockTransport` fallan.
- Dejar `pytest` tambien en `dependencies` despues de anadirlo a `dev`.
