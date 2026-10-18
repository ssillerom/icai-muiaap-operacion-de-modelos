# Contexto para el chat de la Clase 2 — Semana 3 (Operación de Modelos)

Documento de traspaso. Resume todo lo hecho en el chat de la **Clase 1** para que este chat pueda seguir con la **Clase 2** sin reexplicar nada. Lo que viene del material del profesor está marcado como tal; lo que es decisión de Alberto o deducción mía, también.

---

## 1. Cómo tiene que trabajar el tutor con Alberto

Alberto cursa el Máster Universitario en Inteligencia Artificial Aplicada (ICAI). Quiere aprender y poder explicar después por qué hizo cada paso, no copiar soluciones. Lo que ha ido pidiendo, a veces con bastante insistencia:

- **Responder a la pregunta que hace, literalmente y primero.** Si pregunta "¿qué es X?", la primera frase dice qué es X (tipo de dato, qué hace). Se enfadó cuando le respondí con analogías en vez de eso. Primero la explicación literal; el ejemplo con números reales después, y solo si hace falta.
- **Ejemplos concretos con sus datos** (la fila red-001, valores como 7.4, 9.4), tablas vuelta a vuelta de un bucle, "esto es lo mismo que esto otro escrito largo".
- **Paso a paso, de uno en uno**, explicando qué hace cada comando y por qué, pero sin gastar tokens de más.
- **Lenguaje simple** para los comentarios del código. Si pide algo "para copiar y pegar", dárselo ya redactado con un tono parecido al suyo (frases cortas, "le pasamos", "nos han pasado").
- **No inventar requisitos de entrega.** Si algo no está en el material del profesor, decirlo claramente ("esto no lo dice el material") en vez de asumirlo. Distinguir siempre qué viene del profe, qué es decisión suya y qué es deducción mía.
- **Primero que lo intente él**, después revisar: él escribe su versión, el tutor señala errores y explica la causa antes de dar la solución. Él valora que se le diga cuando algo está mal ("no me des la razón si no la tengo").
- **No añadir complejidad** (ni librerías ni arquitecturas más avanzadas que las de clase).
- Prefiere **nombres descriptivos** y le gusta saber de dónde sale cada nombre (de la librería, elección suya o de los datos).
- Cuando se frustra, hay que ser más directo y más corto, no más largo.

---

## 2. Material y entorno

- Asignatura: Operación de Modelos. Proyecto de Claude: "Operaciones de modelos". PDFs en el proyecto: `OM_S3_Inferencias_C1.pdf` y `MUIAAp_Operación_Modelos_S3_C1.pdf` (diapositivas de la clase 1 de la semana 3), `OM_S2_Git_Reproducibilidad.pdf`, `Operación_Model_Introd_S1.pdf` y `OM_S4_C1.pdf` (semana 4, fuera de alcance ahora).
- Repo en el Mac de Alberto: `/Users/albertorey/dev/icai-muiaap-operacion-de-modelos`. Su GitHub: `albertoreydlf`. `origin` es su fork (`albertoreydlf/icai-muiaap-operacion-de-modelos`); `upstream` es el repo del profesor (`ssillerom/...`). Las entregas van por **Pull Request en su propio fork, sin hacer merge**.
- Gestor de entornos: **`uv`** (`uv sync`, `uv run ...`). Cada proyecto tiene su `.venv`. En VS Code hay que elegir el kernel/intérprete del `.venv` correspondiente. Si la terminal muestra el nombre del proyecto entre paréntesis, el entorno está activo.
- Dependencias de `semana3/pyproject.toml`: joblib, pydantic, scikit-learn; dev: pytest, ruff. **No hay pandas.**
- Alberto usa VS Code y trabaja con notebooks.

---

## 3. Estado actual (resumen)

**Clase 1 terminada y subida a GitHub.**

