"""
Gestor de sesiones conversacionales para el chatbot
Mantiene memoria de múltiples conversaciones simultáneas
"""

from typing import Dict, Optional
from datetime import datetime, timedelta
import logging
import uuid

logger = logging.getLogger(__name__)


class SessionManager:
    """
    Gestiona múltiples sesiones de chat independientes con su propia memoria
    """
    
    def __init__(self, session_timeout_minutes: int = 60):
        """
        Args:
            session_timeout_minutes: Minutos antes de expirar una sesión inactiva
        """
        self.sessions: Dict[str, Dict] = {}
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
    
    def create_session(self, session_id: Optional[str] = None) -> str:
        """
        Crea una nueva sesión
        
        Args:
            session_id: ID personalizado (opcional). Si no se proporciona, se genera uno
            
        Returns:
            ID de la sesión creada
        """
        if session_id is None:
            session_id = str(uuid.uuid4())[:8]
        
        self.sessions[session_id] = {
            "created_at": datetime.now(),
            "last_activity": datetime.now(),
            "messages": [],  # Historial de mensajes
            "metadata": {}
        }
        
        logger.info(f"Sesión creada: {session_id}")
        return session_id
    
    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
    ) -> None:
        """
        Añade un mensaje al historial de la sesión
        
        Args:
            session_id: ID de la sesión
            role: "user" o "assistant"
            content: Contenido del mensaje
        """
        if session_id not in self.sessions:
            raise ValueError(f"Sesión no encontrada: {session_id}")
        
        self.sessions[session_id]["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        self.sessions[session_id]["last_activity"] = datetime.now()
        logger.debug(f"Mensaje añadido a sesión {session_id}: {role}")
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Obtiene información de una sesión
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            Datos de la sesión o None si no existe
        """
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Verificar si expiró
        if datetime.now() - session["last_activity"] > self.session_timeout:
            del self.sessions[session_id]
            logger.info(f"Sesión expirada: {session_id}")
            return None
        
        return session
    
    def get_chat_history(self, session_id: str) -> list:
        """
        Obtiene el historial de mensajes de una sesión
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            Lista de mensajes [{"role": "...", "content": "..."}, ...]
        """
        session = self.get_session(session_id)
        if session is None:
            return []
        
        return session["messages"]
    
    def clear_session(self, session_id: str) -> None:
        """
        Limpia el historial de una sesión (pero mantiene la sesión activa)
        
        Args:
            session_id: ID de la sesión
        """
        if session_id not in self.sessions:
            raise ValueError(f"Sesión no encontrada: {session_id}")
        
        self.sessions[session_id]["messages"] = []
        self.sessions[session_id]["last_activity"] = datetime.now()
        
        logger.info(f"Sesión limpiada: {session_id}")
    
    def delete_session(self, session_id: str) -> None:
        """
        Elimina una sesión completamente
        
        Args:
            session_id: ID de la sesión
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Sesión eliminada: {session_id}")
    
    def cleanup_expired_sessions(self) -> int:
        """
        Limpia todas las sesiones expiradas
        
        Returns:
            Número de sesiones eliminadas
        """
        expired = []
        current_time = datetime.now()
        
        for session_id, session in self.sessions.items():
            if current_time - session["last_activity"] > self.session_timeout:
                expired.append(session_id)
        
        for session_id in expired:
            del self.sessions[session_id]
        
        if expired:
            logger.info(f"Limpiadas {len(expired)} sesiones expiradas")
        
        return len(expired)
    
    def get_session_stats(self, session_id: str) -> Optional[Dict]:
        """
        Obtiene estadísticas de una sesión
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            Dict con estadísticas o None si no existe
        """
        session = self.get_session(session_id)
        if session is None:
            return None
        
        return {
            "session_id": session_id,
            "created_at": session["created_at"].isoformat(),
            "last_activity": session["last_activity"].isoformat(),
            "message_count": len(session["messages"]),
            "user_messages": len([m for m in session["messages"] if m["role"] == "user"]),
            "assistant_messages": len([m for m in session["messages"] if m["role"] == "assistant"])
        }
