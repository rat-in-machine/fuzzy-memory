from pydantic_settings import BaseSettings
from pydantic import Field, AliasChoices
from typing import Optional


class Settings(BaseSettings):
    """
    Configuración global del chatbot RAG.
    
    Carga todas las configuraciones desde variables de entorno (.env).
    Centraliza la gestión de parámetros para API, base de datos, LLM, etc.
    
    Uso:
        >>> from config.settings import settings
        >>> print(settings.api_port)  # 8000
    """
    
    # ========================================================================
    # CONFIGURACIÓN DE LLM CON STREAMING (CodingBuddy - OpenAI Compatible)
    # ========================================================================
    llm_api_endpoint: str = Field(
        default="https://ia-research-dev.codingbuddy-4282826dce7d155229a320302e775459-0000.eu-de.containers.appdomain.cloud/research/llm/stream/openai/clients",
        validation_alias=AliasChoices("LLM_API_ENDPOINT", "API_ENDPOINT")
    )  # Endpoint LLM
    llm_api_key: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("LLM_API_KEY", "API_KEY")
    )  # Clave API para LLM (X-API-KEY)
    llm_model: str = "gpt-4o"  # Modelo LLM: gpt-4o, gpt-4-turbo, etc.
    llm_user_email: str = Field(
        default="ismael@research.com",
        validation_alias=AliasChoices("LLM_USER_EMAIL", "USER_EMAIL")
    )  # Usuario registrado en CodingBuddy
    llm_streaming_enabled: bool = True  # Habilitar streaming de respuestas
    llm_max_tokens: int = 1500  # Tokens máximos por respuesta
    llm_temperature: float = 0.7  # Temperatura: 0=determinista, 1=creativo
    
    # ========================================================================
    # CONFIGURACIÓN DE OPENAI (APIs de LLM y Embeddings)
    # ========================================================================
    openai_api_key: Optional[str] = None  # Clave API de OpenAI
    openai_model: str = "gpt-4-turbo-preview"  # Modelo LLM para generación de respuestas
    openai_embedding_model: str = "text-embedding-3-small"  # Modelo para vectorización
    
    # ========================================================================
    # CONFIGURACIÓN DE APIs EXTERNAS
    # ========================================================================
    steam_api_key: Optional[str] = None  # Clave para Steam Web API
    ggdeals_api_key: Optional[str] = None  # Clave para GG.deals API (precios EUR)
    
    # ========================================================================
    # CONFIGURACIÓN DE MONGODB
    # ========================================================================
    mongodb_uri: str = "mongodb://localhost:27017"  # URI de conexión
    mongodb_db_name: str = "videogames_recommender"  # Nombre de la base de datos
    
    # ========================================================================
    # CONFIGURACIÓN DE VECTOR STORE (RAG)
    # ========================================================================
    vector_store_type: str = "faiss"  # Tipo: FAISS o ChromaDB
    vector_store_path: str = "./data/vector_store"  # Ruta de índices FAISS
    
    # ========================================================================
    # CONFIGURACIÓN DE API REST
    # ========================================================================
    api_host: str = "0.0.0.0"  # Interfaz de escucha (0.0.0.0 = todas)
    api_port: int = 8000  # Puerto de escucha
    api_reload: bool = True  # Recargar servidor en cambios (desarrollo)
    
    # ========================================================================
    # CONFIGURACIÓN DE RAG
    # ========================================================================
    top_k_results: int = 5  # Número de juegos a devolver en búsqueda
    max_tokens: int = 1000  # Tokens máximos en respuesta LLM
    temperature: float = 0.7  # Creatividad del LLM (0-1): 0=determinista, 1=creativo
    
    # ========================================================================
    # CONFIGURACIÓN DE LOGGING
    # ========================================================================
    log_level: str = "INFO"  # Nivel de logging: DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    class Config:
        """Configuración de Pydantic para cargar desde .env"""
        env_file = "../.env"  # Archivo de configuración en la raíz del workspace
        case_sensitive = False  # Variables de entorno case-insensitive


# Instancia global de configuración
# Se crea una única instancia que se importa en toda la aplicación
settings = Settings()