- Rama: `semana3`, creada desde `origin/main` (no desde `semana1`, para no arrastrar los commits de las prácticas 1 y 2, que ya están en su PR anterior). Ya está en `origin/semana3` y vinculada a ella.
- Carpeta de entrega: `semana3/entrega-clase1/` con: copia del notebook (`01-inferencia-y-contratos-alumno-AlbertoRey.ipynb`, con `DATA_PATH` ajustada a `../assets/03-wine-quality/inference_samples.csv`), `DiagramaSemana3Clase1.drawio`, `Plan_implementación.txt` y las capturas PNG (tabla del contrato, prácticas A, B y C, orden de las 11 características, ejemplo de entrada inválida, contrato de salida, diagrama).
- El notebook original (`.../01.01-contract-and-preprocess-canvas/problem/01-inferencia-y-contratos-alumno.ipynb`) sigue modificado en su sitio y **sin commit**; es intencionado.
- Archivos sin seguimiento que NO deben subirse: `.DS_Store` (modificados por macOS) y la carpeta `Claude outputs/`. **No usar `git add .`**; añadir rutas concretas.

**Pendiente:**

1. Clase 2: completar el módulo en el *starter*.
2. Subir la clase 2 a la misma rama `semana3` (`git add` de rutas concretas, `git commit`, `git push`).
3. Crear **una sola** PR `semana3 → main` en su propio repo, sin merge, y pasar el enlace al profesor. El push ya devolvió el enlace `https://github.com/albertoreydlf/icai-muiaap-operacion-de-modelos/pull/new/semana3`.
4. Cuando acaben las clases 1 y 2, Alberto pedirá **otro `.md`** más orientado a apuntes: flujo completo, comandos usados y por qué se eligió cada argumento, para generar apuntes "a mano" y preparar el examen (hasta la práctica 3). Este documento puede servir de base, pero ese `.md` aún no se ha pedido.

---

## 4. Lo que se aprendió en la clase 1 (conceptos)

- **Inferencia vs entrenamiento:** en inferencia el modelo ya está entrenado (`.joblib`) y solo recibe datos nuevos para predecir.
- **Contrato de datos:** reglas que debe cumplir un dato para entrar. Define qué campos se aceptan, de qué tipo, qué valores son válidos y qué campos están prohibidos. Se valida **antes** de llegar al modelo (idea de las diapositivas).
- **El orden de las 11 características importa:** el modelo recibe una lista de números sin nombres. Si se cambia el orden (p. ej. `density` y `alcohol`), sigue habiendo 11 valores, no salta ningún error y la predicción sale mal sin avisar. Por eso `FEATURE_NAMES` se define una sola vez, en un solo archivo, y el resto lo importa.
- **Lectura del CSV con `csv.DictReader`:** `rows = list(reader)` da una lista de diccionarios (5 filas de datos; la cabecera no cuenta como fila, solo da las claves). `rows[0]` es una fila; `row.keys()` son las 12 columnas. Todos los valores salen como **texto**.
- **Diccionarios:** `.pop("sample_id")` quita y devuelve ese valor; `dict(x)` y `x.copy()` hacen copias; `modelo = otro` NO copia (es el mismo objeto con otro nombre). `**dic` desempaqueta un diccionario como argumentos con nombre.
- **Pydantic** (frontera, datos externos): `BaseModel`, `ConfigDict(extra="forbid")`, `Field(ge=..., le=...)`, `model_validate(dic)`, `ValidationError`. Convierte `"7.4"` en `7.4`, rechaza columnas extra (`type=extra_forbidden`) y valores fuera de rango (`type=less_than_equal`). Ambos casos son `ValidationError`, con distinto `type=`.
- **`@dataclass(frozen=True, slots=True)`** (interior, datos ya validados): NO valida rangos NI convierte tipos (acepta `ph=99.0` y deja los demás valores como strings; las anotaciones `: float` son solo etiquetas). Lo que hace: genera el `__init__` automático, un `print` legible y comparación con `==`; con `frozen=True` no se puede modificar después de crearlo; permite acceso por nombre (`muestra.alcohol`). Falla con `TypeError` si faltan o sobran campos.
- **Decisión de diseño de Alberto:** Pydantic en la entrada del CSV porque son datos externos y hay que comprobar rangos, rechazar columnas extra y convertir strings a float; dataclass dentro del módulo (p. ej. `WineFeatures`) con datos ya validados, para agruparlos con nombres fijos e inmutables.
- **`getattr(objeto, "nombre")`** lee un atributo cuando el nombre está en una variable: `getattr(request, "alcohol")` equivale a `request.alcohol`.
- **El objeto `request`** que devuelve `model_validate` no es ni lista ni diccionario: es una instancia de la clase del contrato, con los 11 campos ya como `float`, accesibles con punto.
- **Vector ordenado:** `vector = [getattr(request, name) for name in FEATURE_NAMES]` (equivale a un bucle `for` que va haciendo `append`).
- **Artefacto del modelo (`.joblib`):** guarda el estimador, los nombres y orden de las características y las versiones. Antes de predecir hay que comprobar que coinciden con `FEATURE_NAMES` (lo pide el starter).

