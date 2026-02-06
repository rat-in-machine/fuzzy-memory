from typing import Optional

from utils.config import MODELO_EMBEDDING, MILVUS_COLLECTION_NAME, TOP_K
from rag.milvus.services import hybrid_search, build_context


# from llm.openai.llm import llamar_llm_openai
from rag.llm_rag.NextAI.llm import llm_call

from rag.llm_rag.prompts import rag_system_prompt, generate_multi_queries_prompt


def generate_multiquery(pregunta: str, n: int = 3) -> list[str]:
    """
    Genera múltiples reformulaciones semánticamente equivalentes de una
    consulta original para mejorar el recall durante la recuperación.

    :param pregunta: Consulta original del usuario.
    :type pregunta: str
    :param n: Número de reformulaciones adicionales a generar.
    :type n: int
    :return: Lista de consultas reformuladas, incluyendo la original.
    :rtype: list[str]
    """
    try:
        prompt = generate_multi_queries_prompt(pregunta=pregunta, n=n)
    except Exception as e:
        print("ERROR GENERANDO EL PROMPT DE MULTIQUERY: ",e)

    # response = llamar_llm_openai(prompt_usuario=prompt)
    try:
        response = llm_call(prompt_usuario=prompt)
    except Exception as e:
        print("ERROR LLAMANDO AL MODELO PARA MULTIQUERY: ",e)

    try:
        queries = [q.strip() for q in response.split("\n") if q.strip()]
    except Exception as e:
        print("ERROR CREANDO LA QUERY DE MULTIQUERY: ",e)
        
    return [pregunta] + queries

def multi_query_hybrid_search(pregunta: str,collection_name: str = "Pruebas_Juegos_Steam",top_k: int = TOP_K,n_queries: int = 3) -> list[str]:
    """
    Ejecuta una búsqueda híbrida utilizando múltiples reformulaciones
    de la consulta original y fusiona los resultados obtenidos.

    :param pregunta: Consulta original del usuario.
    :type pregunta: str
    :param collection_name: Nombre de la colección de Milvus.
    :type collection_name: str
    :param top_k: Número de resultados a recuperar por reformulación.
    :type top_k: int
    :param n_queries: Número de reformulaciones a generar.
    :type n_queries: int
    :return: Lista fusionada de fragmentos relevantes sin duplicados.
    :rtype: list[str]
    """
    try:
        queries = generate_multiquery(pregunta, n=n_queries)
    except Exception as e:
        print("ERROR BUSCANDO CON HYBRID MULTY QUERY: ",e)

    seen = set()
    merged = []

    for q in queries:
        try:
            query_vector = MODELO_EMBEDDING.embed_query(q)
        except Exception as e:
            continue

        try:
            chunks = hybrid_search(
                query=q,
                query_vector=query_vector,
                collection_name=collection_name,
                top_k=top_k
            )
        except Exception as e:
            continue

        for chunk in chunks:
            if chunk not in seen:
                seen.add(chunk)
                merged.append(chunk)

    return merged

def rag_system_call(pregunta: str,collection_name: str = MILVUS_COLLECTION_NAME,top_k: int = TOP_K,id_chat: Optional[str] = None) -> str:
    """
    Orquesta el flujo completo de un sistema RAG (Retrieval-Augmented Generation),
    incorporando expansión de consultas (multi-query), búsqueda híbrida y
    generación de respuestas mediante un modelo de lenguaje.

    :param pregunta: Consulta formulada por el usuario en lenguaje natural.
    :type pregunta: str
    :param collection_name: Nombre de la colección de Milvus utilizada.
    :type collection_name: str
    :param top_k: Número máximo de fragmentos que se usarán como contexto.
    :type top_k: int
    :param id_chat: Identificador opcional de conversación.
    :type id_chat: Optional[str]
    :return: Respuesta generada por el modelo de lenguaje.
    :rtype: str
    """
    try:
        chunks = multi_query_hybrid_search(
            pregunta=pregunta,
            collection_name=collection_name,
            top_k=top_k * 2,
            n_queries=3
        )
    except Exception as e:
        print("ERROR OBTENIENDO CHUNKS PARA LA LLAMADA CON RAG:", e)

    if not chunks:
        return "No tengo información suficiente para responder."

    try:
        context = build_context(chunks[:top_k])
    except Exception as e:
        print("ERROR AL OBTENER EL CONTEXTO DE CHUNKS PARA LLAMADA RAG: ",e)
    system_prompt = rag_system_prompt(context=context)


    # return llamar_llm_openai(
    #     prompt_usuario=pregunta,
    #     prompt_sistema=system_prompt,
    #     id_chat=id_chat
    # )
    try:
        return llm_call(
            prompt_usuario=pregunta,
            prompt_sistema=system_prompt,
            id_chat=id_chat
        )
    except Exception as e:
        print("ERROR AL ELABORAR LA RESPUESTA DEL MODELO CON EL RAG: ",e)