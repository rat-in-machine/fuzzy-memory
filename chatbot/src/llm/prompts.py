"""
Sistema de prompts para el chatbot RAG
"""

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder


SYSTEM_PROMPT = """Eres un asistente experto en recomendación de videojuegos.

Tu trabajo es ayudar a los usuarios a encontrar juegos que les gusten basándote en:
- Sus preferencias expresadas en lenguaje natural
- Un contexto de juegos relevantes recuperados de nuestra base de datos
- Datos reales de precios, géneros y descripciones

REGLAS IMPORTANTES:
1. Solo recomienda juegos que aparezcan en el contexto proporcionado
2. NUNCA inventes juegos, precios o información que no esté en el contexto
3. Si no tienes información suficiente, dilo claramente
4. Explica por qué recomiendas cada juego (género, gameplay, precio, etc.)
5. Sé conciso pero informativo
6. Si mencionas precios, indica la fuente (GG.deals)
7. Si mencionas información del juego, indica que viene de Steam

FORMATO DE RESPUESTA:
- Presenta 3-5 juegos recomendados
- Para cada uno: nombre, géneros, por qué encaja, precio actual
- Ordena de más a menos recomendado
- Al final, pregunta si quiere más detalles o ajustar la búsqueda

TONO:
- Amigable y entusiasta
- Claro y directo
- Educativo cuando sea relevante
"""


RECOMMENDATION_TEMPLATE = """Basándote en la consulta del usuario y el contexto de juegos disponibles, 
proporciona recomendaciones personalizadas.

CONSULTA DEL USUARIO:
{query}

CONTEXTO DE JUEGOS RELEVANTES:
{context}

HISTORIAL DE CONVERSACIÓN:
{chat_history}

Genera tu recomendación siguiendo las reglas del sistema."""


def get_recommendation_prompt() -> ChatPromptTemplate:
    """
    Crea el prompt template para recomendaciones
    """
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", RECOMMENDATION_TEMPLATE)
    ])


CONTEXT_FORMATTER = """
Juego: {name}
Géneros: {genres}
Descripción: {description}
Desarrollador: {developers}
Precio actual: {price} (fuente: GG.deals)
Metacritic: {metacritic}
Año: {year}
---
"""


def format_game_context(games: list) -> str:
    """
    Formatea lista de juegos para incluir en el prompt
    
    Args:
        games: Lista de diccionarios con información de juegos
        
    Returns:
        String formateado con información de juegos
    """
    if not games:
        return "No se encontraron juegos relevantes en la base de datos."
    
    context_parts = []
    
    for game in games:
        context = CONTEXT_FORMATTER.format(
            name=game.get("name", "Desconocido"),
            genres=", ".join(game.get("genres", [])),
            description=game.get("description", "Sin descripción")[:200] + "...",
            developers=", ".join(game.get("developers", ["Desconocido"])),
            price=f"${game.get('current_price', 'N/A')}" if game.get("current_price") else "Precio no disponible",
            metacritic=game.get("metacritic", "N/A"),
            year=game.get("release_year", "N/A")
        )
        context_parts.append(context)
    
    return "\n".join(context_parts)
