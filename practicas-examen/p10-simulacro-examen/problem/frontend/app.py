"""Frontend Streamlit (HECHO, no tocar).

Arranque, desde la raiz del proyecto:  uv run streamlit run frontend/app.py
Necesita la API en marcha (uv run uvicorn app.main:app).
"""
import streamlit as st

import cliente_api

COLORES = {"a_tiempo": "green", "riesgo": "orange", "retraso_probable": "red"}
TEXTOS = {"a_tiempo": "A TIEMPO", "riesgo": "EN RIESGO", "retraso_probable": "RETRASO PROBABLE"}

st.set_page_config(page_title="Riesgo de retraso", page_icon="📦")
st.title("📦 ¿Llegará tarde este envío?")
st.caption("Datos sintéticos · Simulacro de examen · Operación de Modelos (MUIAAp)")

with st.form("envio"):
    col1, col2 = st.columns(2)
    distancia = col1.number_input("Distancia (km)", min_value=0.0, max_value=20000.0, value=450.0)
    peso = col2.number_input("Peso (kg)", min_value=0.0, max_value=500.0, value=2.5)
    dias = col1.number_input("Días prometidos", min_value=0, max_value=60, value=3)
    cola = col2.number_input("Envíos en cola", min_value=0, max_value=5000, value=120)
    transportista = col1.selectbox("Transportista", ["rapido", "estandar", "economico"])
    internacional = col2.checkbox("Envío internacional")
    enviado = st.form_submit_button("Calcular riesgo", type="primary")

if enviado:
    valores = {
        "distancia_km": distancia,
        "peso_kg": peso,
        "dias_prometidos": dias,
        "transportista": transportista,
        "es_internacional": internacional,
        "envios_en_cola": cola,
    }
    with st.spinner("Consultando la API..."):
        respuesta = cliente_api.consultar(valores)

    if respuesta.ok:
        prediccion = respuesta.prediccion
        st.metric("Probabilidad de retraso", f"{prediccion.probabilidad_retraso:.0%}")
        st.markdown(f"Estado: :{COLORES[prediccion.nivel]}[**{TEXTOS[prediccion.nivel]}**]")
        st.caption(f"Modelo {prediccion.version_modelo}")
    else:
        st.error("No se ha podido calcular el riesgo:")
        for mensaje in respuesta.errores:
            st.markdown(f"- {mensaje}")
