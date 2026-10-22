# Frontend del chatbot (YA HECHO: los alumnos no lo modifican).
# Arrancar:  streamlit run frontend/app.py      (con la API en marcha en el puerto 8000)
import os

import httpx
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000")
LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
AMARILLO = "#FAB900"
NEGRO = "#1D1D1B"

EJEMPLOS = [
    "Calcula el riesgo: edad 30, ingresos 2500, importe 12000, plazo 36, antigüedad 5, impagos 0",
    "Edad 25, ingresos 1200, importe 20000, plazo 24, antigüedad 1, impagos 2",
    "Y si tuviera 3 impagos previos?",
    "Solo sé que tiene 40 años y gana 1800 euros",
]

st.set_page_config(page_title="Asistente de riesgo | Comillas ICAI", page_icon="💬", layout="centered")

st.markdown(
    f"""
    <style>
    .stApp {{ background: #F6F5F1; }}
    .cabecera {{
        background: white; border-radius: 16px; padding: 14px 22px; margin-bottom: 18px;
        border-bottom: 6px solid {AMARILLO}; box-shadow: 0 2px 10px rgba(0,0,0,.08);
    }}
    .cabecera h1 {{ font-size: 1.6rem; margin: 0; color: {NEGRO}; }}
    .cabecera p {{ margin: 2px 0 0 0; color: #666; font-size: .95rem; }}
    [data-testid="stChatMessage"] {{
        background: white; border-radius: 14px; padding: 12px 16px; margin-bottom: 8px;
        box-shadow: 0 1px 4px rgba(0,0,0,.06);
    }}
    [data-testid="stSidebar"] {{ background: {NEGRO}; }}
    [data-testid="stSidebar"] * {{ color: #f2f2f2; }}
    [data-testid="stSidebar"] .stButton button {{
        background: transparent; border: 1px solid {AMARILLO}; color: {AMARILLO};
        text-align: left; border-radius: 10px; font-size: .85rem;
    }}
    [data-testid="stSidebar"] .stButton button:hover {{ background: {AMARILLO}; color: {NEGRO}; }}
    </style>
    """,
    unsafe_allow_html=True,
)

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    st.session_state.pendiente = None

# ---- Barra lateral ----
with st.sidebar:
    st.markdown("### 💡 Prueba con...")
    for i, ejemplo in enumerate(EJEMPLOS):
        if st.button(ejemplo, key="ej" + str(i), use_container_width=True):
            st.session_state.pendiente = ejemplo
    st.markdown("---")
    if st.button("🗑️ Nueva conversación", use_container_width=True):
        st.session_state.mensajes = []
        st.session_state.pendiente = None
        st.rerun()
    st.caption("API: " + API_URL)
    try:
        estado = httpx.get(API_URL + "/health", timeout=2).json().get("status")
        st.success("Backend conectado" if estado == "ok" else "Backend responde raro")
    except Exception:
        st.error("Backend no disponible")

# ---- Cabecera ----
columna_logo, columna_texto = st.columns([1, 2.4])
with columna_logo:
    st.image(LOGO, use_container_width=True)
with columna_texto:
    st.markdown(
        f"""<div class="cabecera"><h1>💬 Asistente de riesgo</h1>
        <p>Operación de Modelos · MUIAAP · Práctica 8</p></div>""",
        unsafe_allow_html=True,
    )


def pintar_herramienta(herramienta):
    resultado = herramienta["resultado"]
    with st.expander("🔧 Herramienta llamada: " + herramienta["nombre"]):
        st.caption("Argumentos que envió el LLM")
        st.json(herramienta["argumentos"])
        st.caption("Resultado de tu API")
        if resultado.get("ok"):
            c1, c2 = st.columns(2)
            c1.metric("Prob. de impago", "{:.1f}%".format(resultado["probabilidad_impago"] * 100))
            c2.metric("Decisión", resultado["decision"].upper())
        else:
            st.error(resultado.get("error", "error desconocido"))


# ---- Historial ----
if len(st.session_state.mensajes) == 0:
    st.info("👋 Cuéntame los datos de una solicitud de préstamo (edad, ingresos, importe, plazo, "
            "antigüedad laboral e impagos previos) y calcularé su riesgo de impago.")

for m in st.session_state.mensajes:
    with st.chat_message(m["role"], avatar="🧑‍💼" if m["role"] == "user" else "🤖"):
        st.markdown(m["content"])
        if m.get("herramienta"):
            pintar_herramienta(m["herramienta"])

# ---- Entrada ----
texto = st.chat_input("Escribe tu consulta...")
if st.session_state.pendiente:
    texto = st.session_state.pendiente
    st.session_state.pendiente = None

if texto:
    st.session_state.mensajes.append({"role": "user", "content": texto})
    with st.chat_message("user", avatar="🧑‍💼"):
        st.markdown(texto)
    cuerpo = {"mensajes": []}
    for m in st.session_state.mensajes:
        cuerpo["mensajes"].append({"role": m["role"], "content": m["content"]})
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Pensando..."):
            try:
                respuesta = httpx.post(API_URL + "/chat", json=cuerpo, timeout=120)
                respuesta.raise_for_status()
                datos = respuesta.json()
                st.markdown(datos["respuesta"])
                if datos.get("herramienta"):
                    pintar_herramienta(datos["herramienta"])
                st.session_state.mensajes.append(
                    {"role": "assistant", "content": datos["respuesta"], "herramienta": datos.get("herramienta")}
                )
            except Exception as error:
                st.error("Error al llamar al backend: " + str(error))
                st.session_state.mensajes.pop()
