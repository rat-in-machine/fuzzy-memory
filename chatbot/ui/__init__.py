"""
Paquete UI - Interfaz Streamlit para el chatbot
"""

from .api_client import ChatbotAPIClient, get_api_client
from .config import config, UIConfig
from .components import (
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

__version__ = "0.1.0"
__author__ = "AI Engineering Team"

__all__ = [
    "ChatbotAPIClient",
    "get_api_client",
    "config",
    "UIConfig",
    "render_game_card",
    "render_games_section",
    "render_chat_message",
    "render_session_info",
    "render_error_message",
    "render_connection_status",
    "render_sidebar_menu",
    "render_api_docs_link",
    "render_pagination",
]
