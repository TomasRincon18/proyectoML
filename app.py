import streamlit as st
import streamlit.components.v1 as components
import os

# Configuración de la página para que sea una "carcasa" invisible
st.set_page_config(
    page_title="SGC Dashboard Pro",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CSS RADICAL PARA ELIMINAR EL DOBLE SCROLL ---
st.markdown("""
    <style>
    /* 1. Eliminar todos los espacios y scrolls de Streamlit */
    html, body, [data-testid="stAppViewContainer"], .main, .block-container {
        margin: 0 !important;
        padding: 0 !important;
        height: 100vh !important;
        overflow: hidden !important; /* Mata el scroll de Streamlit */
    }

    /* 2. Forzar al iframe a ocupar toda la pantalla */
    iframe {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh !important;
        border: none !important;
    }

    /* 3. Ocultar elementos decorativos de Streamlit que quitan espacio */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stAppDeployButton {display:none;}
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

    # Inyección de dependencias (Self-contained)
    full_html = html_content.replace('</head>', f'<style>{css_content}</style></head>')
    full_html = full_html.replace('</body>', f'<script>{js_content}</script></body>')
    
    # Limpiar referencias antiguas
    full_html = full_html.replace('<link rel="stylesheet" href="style.css">', '')
    full_html = full_html.replace('<script src="script.js"></script>', '')

    return full_html

# Renderizar el dashboard
# Al usar position: fixed e iframe height 100vh en el estilo de arriba,
# el componente se expandirá para llenar la pantalla.
html_data = load_dashboard()
components.html(html_data, height=0) # El height de aquí se ignora por el CSS anterior
