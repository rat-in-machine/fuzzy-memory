"""
LLM Chain para generación de recomendaciones
"""

from typing import List, Dict
import logging
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

from .prompts import get_recommendation_prompt, format_game_context

logger = logging.getLogger(__name__)


class RecommendationChain:
    """
    Chain de LangChain para generar recomendaciones explicadas
    """
    
    def __init__(
        self,
        model_name: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        """
        Args:
            model_name: Modelo de OpenAI a usar
            temperature: Creatividad del modelo (0-1)
            max_tokens: Máximo de tokens en respuesta
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        self.prompt = get_recommendation_prompt()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory,
            verbose=True
        )
    
    def generate_recommendation(
        self,
        query: str,
        retrieved_games: List[Dict]
    ) -> str:
        """
        Genera recomendación basada en query del usuario y juegos recuperados
        
        Args:
            query: Consulta en lenguaje natural del usuario
            retrieved_games: Lista de juegos relevantes de la BD
            
        Returns:
            Recomendación generada por el LLM
        """
        logger.info(f"Generando recomendación para: '{query}'")
        
        # Formatear contexto de juegos
        context = format_game_context(retrieved_games)
        
        # Generar recomendación
        try:
            response = self.chain.predict(
                query=query,
                context=context
            )
            
            logger.info("Recomendación generada exitosamente")
            return response
            
        except Exception as e:
            logger.error(f"Error generando recomendación: {e}")
            return "Lo siento, hubo un error generando la recomendación. Por favor intenta de nuevo."
    
    def clear_memory(self):
        """Limpia el historial de conversación"""
        self.memory.clear()
        logger.info("Memoria de conversación limpiada")
    
    def get_chat_history(self) -> List[Dict]:
        """Obtiene el historial de conversación"""
        return self.memory.chat_memory.messages
