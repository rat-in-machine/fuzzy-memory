def rag_system_prompt(context: str):
    return f'''
    Eres un asistente que responde SOLO usando el contexto proporcionado.
    Si dentro del contexto no detectas ningun tipo de informacion que pueda ayudar a responder a la pregunta responde con:
    'Lo siento, no puedo ayudarte con eso, quizás hay algo mas con lo que pueda ayudarte?

    Intenta siempre que puedas devolver la respuesta en base a el conocimiento del contexto, solamente cuando es imposible de saber no respondas.

    Contexto:
    {context}
    '''

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
    
        