import streamlit as st
import streamlit.components.v1 as components
import os

# Configuración de la página
st.set_page_config(page_title="SGC Dashboard Pro", layout="wide", initial_sidebar_state="collapsed")

def load_dashboard():
    # Rutas de los archivos
    base_path = "dashboard_pro"
    html_path = os.path.join(base_path, "index.html")
    css_path = os.path.join(base_path, "style.css")
    js_path = os.path.join(base_path, "script.js")

    # Leer archivos
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()
        
    with open(js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    # Inyectar CSS y JS en el HTML para que sea autoportante en el iframe de Streamlit
    # Insertar CSS antes de cerrar el head
    full_html = html_content.replace('</head>', f'<style>{css_content}</style></head>')
    # Insertar JS al final del body
    full_html = full_html.replace('</body>', f'<script>{js_content}</script></body>')
    # Limpiar referencias externas que ya inyectamos
    full_html = full_html.replace('<link rel="stylesheet" href="style.css">', '')
    full_html = full_html.replace('<script src="script.js"></script>', '')

    return full_html

# Renderizar el dashboard a pantalla completa
html_data = load_dashboard()
components.html(html_data, height=2000, scrolling=True)

# Estilos para ocultar el menú de Streamlit y que parezca una web pura
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { margin-top: -80px; }
    iframe { border-radius: 0px !important; }
    </style>
""", unsafe_allow_html=True)
