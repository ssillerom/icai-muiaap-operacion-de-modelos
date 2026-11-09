# envios

Riesgo de retraso de envios: modelo, API FastAPI y frontend Streamlit.

```
pyproject.toml, .gitignore, .env.example      proyecto y entorno            (A)
src/envios/
  config.py           rutas y version                                       (HECHO)
  data/features.py    variables y preparar_fila()                           (HECHO)
  train.py            entrenamiento con datos sinteticos                    (HECHO)
  schemas.py          EnvioEntrada y PrediccionSalida                       (B1, B2)
  model/cargador.py   cargar_modelo()                                       (B3)
  inference.py        clasificar_nivel() y predecir()                       (B4)
app/
  main.py, config.py, routers/health.py                                     (HECHO)
  dependencies.py     obtener_modelo() con 503                              (C1)
  security.py         verificar_api_key()                                   (C2)
  routers/predict.py  POST /predict                                         (C3)
frontend/
  app.py              interfaz Streamlit                                    (HECHO, no tocar)
  cliente_api.py      cliente HTTP de la API                                (C4)
tests/                test_a_*, test_b_*, test_c_*                          (HECHO, no tocar)
```
