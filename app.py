import streamlit as st
import streamlit.components.v1 as components
import os

# Configuración de página con fondo oscuro para que no haya contraste
st.set_page_config(
    page_title="SGC Dashboard Pro",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CSS PARA ELIMINAR BORDES Y PERMITIR SCROLL ---
st.markdown("""
    <style>
    /* Ocultar elementos de UI de Streamlit */
    [data-testid="stHeader"], footer, #MainMenu, .stAppDeployButton {display: none !important;}
    
    /* Reset de márgenes y padding para que tu HTML toque los bordes */
    .block-container {
        padding: 0px !important;
        max-width: 100% !important;
        margin: 0px !important;
    }
    
    .stApp {
        background-color: #0f172a; /* Mismo fondo que tu dashboard */
    }

    /* Quitar espacios en blanco adicionales */
    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
    }

    /* Estilo para el contenedor del iframe */
    iframe {
        border: none !important;
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
    
    # Limpiar links rotos
    full_html = full_html.replace('<link rel="stylesheet" href="style.css">', '')
    full_html = full_html.replace('<script src="script.js"></script>', '')

    return full_html

# Renderizar el dashboard
# Tip: He puesto height=4000 para asegurar que todo tu contenido quepa en un solo scroll natural de Streamlit
html_data = load_dashboard()
components.html(html_data, height=4000, scrolling=False)