---

## 5. Datos y código de referencia

**CSV** `assets/03-wine-quality/inference_samples.csv`: 5 filas (red-001 … red-005), 12 columnas:
`sample_id, fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol`.
Fila red-001: `7.4, 0.7, 0.0, 1.9, 0.076, 11.0, 34.0, 0.9978, 3.51, 0.56, 9.4`.

**Contrato de entrada que escribió Alberto (notebook).** `sample_id` se separa antes de validar con `.pop`. Los rangos son **decisión suya**: algunos salen de la diapositiva y otros, como el del pH, de conocimiento general; el profesor no los fija en el material que tenemos.

```python
class WineQualityRequestPydantic(BaseModel):
    model_config = ConfigDict(extra="forbid")
    fixed_acidity: float = Field(ge=0, le=20)
    volatile_acidity: float = Field(ge=0, le=2)
    citric_acid: float = Field(ge=0, le=2)
    residual_sugar: float = Field(ge=0, le=20)
    chlorides: float = Field(ge=0, le=1)
    free_sulfur_dioxide: float = Field(ge=0, le=100)
    total_sulfur_dioxide: float = Field(ge=0, le=300)
    density: float = Field(ge=0.98, le=1.01)
    ph: float = Field(ge=2.5, le=4.5)
    sulphates: float = Field(ge=0, le=3)
    alcohol: float = Field(ge=5, le=20)

model_row = dict(row)
sample_id = model_row.pop("sample_id")
request = WineQualityRequestPydantic.model_validate(model_row)
```

**Contrato de salida que escribió Alberto (notebook).** Ojo: mezcla inglés y español; en el starter hay que usar **los nombres que exijan los tests**, que probablemente sean los del profesor (`sample_id`, `quality_band`, `confidence`, `model_version`, `preprocessing_version`).

```python
class WineQualityPredictionPydantic(BaseModel):
    sample_id: str = Field(min_length=1)
    quality_band: str = Field(min_length=1)
    confianza: float = Field(ge=0, le=1)
    version_modelo: str = Field(min_length=1)
    version_preprocesado: str = Field(min_length=1)
```

Ejemplo de salida para red-001 (valores inventados para el ejercicio): `sample_id='red-001' quality_band='acceptable' confianza=0.62 version_modelo='wine-quality-rf-v1' version_preprocesado='wine-red-features-v1'`.
Valores de versión de las diapositivas: `model_version: wine-quality-rf-v1`, `preprocessing_version: wine-red-features-v1`. Etiquetas de calidad que aparecen como ejemplo: `acceptable`, `needs_review` (no sabemos si es una lista cerrada).

**Orden de las características (`FEATURE_NAMES`, dado en el starter, no se cambia):**
`fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol`.

---

## 6. Responsabilidad de cada archivo (Checkpoint 3, ya entregado)

