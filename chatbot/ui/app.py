"""
Aplicación principal Streamlit - Interfaz de chat para el chatbot de videojuegos
Proporciona una interfaz conversacional para probar el backend RAG
"""

import streamlit as st
import logging
import uuid
from datetime import datetime
from typing import Optional
import sys
from pathlib import Path

# Agregar el directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ui.config import config
from ui.api_client import get_api_client
from ui.components import (
    render_game_card,
    render_games_section,
    render_chat_message,
    render_session_info,
    render_error_message,
    render_connection_status,
    render_sidebar_menu,
    render_api_docs_link,
    render_pagination,
)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de la página
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state=config.INITIAL_SIDEBAR_STATE
)

# Inicializar estado if session_id no existe
if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_response_empty" not in st.session_state:
    st.session_state.last_response_empty = False

if "api_client" not in st.session_state:
    st.session_state.api_client = get_api_client()

if "api_connected" not in st.session_state:
    # Hacer test de conexión
    api_client = st.session_state.api_client
    test_result = api_client.test_connection()
    st.session_state.api_connected = test_result["connected"]
    st.session_state.api_info = test_result

# Estados para el catálogo paginado
if "catalog_mode" not in st.session_state:
    st.session_state.catalog_mode = False

if "catalog_games" not in st.session_state:
    st.session_state.catalog_games = []

if "catalog_page" not in st.session_state:
    st.session_state.catalog_page = 1

if "catalog_total" not in st.session_state:
    st.session_state.catalog_total = 0

if "catalog_total_pages" not in st.session_state:
    st.session_state.catalog_total_pages = 0


def initialize_session() -> str:
    """
    Inicializa o recupera una sesión
    
    Returns:
        ID de sesión (nuevo o existente)
    """
    if st.session_state.session_id is None:
        session_id = str(uuid.uuid4())[:config.SESSION_ID_LENGTH]
        st.session_state.session_id = session_id
        logger.info(f"Nueva sesión creada: {session_id}")
        return session_id
    return st.session_state.session_id


def get_or_create_session() -> str:
    """
    Obtiene o crea la sesión del usuario
    
    Returns:
        ID de sesión
    """
    return initialize_session()


def send_message(query: str) -> None:
    """
    Envía un mensaje al chatbot y obtiene respuesta
    
    Args:
        query: Pregunta del usuario
    """
    if not query.strip():
        st.warning("⚠️ Por favor escribe una consulta", icon="⚠️")
        return
    
    if not st.session_state.api_connected:
        st.error(
            f"❌ No hay conexión con la API en {config.BACKEND_URL}",
            icon="❌"
        )
        return
    
    # Detectar consulta de "todos los juegos"
    query_lower = query.lower()
    all_games_keywords = [
        "todos los juegos",
        "todos",
        "catalogo completo",
        "catalogo",
        "muestra todos",
        "muestrame todos",
        "listado completo",
        "ver todos"
    ]
    
    if any(keyword in query_lower for keyword in all_games_keywords):
        # Activar modo catálogo
        st.session_state.catalog_mode = True
        st.session_state.catalog_page = 1
        st.session_state.messages.append({
            "role": "user",
            "content": query,
            "timestamp": datetime.now().isoformat()
        })
        st.session_state.messages.append({
            "role": "assistant",
            "content": "📚 Mostrando catálogo completo de juegos (25 por página)",
            "timestamp": datetime.now().isoformat()
        })
        load_all_games(page=1)
        st.rerun()
        return
    
    # Flujo normal de chat
    api_client = st.session_state.api_client
    session_id = st.session_state.session_id
    
    # Mostrar spinner mientras se procesa
    with st.spinner(config.MESSAGES["loading"]):
        # Llamar a la API
        response = api_client.chat(query, session_id)
    
    if response["success"]:
        data = response["data"]
        
        # Actualizar session_id (por si se creó nueva)
        if "session_id" in data:
            st.session_state.session_id = data["session_id"]
        
        # Guardar en historial local
        st.session_state.messages.append({
            "role": "user",
            "content": query,
            "timestamp": datetime.now().isoformat()
        })
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": data.get("response", ""),
            "timestamp": datetime.now().isoformat()
        })
        
        # Guardar juegos recuperados para mostrar
        retrieved_games = data.get("retrieved_games", [])
        st.session_state.last_games = retrieved_games
        st.session_state.last_response_empty = len(retrieved_games) == 0
        st.session_state.last_message_count = data.get("message_count", 0)
        st.session_state.catalog_mode = False  # Desactivar modo catálogo
        
        # Rerun para actualizar UI
        st.rerun()
    else:
        error_msg = response.get("error", "Error desconocido")
        st.error(
            f"{config.MESSAGES['error_response'].format(error=error_msg)}",
            icon="❌"
        )


