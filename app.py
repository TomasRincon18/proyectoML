import streamlit as st
import streamlit.components.v1 as components
import os

# Configuración ultra-completa
st.set_page_config(
    page_title="SGC Dashboard Pro",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CSS DEFINITIVO: STREAMLIT COMO UN VISOR 1:1 ---
st.markdown("""
    <style>
    /* 1. Reset total de la interfaz de Streamlit */
    [data-testid="stHeader"], footer, #MainMenu, .stAppDeployButton {display: none !important;}
    
    /* 2. Eliminar márgenes y scroll del contenedor padre (Streamlit) */
    .stApp {
        margin: 0 !important;
        padding: 0 !important;
        height: 100vh !important;
        width: 100vw !important;
        overflow: hidden !important; /* Mata el scroll externo */
        background-color: #0f172a;
    }

    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        height: 100vh !important;
        width: 100vw !important;
    }

    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
    }

    /* 3. Forzar el IFRAME a ser el VIEWPORT real */
    /* Usamos !important para anular el inline style de Streamlit */
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

def load_dashboard():
    base_path = "dashboard_pro"
    with open(os.path.join(base_path, "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()
    with open(os.path.join(base_path, "style.css"), "r", encoding="utf-8") as f:
        css_content = f.read()
    with open(os.path.join(base_path, "script.js"), "r", encoding="utf-8") as f:
        js_content = f.read()

    # Inyección de estilos y scripts
    full_html = html_content.replace('</head>', f'<style>{css_content}</style></head>')
    full_html = full_html.replace('</body>', f'<script>{js_content}</script></body>')
    
    # Limpiar referencias antiguas del dashboard
    full_html = full_html.replace('<link rel="stylesheet" href="style.css">', '')
    full_html = full_html.replace('<script src="script.js"></script>', '')

    return full_html

# Renderizar
# El 'height' aquí es solo un fallback, el CSS lo forzará a 100vh
# scrolling=True permite que tu página gestione el scroll dentro del iframe
html_data = load_dashboard()
components.html(html_data, scrolling=True, height=1)
