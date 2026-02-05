"""
Cliente HTTP para interactuar con la API FastAPI del chatbot
Centraliza todas las llamadas HTTP al backend
"""

import httpx
import logging
from typing import Optional, Dict, Any
from .config import config

logger = logging.getLogger(__name__)


class ChatbotAPIClient:
    """
    Cliente HTTP para la API del chatbot.
    Gestiona la comunicación con los endpoints del backend.
    """
    
    def __init__(self, backend_url: str = config.BACKEND_URL, timeout: int = config.API_TIMEOUT):
        """
        Inicializa el cliente
        
        Args:
            backend_url: URL base del backend (default: config.BACKEND_URL)
            timeout: Timeout en segundos (default: config.API_TIMEOUT)
        """
        self.backend_url = backend_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout, verify=False)
    
    def _build_url(self, endpoint: str) -> str:
        """
        Construye la URL completa para un endpoint
        
        Args:
            endpoint: Ruta del endpoint (ej: "/chat")
            
        Returns:
            URL completa (ej: "http://localhost:8000/chat")
        """
        return f"{self.backend_url}{endpoint}"
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Prueba la conexión con la API
        
        Returns:
            Diccionario con estado de conexión y detalles
        """
        try:
            response = self.client.get(self._build_url("/"), follow_redirects=True)
            response.raise_for_status()
            return {
                "connected": True,
                "status_code": response.status_code,
                "data": response.json()
            }
        except httpx.ConnectError:
            logger.error(f"No se puede conectar a {self.backend_url}")
            return {
                "connected": False,
                "error": f"No se puede conectar a {self.backend_url}",
                "status_code": None
            }
        except Exception as e:
            logger.error(f"Error en test_connection: {e}")
            return {
                "connected": False,
                "error": str(e),
                "status_code": None
            }
    
    def chat(self, query: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Envía una consulta al endpoint /chat
        
        Args:
            query: Pregunta del usuario
            session_id: ID de sesión (opcional)
            
        Returns:
            Respuesta del chatbot con juegos recomendados
        """
        try:
            payload = {
                "query": query,
                "session_id": session_id
            }
            
            response = self.client.post(self._build_url("/chat"), json=payload)
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json()
            }
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Error {e.response.status_code}: {e.response.text}")
            return {
                "success": False,
                "error": f"HTTP {e.response.status_code}: {e.response.reason_phrase}",
                "status_code": e.response.status_code
            }
        except httpx.TimeoutException:
            logger.error("Timeout en chat()")
            return {
                "success": False,
                "error": "La solicitud tardó demasiado. Intenta de nuevo.",
                "status_code": None
            }
        except Exception as e:
            logger.error(f"Error en chat(): {e}")
            return {
                "success": False,
                "error": str(e),
                "status_code": None
            }
    
    def get_chat_history(self, session_id: str) -> Dict[str, Any]:
        """
        Obtiene el historial de chat de una sesión
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            Historial de mensajes
        """
        try:
            response = self.client.get(self._build_url(f"/chat/history/{session_id}"))
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json()
            }
        except Exception as e:
            logger.error(f"Error en get_chat_history(): {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def reset_chat(self, session_id: str) -> Dict[str, Any]:
        """
        Resetea el historial de una sesión
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            Confirmación del reset
        """
        try:
            response = self.client.post(
                self._build_url("/chat/reset"),
                params={"session_id": session_id}
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json()
            }
        except Exception as e:
            logger.error(f"Error en reset_chat(): {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """
        Obtiene estadísticas de una sesión
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            Estadísticas de la sesión (creación, mensajes, etc)
        """
        try:
            response = self.client.get(self._build_url(f"/chat/stats/{session_id}"))
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json()
            }
        except Exception as e:
            logger.error(f"Error en get_session_stats(): {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_all_games(self, page: int = 1, page_size: int = 25) -> Dict[str, Any]:
        """
        Obtiene todos los juegos con paginación
        
        Args:
            page: Número de página (empieza en 1)
            page_size: Cantidad de juegos por página
            
        Returns:
            Diccionario con juegos paginados
        """
        try:
            response = self.client.get(
                self._build_url("/games/all"),
                params={"page": page, "page_size": page_size}
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json()
            }
        except Exception as e:
            logger.error(f"Error en get_all_games(): {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def close(self):
        """Cierra la conexión HTTP"""
        try:
            self.client.close()
            logger.info("Cliente HTTP cerrado")
        except Exception as e:
            logger.error(f"Error al cerrar cliente: {e}")


# Función singleton para obtener instancia del cliente
_client_instance: Optional[ChatbotAPIClient] = None


def get_api_client() -> ChatbotAPIClient:
    """
    Obtiene la instancia global del cliente API
    (Singleton pattern)
    
    Returns:
        Instancia del ChatbotAPIClient
    """
    global _client_instance
    if _client_instance is None:
        _client_instance = ChatbotAPIClient()
    return _client_instance