Los nombres de las diapositivas: `contracts.py` valida, `preprocess.py` prepara, `inference.py` carga y predice, `predict_file.py` coordina el flujo. Flujo: `CSV → contracts.py → preprocess.py → inference.py → predict_file.py → predictions.csv`.

- `contracts.py`: contratos de entrada y de salida con Pydantic; valida una fila ya leída.
- `preprocess.py`: convierte la muestra validada en el vector ordenado de 11 números según `FEATURE_NAMES`; `sample_id` no entra.
- `inference.py`: carga el `.joblib`, comprueba que sus características coinciden con `FEATURE_NAMES` (falla antes de predecir si no), y predice con el vector.
- `predict_file.py`: es el script que se ejecuta (`--input`, `--output`); lee el CSV y llama fila a fila a los otros tres. Esta asignación de "leer el CSV" a `predict_file.py` es **deducción** a partir de "coordinar el flujo", no una frase literal del material.
- **CSV parcial:** se validan y predicen todas las filas, guardando los resultados en memoria, y el archivo de salida se abre solo al final si todo ha ido bien. Coincide con la pista 4 de la guía del profesor.

---

## 7. Clase 2: lo que sabemos del starter

**Ruta del starter:** `semana3/modules/03-inference-contracts/exercises/01-local-inference/01.02-wine-quality-inference-module/problem/starter/`. Tiene su propio `pyproject.toml`, `uv.lock` y `.venv`, así que los comandos se ejecutan **desde esa carpeta**.

Estructura: `assets/` (con `inference_samples.csv`), `src/model_inference/{contracts,preprocess,inference,predict_file}.py`, `tests/{test_inference_components.py, test_predict_file.py}`. El profesor indica que el modelo va en `models/wine_quality_classifier.joblib` (lo copia el docente; **no sabemos si Alberto ya lo tiene**) y que se trabaja con la carpeta `.tmp/` local (ignorada por git).

Qué piden los archivos (TODOs del starter):

- `contracts.py`: implementar `WineQualityRequest` y `WineQualityPrediction` con Pydantic, revisando el CSV y prohibiendo columnas extra. (Ojo: los nombres de clase del starter no llevan el sufijo `Pydantic` del notebook.)
- `preprocess.py`: `FEATURE_NAMES` ya viene dado; implementar `WineFeatures` y `preprocess_wine_request()`. El orden debe coincidir con el artefacto, no con un orden arbitrario del CSV.
- `inference.py`: declarar `DEFAULT_MODEL_PATH`, `load_wine_quality_model()` e `infer_wine_quality()`; comprobar las características del artefacto antes de llamar al clasificador.
- `predict_file.py`: CLI `python -m model_inference.predict_file --input <csv> --output <csv>`; no dejar archivo de salida parcial si alguna fila es inválida.

**Guion docente (resumen, el profesor lo usa en 120 min):** empezar con `uv sync` y `uv run pytest` (el rojo es el punto de partida, no se edita aún) → `contracts.py` (entrada estricta, salida con categoría, confianza y versiones) → `preprocess.py` (incluida la versión del preprocesado; `sample_id` no aparece en el vector) → `load_wine_quality_model()` e `infer_wine_quality()` (comprobar estimador, versión, nombres y orden antes de predecir; el objeto cargado debe tener `predict` y `predict_proba`) → `predict_file.py` (leer, validar, transformar, inferir y escribir al final) → tres fallos de aceptación (columna extra, segunda fila inválida, artefacto incompatible) → Ruff y pytest en verde.

**Comando de aceptación**, desde la carpeta del starter:

```bash
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
uv run python -m model_inference.predict_file \
  --input assets/inference_samples.csv \
  --output .tmp/wine_predictions.csv
```

**Reglas del juego:** hay una carpeta `solutions/` que el profesor mantiene cerrada hasta el debrief; **no abrirla**. La guía trae "pistas graduadas" que solo deben darse si Alberto se bloquea, y entonces como pregunta, no como código. Mejor hacer pasar un test cada vez y leer bien el primer fallo antes de escribir.

---