def load_all_games(page: int = 1) -> None:
    """
    Carga todos los juegos con paginación
    
    Args:
        page: Número de página a cargar
    """
    api_client = st.session_state.api_client
    
    with st.spinner(f"Cargando página {page}..."):
        result = api_client.get_all_games(page=page, page_size=25)
    
    if result["success"]:
        data = result["data"]
        st.session_state.catalog_games = data["games"]
        st.session_state.catalog_total = data["total"]
        st.session_state.catalog_page = data["page"]
        st.session_state.catalog_total_pages = data["total_pages"]
    else:
        st.error(f"Error al cargar juegos: {result.get('error')}", icon="❌")
        st.session_state.catalog_mode = False


def reset_conversation() -> None:
    """
    Resetea la conversación actual
    """
    api_client = st.session_state.api_client
    session_id = st.session_state.session_id
    
    with st.spinner("Reseteando conversación..."):
        result = api_client.reset_chat(session_id)
    
    if result["success"]:
        st.session_state.messages = []
        st.session_state.last_games = []
        st.session_state.last_response_empty = False
        st.success(config.MESSAGES["session_reset"], icon="✅")
        st.rerun()
    else:
        st.error(f"Error al resetear: {result.get('error')}", icon="❌")


def get_session_stats() -> None:
    """
    Obtiene y muestra estadísticas de la sesión
    """
    api_client = st.session_state.api_client
    session_id = st.session_state.session_id
    
    with st.spinner("Cargando estadísticas..."):
        result = api_client.get_session_stats(session_id)
    
    if result["success"]:
        st.session_state.session_stats = result["data"]
    else:
        st.warning(f"No se pudieron cargar las estadísticas: {result.get('error')}")


