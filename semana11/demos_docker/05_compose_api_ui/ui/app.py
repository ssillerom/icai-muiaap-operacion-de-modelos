import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Clasificador de flores Iris")
st.caption(f"Llamando a la API en {API_URL}")

datos = {
    "sepal_length": st.slider("Largo del sépalo (cm)", 4.0, 8.0, 5.1),
    "sepal_width": st.slider("Ancho del sépalo (cm)", 2.0, 4.5, 3.5),
    "petal_length": st.slider("Largo del pétalo (cm)", 1.0, 7.0, 1.4),
    "petal_width": st.slider("Ancho del pétalo (cm)", 0.1, 2.5, 0.2),
}

if st.button("Predecir"):
    r = requests.post(f"{API_URL}/predict", json=datos, timeout=10)
    st.success(f"Especie predicha: {r.json()['clase']}")