## 8. Comandos usados y por qué

**uv / entorno**

- `uv sync`: instala las dependencias del `pyproject.toml` en el `.venv` del proyecto.
- `uv run <comando>`: ejecuta el comando dentro de ese entorno, sin activarlo a mano.

**Git (los usados para la entrega de la clase 1)**

- `git fetch origin`: trae la información más reciente de su GitHub sin tocar archivos.
- `git switch -c semana3 origin/main`: crea la rama `semana3` partiendo de `main` de su fork y se cambia a ella (`-c` = crear). Los cambios sin guardar viajan con él.
- `mkdir -p semana3/entrega-clase1`: crea la carpeta (`-p` evita error si ya existe).
- `git status`: ver qué cambia y qué está preparado.
- `git add <rutas concretas>`: prepara solo esos archivos. No `git add .`, porque arrastraría `.DS_Store` y `Claude outputs/`.
- `git commit -m "mensaje"`: guarda lo preparado como commit.
- `git push -u origin semana3`: sube la rama a su GitHub y la vincula a `origin/semana3` (`-u` = recordar el vínculo, y luego basta `git push`).
- Se le dio el aviso de usar ese comando exacto la primera vez: la rama había nacido apuntando a `origin/main`.
- Error visto: `.git/index.lock: File exists`. Es un archivo temporal que Git deja mientras trabaja; lo normal es que VS Code tuviera Git ocupado. Se comprobó con `ps aux | grep "[g]it "` que no había procesos y se borró con `rm .git/index.lock`.

---

## 9. Errores típicos de Alberto (para anticiparlos)

- Erratas en los nombres de campos del contrato (`fixed_acidfity`, `citric_acidity`): con `extra="forbid"` fallan, así que conviene copiar los nombres de `FEATURE_NAMES` / del CSV.
- Confusión entre `list(reader)` y filas sueltas, y mezclar placeholders del profesor (`rows = []`) con su código.
- Predecir mal el nombre de las excepciones (`InvalidRowError`…): las dos son `ValidationError` con distinto `type=`.
- Llamar `.model_validate` sobre una dataclass (no existe) o esperar que la dataclass valide.
- Rutas relativas al mover notebooks (`DATA_PATH` con `../`): se rompen al cambiar de carpeta.
- Reutilizar nombres de variable (`request`) en celdas distintas, que luego apuntan a otra cosa.

---

## 10. Dudas abiertas (no están en el material que tenemos)

- Dónde y cómo entrega la clase 2 el profesor (dentro del propio *starter* en su rama, en una copia, etc.). Habría que confirmarlo con él.
- Si el modelo `models/wine_quality_classifier.joblib` ya está en el starter de Alberto o falta.
- Nombres exactos de campos y clases que exigen los tests de la clase 2 (hay que leer `tests/` antes de escribir `contracts.py`).
- Dónde estaba el "lienzo compartido" de la clase 1 y si hay algo más por entregar de ella.
- Si el profesor espera para la semana 3 el mismo flujo de PR sin merge que en las prácticas 1 y 2.
- Pequeños retoques opcionales que no se han hecho en el notebook de la clase 1: comentarios de la Práctica B que mencionan `InvalidRowError` / `InvalidValueError` (los errores reales son `ValidationError`) y un comentario "me lo he inventado" en el contrato de salida.

---

## 11. Cómo empezar la clase 2 (propuesta)

1. `cd` a la carpeta del *starter* y ejecutar `uv sync` y `uv run pytest`. Leer el primer fallo con Alberto, sin editar nada.
2. Leer `tests/` para saber qué nombres y firmas exigen, y abrir `problem/readme.md`.
3. Ir archivo por archivo en el orden `contracts.py → preprocess.py → inference.py → predict_file.py`, haciendo pasar un test cada vez. Alberto escribe, el tutor revisa y explica los errores antes de dar la solución.
4. Cada cierto tiempo, `git add` de rutas concretas + commit en la rama `semana3`; al terminar, `git push` y crear la PR.
