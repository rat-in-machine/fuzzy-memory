"""
Configuración de la interfaz Streamlit
Define variables globales, URLs del backend y constantes de la aplicación
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class UIConfig:
    """
    Clase de configuración centralizada para la UI Streamlit
    """
    
    # Backend API
    BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    
    # Opciones de timeout (aumentado para LLM)
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", 60))  # 60 segundos para dar tiempo al LLM
    
    # Configuración de la sesión
    SESSION_ID_LENGTH = 8
    DEFAULT_SESSION_TIMEOUT_MINUTES = 60
    
    # Configuración de la interfaz
    PAGE_TITLE = "🎮 Videogames Recommender Chatbot"
    PAGE_ICON = "🎮"
    LAYOUT = "wide"
    INITIAL_SIDEBAR_STATE = "expanded"
    
    # Configuración de chat
    MAX_MESSAGES_DISPLAY = 50
    GAMES_DISPLAY_LIMIT = 5
    
    # Estilos y colores
    PRIMARY_COLOR = "#FF6B6B"
    BACKGROUND_COLOR = "#0E1117"
    SECONDARY_BG_COLOR = "#1B1B1B"
    TEXT_COLOR = "#FFFFFF"
    SUCCESS_COLOR = "#51CF66"
    WARNING_COLOR = "#FFA94D"
    ERROR_COLOR = "#FF8787"
    
    # Mensajes del sistema
    MESSAGES = {
        "welcome": "¡Bienvenido! 👋 Soy tu asistente de recomendación de videojuegos.\n\n"
                   "Puedo ayudarte de varias formas:\n"
                   "• 🎯 Buscar juegos por **género** (ej: 'Dame juegos indie')\n"
                   "• 🎮 Buscar juegos por **nombre** (ej: 'Baldur\'s Gate 3')\n"
                   "• 💰 Ver **precios** en retail y keyshops\n"
                   "• ⭐ Consultar puntuaciones Metacritic",
        
        "loading": "Pensando... 🤖",
        "error_api": "❌ Error al conectar con el servidor. Verifica que la API está ejecutándose en {url}",
        "error_response": "⚠️ Hubo un error procesando tu solicitud: {error}",
        "no_results": "No encontré resultados para tu consulta. Intenta ser más específico.",
        "session_created": "✅ Sesión creada: {session_id}",
        "session_reset": "🔄 Conversación reseteada",
        "connection_ok": "✅ API conectada",
        "connection_fail": "❌ Error de conexión",
    }


# Crear instancia global de configuración
config = UIConfig()
