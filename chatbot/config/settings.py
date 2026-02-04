from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración global del chatbot RAG"""
    
    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4-turbo-preview"
    openai_embedding_model: str = "text-embedding-3-small"
    
    # APIs Externas
    steam_api_key: Optional[str] = None
    ggdeals_api_key: Optional[str] = None
    
    # MongoDB
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "videogames_recommender"
    
    # Vector Store
    vector_store_type: str = "faiss"
    vector_store_path: str = "./data/vector_store"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # RAG Configuration
    top_k_results: int = 5
    max_tokens: int = 1000
    temperature: float = 0.7
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instancia global de configuración
settings = Settings()
