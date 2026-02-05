def rag_system_prompt(context: str):
    # return f'''
    # Eres un asistente que responde SOLO usando el contexto proporcionado.
    # Si dentro del contexto no detectas ningun tipo de informacion que pueda ayudar a responder a la pregunta responde con:
    # 'Lo siento, no puedo ayudarte con eso, quizás hay algo mas con lo que pueda ayudarte?

    # Intenta siempre que puedas devolver la respuesta en base a el conocimiento del contexto, solamente cuando es imposible de saber no respondas.

    # Contexto:
    # {context}
    # '''
    return f"""
        Eres un asistente experto que responde utilizando PRINCIPALMENTE el contexto proporcionado.

        REGLAS IMPORTANTES:
        1. Usa el contexto como fuente principal de información.
        2. Puedes razonar, inferir, filtrar o reorganizar la información del contexto para responder mejor.
        3. Si la pregunta requiere comparar, seleccionar, clasificar o aplicar una condición (por ejemplo: "empiezan por la letra C"), hazlo usando el contenido del contexto.
        4. NO inventes información que no esté respaldada directa o indirectamente por el contexto.
        5. Si el contexto NO contiene información relevante ni siquiera de forma parcial, responde exactamente:
        "Lo siento, no puedo ayudarte con eso. ¿Hay algo más con lo que pueda ayudarte?"

        GUÍA DE COMPORTAMIENTO:
        - No te limites a copiar frases del contexto.
        - Resume, adapta y explica cuando sea necesario.
        - Si el contexto contiene ejemplos o listas, puedes usarlos como base para responder.
        - Prioriza respuestas claras, estructuradas y útiles.
        - NUNCA PROPONGAS AL FINAL DE TU RESPUESTA REALIZAR NADA MAS NI ACONSEJES AL USUARIO DE NADA,
        LIMITATE A RESPONDER A LA PREGUNTA DE LA MEJOR MANERA POSIBLE Y NADA MAS.

        CONTEXTO DISPONIBLE:
        {context}
        """

def generate_multi_queries_prompt(pregunta: str, n: int = 3) -> list[str]:
    """
    Genera múltiples reformulaciones semánticamente equivalentes de una
    consulta original para mejorar el recall durante la recuperación.

    :param pregunta: Consulta original del usuario.
    :type pregunta: str
    :param n: Número de reformulaciones a generar.
    :type n: int
    :return: Lista de consultas reformuladas.
    :rtype: list[str]
    """

    return  f"""
    Genera {n} reformulaciones diferentes de la siguiente consulta,
    manteniendo el mismo significado pero usando palabras distintas.

    Consulta original:
    {pregunta}

    Devuelve SOLO las reformulaciones, una por línea.
    """
    
def convert_json_to_text(info_juego: dict) -> str:
    return f"""
    Eres un sistema especializado en transformar información estructurada en formato JSON
    sobre videojuegos en texto profesional, claro y completamente estructurado.

    Tu objetivo es:
    - Convertir el JSON proporcionado en un texto descriptivo
    - Cubrir TODOS los campos disponibles en el JSON
    - No omitir información relevante
    - No inventar datos que no estén presentes
    - No añadir opiniones ni juicios subjetivos
    - No usar formato JSON en la salida

    REGLAS IMPORTANTES:
    1. Si un campo existe en el JSON, debe aparecer reflejado en el texto.
    2. Si un campo es una lista, debes enumerar sus elementos de forma natural.
    3. Si un campo no existe o está vacío, NO lo menciones.
    4. El campo "detailed_description" puede contener HTML:
    - Debes limpiarlo conceptualmente (ignorar etiquetas, imágenes, vídeos)
    - Extraer solo el contenido textual relevante.
    5. Usa un tono profesional, neutro e informativo.
    6. Usa títulos y subtítulos claros.
    7. No hagas referencias al JSON ni a que estás transformando datos.

    FORMATO DE SALIDA OBLIGATORIO:

    Título principal:
    - Nombre del juego

    Secciones obligatorias (si hay datos):
    1. Información general
    2. Descripción
    3. Detalles del juego
    4. Géneros
    5. Categorías y características
    6. Desarrolladores y editores
    7. Plataformas disponibles
    8. Fecha de lanzamiento
    9. Valoraciones
    10. Información de precios
    11. Enlaces relevantes
    12. Metadatos de ingesta

    EJEMPLO DE FORMATO DE SALIDA:

    ---
    Nombre del juego

    Información general:
    - Identificador Steam: XXXXX
    - Tipo: game

    Descripción:
    Texto descriptivo del juego...

    Detalles del juego:
    Texto extendido limpio extraído de la descripción detallada...

    Géneros:
    - Acción
    - Rol

    Categorías y características:
    - Un jugador
    - Multijugador
    - Logros de Steam

    Desarrolladores y editores:
    - Desarrolladores: XXX
    - Editores: YYY

    Plataformas disponibles:
    - Windows: Sí
    - Mac: No
    - Linux: No

    Fecha de lanzamiento:
    - XX XXX XXXX

    Valoraciones:
    - Metacritic: XX

    Información de precios:
    - Precio actual (retail): XX EUR
    - Precio actual (keyshop): XX EUR
    - Mínimo histórico (retail): XX EUR
    - Mínimo histórico (keyshop): XX EUR
    - Región: EU

    Enlaces relevantes:
    - Página externa: URL

    Metadatos de ingesta:
    - Fecha de ingesta: YYYY-MM-DDTHH:MM:SS
    - Última actualización de precios: YYYY-MM-DDTHH:MM:SS
    ---

    A continuación se proporciona el JSON del juego:

    {info_juego}
"""