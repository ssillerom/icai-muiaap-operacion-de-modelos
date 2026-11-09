"""Frontend Streamlit (HECHO, no tocar).

Arranque, desde la raiz del proyecto:  uv run streamlit run frontend/app.py

Esta pagina solo se ocupa de la PRESENTACION: pinta el formulario, envia los
valores a `gateway.consultar_modelo()` y muestra lo que este devuelva.
No valida reglas de negocio ni carga el modelo: eso es cosa del backend.
Por eso los limites de los widgets son amplios a proposito.
"""
import streamlit as st

import gateway

COLORES_RIESGO = {"bajo": "green", "medio": "orange", "alto": "red"}

st.set_page_config(page_title="Riesgo de cancelacion", page_icon="🏨")
st.title("🏨 Riesgo de cancelación de una reserva")
st.caption("Datos sintéticos · Operación de Modelos (MUIAAp) · Comillas ICAI")

with st.form("reserva"):
    col1, col2 = st.columns(2)
    antelacion = col1.number_input("Antelación (días)", min_value=0, max_value=1000, value=30)
    noches = col2.number_input("Noches", min_value=0, max_value=60, value=3)
    adultos = col1.number_input("Adultos", min_value=0, max_value=10, value=2)
    ninos = col2.number_input("Niños", min_value=0, max_value=10, value=0)
    precio = col1.number_input(
        "Precio por noche (€)", min_value=0.0, max_value=5000.0, value=120.0, step=10.0
    )
    canal = col2.selectbox("Canal de reserva", ["web", "agencia", "telefono"])
    cancelaciones = col1.number_input("Cancelaciones previas", min_value=0, max_value=20, value=0)
    peticiones = col2.number_input("Peticiones especiales", min_value=0, max_value=10, value=1)
    enviado = st.form_submit_button("Calcular riesgo", type="primary")

if enviado:
    valores = {
        "antelacion_dias": antelacion,
        "noches": noches,
        "adultos": adultos,
        "ninos": ninos,
        "precio_noche": precio,
        "canal": canal,
        "cancelaciones_previas": cancelaciones,
        "peticiones_especiales": peticiones,
    }
    with st.spinner("Consultando el modelo..."):
        respuesta = gateway.consultar_modelo(valores)

    if respuesta.ok:
        prediccion = respuesta.prediccion
        color = COLORES_RIESGO[prediccion.riesgo]
        st.metric("Probabilidad de cancelación", f"{prediccion.probabilidad_cancelacion:.0%}")
        st.markdown(f"Riesgo: :{color}[**{prediccion.riesgo.upper()}**]")
        st.caption(f"Modelo {prediccion.version_modelo}")
    else:
        st.error("No se ha podido calcular el riesgo:")
        for mensaje in respuesta.errores:
            st.markdown(f"- {mensaje}")
