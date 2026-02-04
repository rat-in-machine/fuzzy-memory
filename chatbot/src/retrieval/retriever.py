"""
Sistema de recuperación híbrido: vectorial + filtros
"""

from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class HybridRetriever:
    """
    Retriever híbrido que combina:
    1. Búsqueda vectorial (similitud semántica)
    2. Filtrado por metadatos (géneros, precio, año)
    3. Re-ranking por popularidad/rating
    """
    
    def __init__(self, vector_store, db_client):
        """
        Args:
            vector_store: Store de vectores (FAISS)
            db_client: Cliente de MongoDB para filtros adicionales
        """
        self.vector_store = vector_store
        self.db_client = db_client
    
    def retrieve(
        self,
        query: str,
        k: int = 5,
        genres: Optional[List[str]] = None,
        max_price: Optional[float] = None,
        min_year: Optional[int] = None,
    ) -> List[Dict]:
        """
        Recupera juegos relevantes combinando búsqueda vectorial y filtros
        
        Args:
            query: Consulta en lenguaje natural
            k: Número de resultados
            genres: Lista de géneros preferidos
            max_price: Precio máximo
            min_year: Año mínimo de lanzamiento
            
        Returns:
            Lista de juegos con score de relevancia
        """
        logger.info(f"Retrieving con query: '{query}', k={k}")
        
        # 1. Búsqueda vectorial inicial (más resultados de los necesarios)
        initial_k = k * 3
        vector_results = self.vector_store.similarity_search_with_score(
            query=query,
            k=initial_k
        )
        
        # 2. Extraer IDs de juegos
        game_ids = [doc.metadata.get("game_id") for doc, _ in vector_results]
        
        # 3. Obtener información completa de BD con filtros
        games = self._fetch_games_with_filters(
            game_ids=game_ids,
            genres=genres,
            max_price=max_price,
            min_year=min_year
        )
        
        # 4. Re-ranking por score vectorial + popularidad
        ranked_games = self._rerank(games, vector_results)
        
        # 5. Top-K final
        return ranked_games[:k]
    
    def _fetch_games_with_filters(
        self,
        game_ids: List[str],
        genres: Optional[List[str]],
        max_price: Optional[float],
        min_year: Optional[int]
    ) -> List[Dict]:
        """
        Obtiene juegos de MongoDB aplicando filtros
        """
        from bson import ObjectId
        
        # Construir query de MongoDB
        query = {"_id": {"$in": [ObjectId(gid) for gid in game_ids]}}
        
        if genres:
            query["genres"] = {"$in": genres}
        
        if max_price is not None:
            query["current_price"] = {"$lte": max_price}
        
        if min_year is not None:
            query["release_year"] = {"$gte": min_year}
        
        # Ejecutar query
        games = list(self.db_client.videogames.find(query))
        
        logger.info(f"Filtrados {len(games)} juegos de {len(game_ids)} iniciales")
        return games
    
    def _rerank(
        self,
        games: List[Dict],
        vector_results: List[tuple]
    ) -> List[Dict]:
        """
        Re-ordena juegos combinando similarity score y métricas del juego
        """
        # Crear mapa de similarity scores
        score_map = {}
        for doc, score in vector_results:
            game_id = doc.metadata.get("game_id")
            score_map[game_id] = score
        
        # Calcular score híbrido
        for game in games:
            game_id = str(game["_id"])
            
            # Score vectorial (normalizado 0-1)
            vector_score = 1 / (1 + score_map.get(game_id, 1.0))
            
            # Score de popularidad (basado en metacritic, reviews, etc.)
            popularity_score = self._calculate_popularity_score(game)
            
            # Score final ponderado
            game["relevance_score"] = (
                0.7 * vector_score +
                0.3 * popularity_score
            )
        
        # Ordenar por score descendente
        games.sort(key=lambda g: g.get("relevance_score", 0), reverse=True)
        
        return games
    
    def _calculate_popularity_score(self, game: Dict) -> float:
        """
        Calcula score de popularidad normalizado (0-1)
        
        Considera:
        - Metacritic score
        - Número de reviews (si disponible)
        - Edad del juego (más reciente = mayor score)
        """
        score = 0.0
        
        # Metacritic (peso 0.5)
        if game.get("metacritic"):
            score += (game["metacritic"] / 100) * 0.5
        
        # Año de lanzamiento (peso 0.3)
        if game.get("release_year"):
            year_score = min((game["release_year"] - 2000) / 25, 1.0)
            score += year_score * 0.3
        
        # Placeholder para reviews (peso 0.2)
        # TODO: añadir cuando tengamos reviews
        score += 0.1  # Base score
        
        return min(score, 1.0)
