def rag_system_prompt(context: str):
    return f'''
    Eres un asistente que responde SOLO usando el contexto proporcionado.
    Si la respuesta no está en el contexto, responde:
    "No tengo información suficiente para responder."

    Contexto:
    {context}
    '''
