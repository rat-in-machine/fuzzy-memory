"""
Componentes visuales reutilizables para la UI Streamlit
Incluye: tarjetas de juegos, renderizado de chat, etc
"""

import streamlit as st
from typing import List, Dict, Any
from .config import config


def render_game_card(game: Dict[str, Any]) -> None:
    """
    Renderiza una tarjeta de juego individual
    
    Args:
        game: Diccionario con datos del juego
    """
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Imagen del juego si está disponible
            if game.get("header_image"):
                try:
                    st.image(game["header_image"], width=500)
                except Exception:
                    st.info("📷 Sin imagen disponible")
            else:
                st.info("📷 Sin imagen disponible")
        
        with col2:
            # Información del juego
            st.subheader(game.get("name", "Juego desconocido"))
            
            # Géneros
            genres = game.get("genres", [])
            if genres:
                genres_str = ", ".join(genres)
                st.caption(f"🎯 **Géneros:** {genres_str}")
            
            # Precios (Retail y Keyshop)
            retail_price = game.get("current_price_retail", 0)
            keyshop_price = game.get("current_price_keyshop", 0)
            
            if retail_price == 0 and keyshop_price == 0:
                st.success("💚 **GRATIS** (Free-to-Play)")
            else:
                price_col1, price_col2 = st.columns(2)
                with price_col1:
                    if retail_price > 0:
                        st.info(f"🏪 **Retail:** €{retail_price:.2f}")
                    else:
                        st.caption("🏪 Retail: N/A")
                with price_col2:
                    if keyshop_price > 0:
                        st.success(f"🔑 **Keyshop:** €{keyshop_price:.2f}")
                    else:
                        st.caption("🔑 Keyshop: N/A")
            
            # Metacritic
            if game.get("metacritic"):
                st.metric("⭐ Metacritic", f"{game['metacritic']}/100")
            
            # Descripción con expander para textos largos
            description = game.get("description", "")
            if description:
                if len(description) > 200:
                    # Mostrar preview y botón "Mostrar más"
                    st.caption(f"📝 {description[:200]}...")
                    with st.expander("📖 Mostrar descripción completa"):
                        st.write(description)
                else:
                    # Mostrar descripción completa si es corta
                    st.caption(f"📝 {description}")
            
            # Enlace a GG.deals
            if game.get("ggdeals_url"):
                st.markdown(f"[🔗 Ver en GG.deals]({game['ggdeals_url']})", unsafe_allow_html=True)
        
        st.divider()


def render_games_section(games: List[Dict[str, Any]]) -> None:
    """
    Renderiza una sección con múltiples tarjetas de juegos
    
    Args:
        games: Lista de juegos a mostrar
    """
    if not games:
        st.info("📭 No hay juegos para mostrar")
        return
    
    st.subheader(f"🎮 Juegos Encontrados ({len(games)})")
    
    for game in games:
        render_game_card(game)


def render_pagination(current_page: int, total_pages: int, on_page_change) -> None:
    """
    Renderiza controles de paginación
    
    Args:
        current_page: Página actual (1-indexed)
        total_pages: Total de páginas disponibles
        on_page_change: Callback cuando se cambia de página
    """
    if total_pages <= 1:
        return
    
    st.divider()
    
    # Mostrar información de paginación
    col_info, col_nav = st.columns([1, 3])
    
    with col_info:
        st.caption(f"📄 Página {current_page} de {total_pages}")
    
    with col_nav:
        cols = st.columns(min(7, total_pages + 2))
        
        # Botón "Anterior"
        with cols[0]:
            if st.button("⬅️ Anterior", key="btn_prev", disabled=(current_page == 1)):
                on_page_change(current_page - 1)
        
        # Botones de páginas
        start_page = max(1, current_page - 2)
        end_page = min(total_pages, current_page + 2)
        
        col_idx = 1
        for page in range(start_page, end_page + 1):
            with cols[col_idx]:
                if page == current_page:
                    st.button(
                        f"**{page}**",
                        key=f"btn_page_{page}",
                        disabled=True,
                        type="primary"
                    )
                else:
                    if st.button(f"{page}", key=f"btn_page_{page}"):
                        on_page_change(page)
            col_idx += 1
        
        # Botón "Siguiente"
        with cols[-1]:
            if st.button("Siguiente ➡️", key="btn_next", disabled=(current_page == total_pages)):
                on_page_change(current_page + 1)