def main():
    """
    Función principal de la aplicación Streamlit
    """
    # Renderizar sidebar
    render_sidebar_menu()
    
    # Título principal
    st.title(config.PAGE_TITLE)
    st.markdown("""
    Interfaz de prueba conversacional para el **chatbot de recomendación de videojuegos**.
    
    Aquí puedes probar la búsqueda inteligente, ver recomendaciones y explorar información detallada de juegos.
    """)
    
    st.divider()
    
    # ===== SECCIÓN 1: ESTADO Y SESIÓN =====
    
    # Test de API
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        render_connection_status(st.session_state.api_connected, config.BACKEND_URL)
    
    with col2:
        if st.button("🔄 Reconectar API", key="btn_reconnect"):
            test_result = st.session_state.api_client.test_connection()
            st.session_state.api_connected = test_result["connected"]
            st.rerun()
    
    with col3:
        st.markdown(f"[📖 Docs API]({config.BACKEND_URL}/docs)", help="Ver documentación de la API")
    
    st.divider()
    
    # ===== SECCIÓN 2: GESTIÓN DE SESIÓN =====
    
    st.subheader("👤 Gestión de Sesión")
    
    col_sess1, col_sess2, col_sess3 = st.columns([2, 1, 1])
    
    with col_sess1:
        # Obtener o mostrar session_id
        if st.session_state.session_id is None:
            session_id = get_or_create_session()
        else:
            session_id = st.session_state.session_id
        
        st.code(session_id, language="plaintext")
    
    with col_sess2:
        if st.button("📊 Estadísticas", key="btn_stats"):
            get_session_stats()
            if "session_stats" in st.session_state:
                stats = st.session_state.session_stats
                st.json(stats)
    
    with col_sess3:
        if st.button("🔄 Resetear Chat", key="btn_reset"):
            reset_conversation()
    
    st.divider()
    
    # ===== SECCIÓN 3: HISTORIAL DE CHAT =====
    
    st.subheader("💬 Conversación")
    
    # Mostrar mensajes del historial
    if st.session_state.messages:
        chat_container = st.container(height=350, border=True)
        
        with chat_container:
            for i, message in enumerate(st.session_state.messages):
                render_chat_message(message, is_user=(message["role"] == "user"))
    else:
        with st.container(height=350, border=True):
            st.info(config.MESSAGES["welcome"], icon="👋")
    
    st.divider()
    
    # ===== SECCIÓN 4: INPUT DE USUARIO =====
    
    st.subheader("🎯 Tu Consulta")
    
    # Input de texto con altura adaptativa
    query = st.text_area(
        "Escribe tu pregunta sobre videojuegos",
        placeholder="Ej: Dame juegos indie... o ¿Qué tal Baldur's Gate 3?",
        height=75,
        max_chars=500,
        key="chat_input",
        help="Escribe tu consulta (máximo 500 caracteres)"
    )
    
    # Función callback para limpiar input
    def clear_input():
        """Limpia el campo de input de chat"""
        st.session_state.chat_input = ""
    
    # Botón enviar
    col_send1, col_send2 = st.columns([3, 1])
    
    with col_send1:
        if st.button("📤 Enviar Consulta", key="btn_send", type="primary"):
            if st.session_state.api_connected:
                send_message(query)
            else:
                st.error("No hay conexión con la API. Reconecta primero.", icon="❌")
    
    with col_send2:
        st.button(
            "🧹 Limpiar",
            key="btn_clear",
            on_click=clear_input,
            help="Limpia el campo de entrada"
        )
    
    st.divider()
    
    # ===== SECCIÓN 5: JUEGOS RECOMENDADOS / CATÁLOGO =====
    
    # Si estamos en modo catálogo, mostrar juegos paginados
    if st.session_state.catalog_mode:
        st.subheader(f"📚 Catálogo Completo ({st.session_state.catalog_total} juegos)")
        
        if st.session_state.catalog_games:
            # Renderizar juegos del catálogo
            for game in st.session_state.catalog_games:
                render_game_card(game)
            
            # Renderizar controles de paginación
            def change_page(new_page):
                load_all_games(page=new_page)
                st.rerun()
            
            render_pagination(
                current_page=st.session_state.catalog_page,
                total_pages=st.session_state.catalog_total_pages,
                on_page_change=change_page
            )
            
            # Botón para salir del modo catálogo
            if st.button("❌ Cerrar catálogo", key="btn_close_catalog"):
                st.session_state.catalog_mode = False
                st.rerun()
        else:
            st.info("No hay juegos en el catálogo")
    
    # Modo normal: mostrar juegos de la última búsqueda
    elif "last_games" in st.session_state and st.session_state.last_games:
        st.subheader("🎮 Juegos Recomendados")
        render_games_section(st.session_state.last_games)
    elif "last_response_empty" in st.session_state and st.session_state.last_response_empty:
        st.warning(
            "🔄 **Estamos actualizando nuestro catálogo... disculpa las molestias**\n\n"
            "No encontramos resultados para tu consulta. Nuestro catálogo está en constante actualización. "
            "Intenta buscar por otro título o género.",
            icon="⚠️"
        )
    
    st.divider()
    
    # ===== FOOTER =====
    
    st.markdown("""
    ---
    **ℹ️ Información de la Aplicación**
    
    - **Backend:** FastAPI + MongoDB
    - **Frontend:** Streamlit
    - **Purpose:** Interfaz educativa para pruebas y demos del chatbot RAG
    - **Version:** 0.1.0
    - **Status:** Desarrollo
    """)


if __name__ == "__main__":
    main()
