"""
Cliente LLM con soporte para streaming de respuestas.

Integración con endpoint de CodingBuddy (OpenAI-compatible) que incluye:
- Autenticación mediante X-API-KEY
- Streaming de respuestas en tiempo real
- Decodificación UTF-8 incremental
- Manejo de errores y reintentos
"""

import json
import requests
import codecs
import logging
from typing import Generator, Optional, AsyncGenerator
from uuid import uuid4
from config.settings import settings

logger = logging.getLogger(__name__)


class LLMStreamingClient:
    """
    Cliente para interactuar con LLM vía CodingBuddy con streaming.
    
    Atributos:
        api_endpoint (str): URL del endpoint LLM
        api_key (str): Clave de autenticación X-API-KEY
        model (str): Nombre del modelo (ej: gpt-4o, gpt-4-turbo)
        user_email (str): Email para identificar la request
        timeout (int): Timeout para requests (segundos)
    """
    
    def __init__(
        self,
        api_endpoint: str = None,
        api_key: str = None,
        model: str = "gpt-4o",
        user_email: str = None,
        timeout: int = 60
    ):
        """Inicializa el cliente LLM."""
        self.api_endpoint = api_endpoint or settings.llm_api_endpoint
        self.api_key = api_key or settings.llm_api_key
        self.model = model or settings.llm_model
        self.user_email = user_email or settings.llm_user_email  # Usar email de settings por defecto
        self.timeout = timeout
        self.session_uuid = str(uuid4())
        
        logger.info(f"LLMStreamingClient inicializado - Modelo: {self.model}, Usuario: {self.user_email}")
    
    def _build_request_body(
        self,
        message_content: str,
        temperature: float = 0.7,
        language: str = "es",
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Construye el body JSON para la request al LLM.
        
        Formato compatible con CodingBuddy OpenAI endpoint.
        
        Args:
            message_content: Mensaje del usuario
            temperature: Parámetro de creatividad (0-1)
            language: Idioma de respuesta (ej: es, en)
            system_prompt: Prompt del sistema (role: system)
        
        Returns:
            String JSON formateado para la API
        """
        body = {
            "model": self.model,
            "uuid": self.session_uuid,
            "message": {
                "role": "user",
                "content": message_content
            },
            "temperature": temperature,
            "language": language,
            "user": self.user_email
        }
        
        return json.dumps(body, ensure_ascii=False)
    
    def stream(
        self,
        message: str,
        temperature: float = 0.7,
        language: str = "es",
        system_prompt: Optional[str] = None,
        max_retries: int = 3
    ) -> Generator[str, None, None]:
        """
        Realiza streaming de respuesta del LLM.
        
        Yields:
            Chunks de texto de la respuesta (decodificados UTF-8)
        
        Raises:
            requests.exceptions.RequestException: Error en la solicitud
            ConnectionError: Fallo de conexión después de reintentos
        
        Ejemplo:
            async for chunk in client.stream("¿Qué es RPG?"):
                print(chunk, end="", flush=True)
        """
        headers = {
            "X-API-KEY": self.api_key
        }
        
        body_str = self._build_request_body(
            message_content=message,
            temperature=temperature,
            language=language,
            system_prompt=system_prompt
        )
        
        data = {"body_str": body_str}
        
        logger.debug(f"Enviando request al LLM: {self.api_endpoint}")
        logger.debug(f"Modelo: {self.model}, Temperature: {temperature}")
        
        attempt = 0
        last_error = None
        
        while attempt < max_retries:
            try:
                with requests.post(
                    self.api_endpoint,
                    headers=headers,
                    data=data,  # Usar data en lugar de json (igual que ejemplo)
                    stream=True,
                    timeout=self.timeout
                ) as response:
                    response.raise_for_status()
                    
                    logger.info(f"Streaming iniciado (Status: {response.status_code})")
                    
                    # Decodificador UTF-8 incremental
                    decoder = codecs.getincrementaldecoder("utf-8")()
                    
                    # Iterar sobre chunks
                    for chunk in response.iter_content(chunk_size=64):
                        if chunk:
                            # Decodificar incrementalmente
                            text = decoder.decode(chunk, final=False)
                            if text:
                                yield text
                    
                    # Procesar resto de bytes pendientes
                    final_text = decoder.decode(b"", final=True)
                    if final_text:
                        yield final_text
                    
                    logger.info("Streaming completado exitosamente")
                    return
                    
            except requests.exceptions.Timeout:
                attempt += 1
                last_error = f"Timeout después de {self.timeout}s"
                logger.warning(f"Timeout - Intento {attempt}/{max_retries}")
                if attempt < max_retries:
                    yield f"\n[⏱️ Timeout - Reintentando ({attempt}/{max_retries})]\n"
                    
            except requests.exceptions.ConnectionError as e:
                attempt += 1
                last_error = str(e)
                logger.error(f"Error de conexión - Intento {attempt}/{max_retries}: {e}")
                if attempt < max_retries:
                    yield f"\n[🔗 Error de conexión - Reintentando ({attempt}/{max_retries})]\n"
                    
            except requests.exceptions.RequestException as e:
                attempt += 1
                last_error = str(e)
                logger.error(f"Error en request - Intento {attempt}/{max_retries}: {e}")
                if attempt < max_retries:
                    yield f"\n[⚠️ Error en request - Reintentando ({attempt}/{max_retries})]\n"
        
        # Falló después de reintentos
        error_msg = f"No se pudo conectar al LLM después de {max_retries} intentos. Último error: {last_error}"
        logger.error(error_msg)
        yield f"\n[❌ {error_msg}]\n"
    
    async def stream_async(
        self,
        message: str,
        temperature: float = 0.7,
        language: str = "es",
        system_prompt: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Versión async de stream() para integración con FastAPI.
        
        Yields:
            Chunks de texto de la respuesta
        
        Nota: Envuelve el generador sincrónico para compatible con async/await
        """
        # Por ahora, delegamos al método sincrónico
        # En producción, considerar usar httpx para I/O async
        for chunk in self.stream(
            message=message,
            temperature=temperature,
            language=language,
            system_prompt=system_prompt
        ):
            yield chunk
    
    def get_response(
        self,
        message: str,
        temperature: float = 0.7,
        language: str = "es",
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Obtiene respuesta completa del LLM (no streaming).
        
        Returns:
            Respuesta completa del LLM
        
        Uso para fallbacks o endpoints que no requieren streaming.
        """
        full_response = ""
        for chunk in self.stream(
            message=message,
            temperature=temperature,
            language=language,
            system_prompt=system_prompt
        ):
            full_response += chunk
        return full_response