def render_chat_message(message: Dict[str, str], is_user: bool = True) -> None:
    """
    Renderiza un mensaje del chat
    
    Args:
        message: Diccionario con 'role' y 'content'
        is_user: True si es mensaje del usuario, False si es del asistente
    """
    if is_user:
        with st.chat_message("user", avatar="👤"):
            st.write(message.get("content", ""))
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.write(message.get("content", ""))


def render_session_info(session_data: Dict[str, Any]) -> None:
    """
    Renderiza información de la sesión
    
    Args:
        session_data: Diccionario con datos de la sesión
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Session ID", session_data.get("session_id", "N/A"))
    
    with col2:
        message_count = session_data.get("message_count", 0)
        st.metric("📊 Mensajes", message_count)
    
    with col3:
        created_at = session_data.get("created_at", "N/A")
        st.metric("📅 Creada", created_at[:10] if created_at else "N/A")


def render_error_message(error: str, error_type: str = "error") -> None:
    """
    Renderiza un mensaje de error
    
    Args:
        error: Texto del error
        error_type: "error", "warning" o "info"
    """
    if error_type == "error":
        st.error(error, icon="❌")
    elif error_type == "warning":
        st.warning(error, icon="⚠️")
    else:
        st.info(error, icon="ℹ️")


def render_loading_spinner(message: str = "Cargando...") -> None:
    """
    Renderiza un spinner de carga
    
    Args:
        message: Mensaje a mostrar durante la carga
    """
    with st.spinner(message):
        pass


def render_connection_status(connected: bool, backend_url: str) -> None:
    """
    Renderiza el estado de conexión a la API
    
    Args:
        connected: True si está conectado
        backend_url: URL del backend
    """
    if connected:
        st.success(f"✅ Conectado a {backend_url}", icon="✅")
    else:
        st.error(f"❌ Error de conexión con {backend_url}", icon="❌")


def render_sidebar_menu() -> str:
    """
    Renderiza el menú lateral con opciones
    
    Returns:
        Opción seleccionada
    """
    st.sidebar.title("⚙️ Opciones")
    
    with st.sidebar:
        # Información de la app
        st.markdown("""
        ## 🎮 Videogames Recommender
        
        Interfaz de prueba para el chatbot de recomendación de videojuegos.
        
        **Versión:** 0.1.0  
        **Estado:** Desarrollo educativo
        """)
        
        st.divider()
        
        # Configuración
        with st.expander("⚙️ Configuración"):
            backend_url = st.text_input(
                "URL del Backend",
                value=config.BACKEND_URL,
                help="URL donde está ejecutándose la API FastAPI"
            )
            
            if st.button("🔄 Actualizar URL"):
                st.info("URL actualizada manualmente en config.py si es necesario")
        
        st.divider()
        
        # Información educativa
        with st.expander("📚 Información"):
            st.markdown("""
            ### Cómo usar
            1. **Genera o usa una sesión** en el panel principal
            2. **Escribe tu consulta** (género, nombre, precio)
            3. **Envía** y verás recomendaciones
            4. **Resetea** cuando quieras empezar nueva conversación
            
            ### Ejemplos de búsqueda
            - "Dame juegos indie"
            - "Quiero juegos estrategia"
            - "¿Hay juegos gratis?"
            - "Busca Baldur's Gate"
            """)
        
        st.divider()
        
        # Footer
        st.caption("🚀 Desarrollado como herramienta educativa para el Hackathon")


def render_api_docs_link() -> None:
    """
    Renderiza un link a los docs de la API
    """
    st.info(
        "📖 **Documentación de la API:** "
        f"[Swagger UI]({config.BACKEND_URL}/docs)",
        icon="📚"
    )
