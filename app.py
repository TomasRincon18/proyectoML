import streamlit as st
import streamlit.components.v1 as components
import os

# Configuración de la página ultra-limpia
st.set_page_config(
    page_title="SGC Dashboard Pro",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CSS FULLSCREEN (PARA ELIMINAR EL "STREAMLIT LOOK") ---
st.markdown("""
    <style>
    /* Eliminar padding superior y laterales del contenedor principal */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    /* Ocultar header, footer y menú de Streamlit */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stAppDeployButton {display:none;}
    
    /* Forzar el iframe a no tener bordes ni márgenes */
    iframe {
        border: none !important;
        margin: 0 !important;
        padding: 0 !important;
        display: block;
    }
    
    /* Eliminar el espacio en blanco arriba (gap) */
    .stApp {
        margin: 0 !important;
        padding: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

def load_dashboard():
    # Rutas de los archivos
    base_path = "dashboard_pro"
    html_path = os.path.join(base_path, "index.html")
    css_path = os.path.join(base_path, "style.css")
    js_path = os.path.join(base_path, "script.js")

    # Leer archivos con encoding utf-8
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()
    with open(js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    # Inyecciones para que el sitio sea autónomo
    full_html = html_content.replace('</head>', f'<style>{css_content}</style></head>')
    full_html = full_html.replace('</body>', f'<script>{js_content}</script></body>')
    
    # Limpiar links rotos que ya inyectamos
    full_html = full_html.replace('<link rel="stylesheet" href="style.css">', '')
    full_html = full_html.replace('<script src="script.js"></script>', '')

    return full_html

# Renderizar el dashboard
# Usamos un height suficientemente grande para evitar doble scroll bar o ajustado a tu diseño
html_data = load_dashboard()
components.html(html_data, height=1000, scrolling=True)
