import streamlit as st
from modelo import predict_toy

st.set_page_config(page_title="Churn con memoria", layout="centered")
st.title("Churn con memoria")
st.caption("Regla de juguete. No usar para tomar decisiones sobre clientes.")

# A: iniciar una sola vez, no en cada rerun.
if "history" not in st.session_state:
    pass  # TODO A: asignar [] a st.session_state.history

def submit_prediction():
    # Leer los valores nuevos desde las keys, no mediante args del callback.
    inputs = {name: st.session_state[name] for name in
              ("tenure_months", "monthly_spend_eur", "contract", "support_calls")}
    result = predict_toy(**inputs)
    # B: una fila por submit. No predecir en cada rerun.
    pass  # TODO B: añadir {**inputs, **result} a history

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

# C: mostrar un contador y, si hay filas, st.dataframe.
# Pista: history = st.session_state.get("history", [])
st.info("TODO C: dibuja aquí el historial y su contador.")
st.button("Vaciar historial", on_click=clear_history)
st.caption("Recargar el navegador o cerrar la conexión puede borrar la sesión. No es una base de datos.")
