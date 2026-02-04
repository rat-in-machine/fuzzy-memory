"""
Generación de embeddings y gestión de vector store
"""

from typing import List, Dict
import logging
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

logger = logging.getLogger(__name__)


class GameVectorizer:
    """
    Gestiona la creación y búsqueda de embeddings de videojuegos
    """
    
    def __init__(self, embedding_model: str = "text-embedding-3-small"):
        """
        Args:
            embedding_model: Modelo de OpenAI para embeddings
        """
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vector_store = None
    
    def create_documents(self, games: List[Dict]) -> List[Document]:
        """
        Convierte juegos en documentos para vectorización
        
        Args:
            games: Lista de diccionarios con información de juegos
            
        Returns:
            Lista de objetos Document de LangChain
        """
        documents = []
        
        for game in games:
            # Crear contenido textual rico para embeddings
            content = self._build_game_content(game)
            
            # Metadata para filtrado y recuperación
            metadata = {
                "game_id": str(game.get("_id", "")),
                "steam_id": game.get("steam_id"),
                "name": game.get("name"),
                "genres": game.get("genres", []),
                "developers": game.get("developers", []),
                "release_year": self._extract_year(game.get("release_date")),
            }
            
            doc = Document(page_content=content, metadata=metadata)
            documents.append(doc)
        
        logger.info(f"Creados {len(documents)} documentos para vectorización")
        return documents
    
    def _build_game_content(self, game: Dict) -> str:
        """
        Construye texto rico para embedding
        
        Incluye: nombre, descripción, géneros, desarrolladores, tags
        """
        parts = [
            f"Nombre: {game.get('name', '')}",
            f"Descripción: {game.get('description', '')}",
        ]
        
        if game.get("genres"):
            genres_str = ", ".join(game["genres"])
            parts.append(f"Géneros: {genres_str}")
        
        if game.get("developers"):
            devs_str = ", ".join(game["developers"])
            parts.append(f"Desarrolladores: {devs_str}")
        
        if game.get("categories"):
            cats_str = ", ".join(game["categories"][:5])  # Top 5
            parts.append(f"Categorías: {cats_str}")
        
        return "\n".join(parts)
    
    def _extract_year(self, date_str: str) -> int:
        """Extrae el año de una fecha"""
        if not date_str:
            return 0
        try:
            return int(date_str.split()[-1])
        except:
            return 0
    
    def build_vector_store(self, documents: List[Document]) -> FAISS:
        """
        Construye el vector store con FAISS
        
        Args:
            documents: Lista de documentos a vectorizar
            
        Returns:
            Vector store FAISS
        """
        logger.info(f"Generando embeddings para {len(documents)} documentos...")
        
        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        logger.info("Vector store creado exitosamente")
        return self.vector_store
    
    def save_vector_store(self, path: str):
        """Guarda el vector store en disco"""
        if not self.vector_store:
            raise ValueError("No hay vector store para guardar")
        
        self.vector_store.save_local(path)
        logger.info(f"Vector store guardado en {path}")
    
    def load_vector_store(self, path: str) -> FAISS:
        """Carga un vector store desde disco"""
        self.vector_store = FAISS.load_local(
            path,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True
        )
        logger.info(f"Vector store cargado desde {path}")
        return self.vector_store
    
    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter_metadata: Dict = None
    ) -> List[Document]:
        """
        Búsqueda por similitud semántica
        
        Args:
            query: Consulta en lenguaje natural
            k: Número de resultados a devolver
            filter_metadata: Filtros adicionales (género, año, etc.)
            
        Returns:
            Lista de documentos más similares
        """
        if not self.vector_store:
            raise ValueError("Vector store no inicializado")
        
        results = self.vector_store.similarity_search(
            query=query,
            k=k,
            filter=filter_metadata
        )
        
        logger.info(f"Encontrados {len(results)} resultados para: '{query}'")
        return results
