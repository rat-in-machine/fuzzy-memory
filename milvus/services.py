from milvus.connection import get_milvus

def search_dense(query_vector: list[float],collection_name: str = "Pruebas",top_k: int = 5) -> list[str]:

    '''
    Realiza una búsqueda vectorial semántica (dense search) en una colección
    de Milvus utilizando embeddings numéricos.

    La búsqueda se basa en la similitud entre el vector de consulta y los
    vectores almacenados en la colección, devolviendo los fragmentos de texto
    más relevantes según la métrica definida en el índice (por ejemplo, COSINE).

    :param query_vector: Vector de embedding que representa la consulta del usuario.
    :type query_vector: list[float]
    :param collection_name: Nombre de la colección de Milvus sobre la que se
                            realizará la búsqueda.
    :type collection_name: str
    :param top_k: Número máximo de resultados más similares que se desean recuperar.
    :type top_k: int
    :return: Lista de fragmentos de texto asociados a los vectores más similares
             encontrados en la búsqueda.
    :rtype: list[str]
    '''

    try:
        milvus_client = get_milvus()
    except Exception as e:
        print("ERROR AL OBTENER EL CLIENTE DE MILVUS EN LA SEARCH DENSE: ",e)

    try:
        results = milvus_client.search(
            collection_name=collection_name,
            data=[query_vector],
            anns_field="vector",
            limit=top_k,
            output_fields=["text"]
        )
    except Exception as e:
        print("ERROR AL OBTENER RESULTADOS DE LA MILVUS: ",e)

    return [
        hit["entity"].get("text", "")
        for hit in results[0]
        if hit["entity"].get("text")
    ]


def search_lexical(query: str,collection_name: str = "Pruebas",top_k: int = 5) -> list[str]:
    '''
    Realiza una búsqueda léxica basada en coincidencia de texto dentro de una
    colección de Milvus.

    Este tipo de búsqueda identifica fragmentos de texto que contienen la
    cadena de consulta de forma explícita, siendo especialmente útil para
    detectar palabras clave, nombres propios, acrónimos o términos exactos
    que pueden no ser capturados adecuadamente por la búsqueda semántica.

    :param query: Cadena de texto utilizada como criterio de búsqueda léxica.
    :type query: str
    :param collection_name: Nombre de la colección de Milvus sobre la que se
                            realizará la búsqueda.
    :type collection_name: str
    :param top_k: Número máximo de resultados que se desean recuperar.
    :type top_k: int
    :return: Lista de fragmentos de texto que contienen coincidencias léxicas
             con la consulta proporcionada.
    :rtype: list[str]
    '''

    try:
        milvus_client = get_milvus()
    except Exception as e:
        print("ERROR AL CONECTAR A LA MILVUS EN LA BUSQUEDA LEXICA: ",e)

    expr = f'text like "%{query}%"'
    try:
        results = milvus_client.query(
            collection_name,
            expr,
            output_fields=["text"],
            limit=top_k
        )
    except Exception as e:
        print("ERROR AL OBTENER RESULTADOS CON LA BSUQEUDA LEXICA: ",e)

    return [r["text"] for r in results if r.get("text")]


def hybrid_search(query: str,query_vector: list[float],collection_name: str = "Pruebas",top_k: int = 5) -> list[str]:
    
    '''
    Ejecuta una búsqueda híbrida combinando búsqueda semántica (dense) y
    búsqueda léxica sobre una colección de Milvus.

    Los resultados de ambos métodos se fusionan en una única lista,
    eliminando duplicados y preservando el orden de relevancia relativo.
    Este enfoque permite capturar tanto similitud semántica como coincidencias
    exactas de términos, mejorando el recall global del sistema RAG.

    :param query: Consulta original del usuario utilizada para la búsqueda léxica.
    :type query: str
    :param query_vector: Vector de embedding que representa semánticamente la consulta.
    :type query_vector: list[float]
    :param collection_name: Nombre de la colección de Milvus donde se realiza la búsqueda.
    :type collection_name: str
    :param top_k: Número máximo de resultados a recuperar por cada tipo de búsqueda.
    :type top_k: int
    :return: Lista combinada de fragmentos de texto resultantes de la búsqueda
             semántica y léxica, sin duplicados.
    :rtype: list[str]
    '''
    try:
        dense_chunks = search_dense(query_vector, collection_name, top_k)
    except Exception as e:
        print("ERROR AL OBTENER DENSE CHUNKS EN LA BUSQUEDA HIBRIDA: ",e)
    try:
        lexical_chunks = search_lexical(query, collection_name, top_k)
    except Exception as e:
        print("ERROR AL OBTENER CHUNKS DE LA BUSQUEDA LEXICA: ",e)

    seen = set()
    merged = []

    for chunk in dense_chunks + lexical_chunks:
        if chunk not in seen:
            seen.add(chunk)
            merged.append(chunk)

    return merged


def build_context(chunks: list[str]) -> str:
    '''
    Construye un bloque de contexto a partir de una lista de fragmentos de texto
    recuperados, formateado para ser utilizado como entrada en un prompt de RAG.

    Cada fragmento se presenta como un elemento independiente, facilitando al
    modelo de lenguaje la identificación de información relevante y reduciendo
    el riesgo de alucinaciones durante la generación de la respuesta.

    :param chunks: Lista de fragmentos de texto recuperados tras la búsqueda.
    :type chunks: list[str]
    :return: Texto formateado que representa el contexto completo para el modelo
             de lenguaje.
    :rtype: str
    '''
    try:
        return "\n\n".join(f"- {chunk}" for chunk in chunks)
    except Exception as e:
        print("ERROR A LA HORA DE CONSTRUIR EL CONTEXTO: ",e)
