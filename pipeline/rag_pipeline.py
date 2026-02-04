from typing import Optional

from utils.config import MODELO_EMBEDDING
from milvus.services import hybrid_search, build_context
from llm.openai.llm import llamar_llm_openai
from llm.openai.prompts import rag_system_prompt


def rag_system_call(pregunta: str,collection_name: str = "Pruebas",top_k: int = 5,id_chat: Optional[str] = None) -> str:
    '''
    Orquesta el flujo completo de un sistema RAG (Retrieval-Augmented Generation),
    combinando búsqueda híbrida en una base de datos vectorial y generación de
    respuestas mediante un modelo de lenguaje.

    El proceso incluye la vectorización de la consulta del usuario, la recuperación
    de fragmentos relevantes mediante búsqueda semántica y léxica, la construcción
    de un contexto controlado y la generación final de la respuesta utilizando
    un LLM. Si no se recupera información relevante, se devuelve un mensaje
    indicando la falta de contexto suficiente.

    :param pregunta: Consulta formulada por el usuario en lenguaje natural.
    :type pregunta: str
    :param collection_name: Nombre de la colección de Milvus que contiene los
                            datos indexados utilizados para la recuperación.
    :type collection_name: str
    :param top_k: Número máximo de fragmentos relevantes que se utilizarán para
                  construir el contexto pasado al modelo de lenguaje.
    :type top_k: int
    :param id_chat: Identificador opcional de la conversación, utilizado para
                    mantener trazabilidad o contexto conversacional entre
                    interacciones sucesivas.
    :type id_chat: Optional[str]
    :return: Respuesta generada por el modelo de lenguaje basada exclusivamente
             en el contexto recuperado.
    :rtype: str
    '''

    query_vector = MODELO_EMBEDDING.embed_query(pregunta)

    chunks = hybrid_search(
        query=pregunta,
        query_vector=query_vector,
        collection_name=collection_name,
        top_k=top_k * 2
    )

    if not chunks:
        return "No tengo información suficiente para responder."

    context = build_context(chunks[:top_k])

    system_prompt = rag_system_prompt(context=context)

    return llamar_llm_openai(
        prompt_usuario=pregunta,
        prompt_sistema=system_prompt,
        id_chat=id_chat
    )