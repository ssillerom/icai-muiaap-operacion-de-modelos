import streamlit as st
st.title("Contador con callback")
if "count" not in st.session_state:
    st.session_state.count = 0
def increment():
    st.session_state.count += 1
st.button("Sumar", on_click=increment)
st.metric("Cuenta", st.session_state.count)
