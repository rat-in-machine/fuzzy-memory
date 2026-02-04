from .llm import llamar_llm_openai
from milvus.connection import get_milvus
from typing import Optional
from .prompts import rag_system_prompt

from utils.config import MODELO_EMBEDDING


def search_dense(query_vector: list[float],collection_name: str = "Pruebas",top_k: int = 5) -> list[str]:
    '''
    Docstring for search_dense
    
    :param query_vector: Description
    :type query_vector: list[float]
    :param collection_name: Description
    :type collection_name: str
    :param top_k: Description
    :type top_k: int
    :return: Description
    :rtype: list[str]
    '''
    milvus_client = get_milvus()

    results = milvus_client.search(
        collection_name=collection_name,
        data=[query_vector],
        anns_field="vector",
        limit=top_k,
        output_fields=["text"]
    )

    chunks = [
        hit["entity"].get("text", "")
        for hit in results[0]
        if hit["entity"].get("text")
    ]

    return chunks

def search_lexical(query: str,collection_name: str = "Pruebas",top_k: int = 5) -> list[str]:
    '''
    Docstring for search_lexical
    
    :param query: Description
    :type query: str
    :param collection_name: Description
    :type collection_name: str
    :param top_k: Description
    :type top_k: int
    :return: Description
    :rtype: list[str]
    '''

    milvus_client = get_milvus()

    expr = f'text like "%{query}%"'

    results = milvus_client.query(
        collection_name,
        expr,
        output_fields=["text"],
        limit=top_k
    )

    return [r["text"] for r in results if r.get("text")]

def hybrid_search(query: str,query_vector: list[float],collection_name: str = "Pruebas",top_k: int = 5) -> list[str]:
    '''
    Docstring for hybrid_search
    
    :param query: Description
    :type query: str
    :param query_vector: Description
    :type query_vector: List[float]
    :param collection_name: Description
    :type collection_name: str
    :param top_k: Description
    :type top_k: int
    :return: Description
    :rtype: list[str]
    '''

    dense_chunks = search_dense(
        query_vector=query_vector,
        collection_name=collection_name,
        top_k=top_k
    )

    lexical_chunks = search_lexical(
        query=query,
        collection_name=collection_name,
        top_k=top_k
    )

    seen = set()
    merged = []

    for chunk in dense_chunks + lexical_chunks:
        if chunk not in seen:
            seen.add(chunk)
            merged.append(chunk)

    return merged

def rerank_chunks(pregunta: str,chunks: list[str]) -> list[str]:
    '''
    Docstring for rerank_chunks
    
    :param pregunta: Description
    :type pregunta: str
    :param chunks: Description
    :type chunks: list[str]
    :return: Description
    :rtype: list[str]
    '''

    if len(chunks) <= 1:
        return chunks

    prompt = f"""
            Pregunta:
            {pregunta}

            Fragmentos:
            {chr(10).join(f"[{i}] {c}" for i, c in enumerate(chunks))}

            Devuelve SOLO los índices ordenados del fragmento más relevante
            al menos relevante, separados por comas.
            Ejemplo:
            2,0,1
            """

    response = llamar_llm_openai(prompt_usuario=prompt)

    try:
        order = [int(i.strip()) for i in response.split(",")]
        return [chunks[i] for i in order if i < len(chunks)]
    except Exception:

        return chunks
    
def build_context(chunks: list[str]) -> str:
    '''
    Docstring for build_context
    
    :param chunks: Description
    :type chunks: list[str]
    :return: Description
    :rtype: str
    '''
    return "\n\n".join(f"- {chunk}" for chunk in chunks)

def rag_system_call(pregunta: str,collection_name: str = "Pruebas",top_k: int = 5,id_chat: Optional[str] = None) -> str:
    '''
    Docstring for rag_system_call
    
    :param pregunta: Description
    :type pregunta: str
    :param collection_name: Description
    :type collection_name: str
    :param top_k: Description
    :type top_k: int
    :param id_chat: Description
    :type id_chat: Optional[str]
    :return: Description
    :rtype: str
    '''

    query_vector = MODELO_EMBEDDING.embed_query(pregunta)

    chunks = hybrid_search(query=pregunta,query_vector=query_vector,collection_name=collection_name,top_k=top_k * 2)

    print(f"CHUNKS OBTENIDOS (pre-rerank): {chunks}")

    if not chunks:
        return "No tengo información suficiente para responder."

    chunks = rerank_chunks(pregunta, chunks)[:top_k]

    print(f"CHUNKS OBTENIDOS (post-rerank): {chunks}")


    context = build_context(chunks)

    system_prompt = rag_system_prompt(context=context)

    return llamar_llm_openai(prompt_usuario=pregunta,prompt_sistema=system_prompt,id_chat=id_chat)