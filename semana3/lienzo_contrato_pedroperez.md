# Lienzo 3.1 — Contrato de inferencia (vino tinto)

Especificación del módulo local de inferencia de la clase 2. Todo lo que se
describe aquí está comprobado ejecutando `model_inference.predict_file` del
`starter` (ver [casos de fallo](#5-casos-de-fallo-y-comportamiento-de-la-cli)).
Diagrama de flujo: [`flujo_pedroperez.drawio`](flujo_pedroperez.drawio).

## 1. Entrenamiento, artefacto y datos nuevos

| Elemento | Qué es | Dónde vive | ¿Va a Git? |
| --- | --- | --- | --- |
| Datos de entrenamiento | Dataset completo *Red Wine Quality* (UCI) con la columna objetivo `quality` | Solo el profesorado, para generar el modelo | No |
| Artefacto | `models/wine_quality_classifier.joblib`: diccionario con `estimator`, `feature_names` y `model_version` | Carpeta local `models/` | No (`models/` está en `.gitignore`) |
| Datos nuevos | `inference_samples.csv`: 5 filas sin etiqueta, con `sample_id` y las 11 características | `assets/` | Sí (muestra docente) |

En inferencia solo se carga el artefacto y se aplica a datos nuevos: no se
reentrena y no hace falta `quality`.

## 2. Contrato de entrada

Cada fila del CSV trae `sample_id` más las 11 características. `sample_id`
identifica la muestra, se separa antes de validar y **no entra en el vector**.
Los límites son inclusivos (`ge`/`le`). Del CSV todo llega como texto y Pydantic
lo convierte a `float`.

| # | Variable | Tipo | Unidad | Mínimo | Máximo | Valor ausente |
| --- | --- | --- | --- | --- | --- | --- |
| — | `sample_id` | str, no vacío | identificador | — | — | Error |
| 1 | `fixed_acidity` | float | g/dm³ (como ácido tartárico) | 0 | 20 | Error |
| 2 | `volatile_acidity` | float | g/dm³ (como ácido acético) | 0 | 2 | Error |
| 3 | `citric_acid` | float | g/dm³ | 0 | 2 | Error |
| 4 | `residual_sugar` | float | g/dm³ | 0 | 20 | Error |
| 5 | `chlorides` | float | g/dm³ (como cloruro sódico) | 0 | 1 | Error |
| 6 | `free_sulfur_dioxide` | float | mg/dm³ | 0 | 100 | Error |
| 7 | `total_sulfur_dioxide` | float | mg/dm³ | 0 | 300 | Error |
| 8 | `density` | float | g/cm³ (ver nota) | 0,98 | 1,01 | Error |
| 9 | `ph` | float | adimensional (escala de pH) | 2,5 | 4,5 | Error |
| 10 | `sulphates` | float | g/dm³ (como sulfato potásico) | 0 | 3 | Error |
| 11 | `alcohol` | float | % vol. | 5 | 20 | Error |

**Valores ausentes:** ninguna variable admite ausentes ni se imputan. Una celda
vacía, una columna que falta o una fila con menos campos que la cabecera
terminan en error y detienen la ejecución.

**Valores finitos:** `nan` e `inf` se rechazan (`allow_inf_nan=False`).

**Formato numérico:** se aceptan `7.4`, `10`, `1e1` y con espacios alrededor
(` 3.51 `). Se rechazan la coma decimal (`3,51`), el texto (`abc`, `true`) y la
celda vacía.

**Notas sobre las unidades:** el README del repo no las indica. Se toman de la
descripción del dataset de Cortez et al. (2009), según
[estos apuntes](https://www.stat.cmu.edu/~rnugent/PCMI2016/WineQuality.pdf). Esa
descripción escribe la densidad en g/dm³, pero los valores del CSV (≈ 0,998) y
el rango del contrato (0,98–1,01) corresponden a g/cm³, que es la unidad
usada aquí. El pH no tiene unidad. La
[ficha de UCI](https://archive.ics.uci.edu/dataset/186/wine+qualitys) indica que
el dataset original no tiene valores ausentes.

## 3. Orden del vector

El clasificador recibe una lista de 11 números sin nombres, en el orden de
`FEATURE_NAMES` (`preprocess.py`):

1. `fixed_acidity`
2. `volatile_acidity`
3. `citric_acid`
4. `residual_sugar`
5. `chlorides`
6. `free_sulfur_dioxide`
7. `total_sulfur_dioxide`
8. `density`
9. `ph`
10. `sulphates`
11. `alcohol`

Si dos columnas se intercambian (por ejemplo `density` y `alcohol`), el vector
sigue teniendo 11 valores y el modelo no da error: predice mal sin avisar. Por
eso el orden se define una sola vez y el cargador comprueba que
`feature_names` del artefacto coincide con `FEATURE_NAMES` (si no, error).

## 4. Contrato de salida

| Variable | Tipo | Restricción | Valor ausente |
| --- | --- | --- | --- |
| `sample_id` | str | El que traía la fila de entrada | No existe |
| `quality_band` | str | Solo `needs_review`, `acceptable` o `excellent` | No existe |
| `confidence` | float | Entre 0 y 1, finito (probabilidad máxima de `predict_proba`) | No existe |
| `model_version` | str | No vacío; viene del artefacto | No existe |
| `preprocessing_version` | str | No vacío; constante `wine-red-features-v1` | No existe |

La salida también se valida con Pydantic (`extra="forbid"`): una etiqueta fuera
de las tres bandas se rechaza. Ejemplo de salida del CSV con el modelo del
curso (`wine-quality-rf-v1`) para `red-001`; la confianza puede variar algo con
otra versión de scikit-learn:

```csv
sample_id,quality_band,confidence,model_version,preprocessing_version
red-001,needs_review,0.8637529232968751,wine-quality-rf-v1,wine-red-features-v1
```

## 5. Casos de fallo y comportamiento de la CLI

La CLI termina con código **0** si todo va bien y con **2** ante cualquier
error: escribe `Error: ...` en `stderr` y **no crea el fichero de salida**. Lee
y valida todas las filas antes de escribir nada (todo o nada) y se detiene en
el primer error, indicando la fila y su `sample_id`.

Fila válida y fila con una columna no permitida:

```csv
sample_id,fixed_acidity,volatile_acidity,citric_acid,residual_sugar,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,ph,sulphates,alcohol
red-001,7.4,0.7,0.0,1.9,0.076,11.0,34.0,0.9978,3.51,0.56,9.4

sample_id,fixed_acidity,volatile_acidity,citric_acid,residual_sugar,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,ph,sulphates,alcohol,unexpected_field
red-001,7.4,0.7,0.0,1.9,0.076,11.0,34.0,0.9978,3.51,0.56,9.4,1
```

| Caso | Ejemplo | Resultado (código 2, sin salida) |
| --- | --- | --- |
| CSV de entrada inexistente | `--input no_existe.csv` | `No such file or directory` |
| Modelo inexistente | `--model no_existe.joblib` | `No existe el modelo: ...` (antes de leer filas) |
| Artefacto que no es un diccionario | `.joblib` con una lista | `El artefacto debe ser un diccionario` |
| Artefacto sin clasificador compatible | falta `estimator` o no tiene `predict_proba` | `El artefacto no contiene un clasificador compatible` |
| Falta `feature_names` o `model_version` en el artefacto | clave ausente | `Falta la clave '...' en el artefacto` |
| `model_version` vacío | `""` | `model_version no puede estar vacío` |
| Orden de características distinto en el artefacto | `feature_names` invertidos | `feature_names del modelo no coincide con FEATURE_NAMES` |
| Columna no permitida | `unexpected_field` | `unexpected_field ... extra_forbidden` |
| Columna obligatoria que falta | CSV sin `alcohol` | `alcohol ... Field required` |
| `sample_id` ausente o vacío | sin columna o celda vacía | `falta sample_id` |
| Valor ausente | `alcohol` vacío | `float_parsing` (no es un número válido) |
| Tipo incorrecto | `alcohol = abc`, `ph = 3,51` | `float_parsing` |
| Valor no finito | `density = nan` o `inf` | `finite_number` |
| Fuera de rango | `ph = 99`, `ph = 4.51`, `alcohol = -1` | `less_than_equal` / `greater_than_equal` |
| Fila con menos campos que la cabecera | `red-001,7.4,0.7` | Error por cada campo sin valor |
| Segunda fila inválida | `red-002` con `alcohol = invalid` | `fila 3 (sample_id='red-002')`; no se escribe ni la primera fila |
| Etiqueta predicha fuera de las tres bandas | modelo que devuelve `unknown` | `quality_band ... literal_error` |

**Comportamientos actuales que el contrato no cubre** (observados, no
corregidos):

- CSV vacío o con solo la cabecera: termina con código 0, `0 predicciones` y
  escribe un CSV solo con la cabecera.
- `sample_id` duplicado: se acepta y se predice cada fila.
- Fila con más campos que la cabecera: se rechaza, pero con un mensaje poco
  claro (`Keys should be strings`).
- Si el fichero de salida ya existía y la ejecución falla, no se toca: queda el
  antiguo.
- Artefacto ilegible o corrupto (un `.joblib` que no se puede deserializar): la
  CLI termina con un traceback y código **1**, no controlado, aunque tampoco
  crea la salida.

El diagrama muestra la comprobación de columnas como un paso previo; en el
código esa comprobación ocurre al validar cada fila, así que la primera fila ya
falla.

## 6. Criterios de aceptación

1. **Entrada válida:** con `inference_samples.csv` y el modelo del docente, el
   comando escribe 5 filas, una por `sample_id`, con las columnas `sample_id`,
   `quality_band`, `confidence`, `model_version` y `preprocessing_version`, y
   termina con código 0.
2. **Entrada o artefacto inválido:** ante una columna extra, una columna que
   falta, un valor ausente, un tipo incorrecto, un valor fuera de rango, una
   fila inválida posterior o un artefacto incompatible, termina con código 2,
   un mensaje con la fila y el campo, y sin fichero de salida.
3. **Orden y artefacto:** el vector respeta el orden de `FEATURE_NAMES` y
   excluye `sample_id`, y el cargador comprueba `feature_names` y la interfaz
   mínima del estimador (`predict` y `predict_proba`).

Comprobación, desde `problem/starter`:

```bash
uv sync
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
uv run python -m model_inference.predict_file --input assets/inference_samples.csv --output .tmp/wine_predictions.csv
```

## 7. Plan de implementación

| Archivo | Responsabilidad |
| --- | --- |
| `contracts.py` | `WineQualityRequest` (11 características con rangos, sin extras) y `WineQualityPrediction` (banda, confianza y versiones) |
| `preprocess.py` | `FEATURE_NAMES`, `PREPROCESSING_VERSION` y `preprocess_wine_request()`, que construye el vector sin `sample_id` |
| `inference.py` | `load_wine_quality_model()` (comprueba el artefacto) e `infer_wine_quality()` (predice y valida la salida) |
| `predict_file.py` | CLI: lee el CSV, valida fila a fila, predice y escribe el CSV solo si todo es válido |

No se lee el CSV en `preprocess.py` ni se carga el `.joblib` desde la CLI: la
CLI llama a `inference.py`.
