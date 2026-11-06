import streamlit as st
from modelo import predict_toy

st.set_page_config(page_title="Churn con memoria", layout="centered")
st.title("Churn con memoria")
st.caption("Regla de juguete. No usar para tomar decisiones sobre clientes.")

# A: iniciar una sola vez, no en cada rerun.
if "history" not in st.session_state:
    st.session_state.history = []

def submit_prediction():
    # Leer los valores nuevos desde las keys, no mediante args del callback.
    inputs = {name: st.session_state[name] for name in
              ("tenure_months", "monthly_spend_eur", "contract", "support_calls")}
    result = predict_toy(**inputs)
    # B: una fila por submit. No predecir en cada rerun.
    st.session_state.history.append({**inputs, **result})

def clear_history():
    st.session_state.history = []

with st.form("churn_form"):
    st.slider("Antigüedad (meses)", 0, 72, 6, key="tenure_months")
    st.number_input("Gasto mensual (EUR)", 0.0, 200.0, 80.0,
                    step=5.0, key="monthly_spend_eur")
    st.selectbox("Contrato", ["Mensual", "Anual"], key="contract")
    st.slider("Llamadas a soporte", 0, 5, 2, key="support_calls")
    st.form_submit_button("Predecir y guardar", on_click=submit_prediction)

# Fuera del form: provoca rerun sin añadir otra predicción.
st.checkbox("Mostrar ayuda", key="show_help")
if st.session_state.show_help:
    st.info("El form envía todos sus valores al pulsar submit. El historial vive en esta sesión.")

# C: dibujar SIEMPRE desde el estado, no solo dentro del if submit.
st.metric("Predicciones guardadas", len(st.session_state.history))
if st.session_state.history:
    last = st.session_state.history[-1]
    st.success(f"Último riesgo: {last['risk']} ({last['probability']:.0%})")
    st.dataframe(st.session_state.history, hide_index=True, width="stretch")
else:
    st.info("Aún no has enviado ninguna predicción.")
st.button("Vaciar historial", on_click=clear_history)
st.caption("Recargar el navegador o cerrar la conexión puede borrar la sesión. No es una base de datos.")
