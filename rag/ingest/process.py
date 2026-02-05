from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Union, List, Dict

from llm_rag.prompts import convert_json_to_text

# from llm.openai.llm import llamar_llm_openai
from llm_rag.NextAI.llm import llm_call


from milvus.connection import get_milvus
from utils.config import MODELO_EMBEDDING, MILVUS_COLLECTION_NAME

def generate_text_from_json(json_package: Union[Dict, List[Dict]]) -> str:
    """
    Genera un único texto descriptivo a partir de uno o varios documentos
    JSON de juegos, utilizando un prompt de sistema para transformar cada
    documento en texto estructurado y profesional.

    El texto resultante es la concatenación de todas las descripciones
    generadas, y está pensado para ser utilizado posteriormente en procesos
    de chunking, generación de embeddings o indexación en sistemas RAG.

    :param json_package: Documento JSON de un juego o lista de documentos JSON.
    :type json_package: dict | list[dict]
    :return: Texto concatenado con la información descriptiva de todos los juegos.
    :rtype: str
    """

    # if isinstance(json_package, dict):
    #     games = [json_package]
    # else:
    #     games = json_package
    try:
        if isinstance(json_package, dict):
            games = [json_package]
        else:
            games = json_package
    except TypeError as e:
        print("ERROR", e)

    texts: list[str] = []

    for game in games:
        try:

            system_prompt = convert_json_to_text(info_juego=game)

            text = llm_call(prompt_usuario="Genera el texto descriptivo siguiendo las instrucciones.", prompt_sistema=system_prompt)

            if text and text.strip():
                texts.append(text.strip())
        except Exception as e:
            print("ERROR GENERANDO TEXTO DEL JSON: ",e)

    return "\n\n" + ("\n\n" + ("-" * 80) + "\n\n").join(texts)


def create_chunks(text: str) -> list[str]:
    '''
    Divide un texto largo en fragmentos (chunks) más pequeños y solapados,
    adecuados para su posterior vectorización y almacenamiento en una base
    de datos vectorial.

    El uso de solapamiento permite preservar contexto entre fragmentos
    consecutivos y mejorar la recuperación semántica en sistemas RAG.

    :param text: Texto completo que se desea dividir en fragmentos.
    :type text: str
    :return: Lista de fragmentos de texto generados a partir del texto original.
    :rtype: list[str]
    '''
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=750,
            chunk_overlap=300
        )
    except TypeError as e:
        print("ERROR CREANDO CHUNKS",e)

    try:
        chunks = splitter.split_text(text=text)
        return chunks
    except Exception as e:
        print("ERROR",e)

    


def vector_generator(chunks: list[str]) -> list[list[float]]:
    '''
    Genera embeddings vectoriales para una lista de fragmentos de texto
    utilizando el modelo de embeddings configurado.

    Cada fragmento de texto se transforma en un vector numérico de dimensión
    fija, adecuado para operaciones de búsqueda semántica en bases de datos
    vectoriales como Milvus.

    :param chunks: Lista de fragmentos de texto a vectorizar.
    :type chunks: list[str]
    :return: Lista de vectores numéricos correspondientes a cada fragmento.
    :rtype: list[list[float]]
    '''
    try:
        return MODELO_EMBEDDING.embed_documents(chunks)
    except Exception as e:
        print("ERROR CREANDO LOS VECTORES: ", e)


def ingest_db(vectors: list[list[float]],chunks: list[str],collection_name: str = MILVUS_COLLECTION_NAME) -> int:
    '''
    Inserta fragmentos de texto y sus embeddings asociados en una colección
    de Milvus para su posterior recuperación mediante búsqueda vectorial.

    Cada fragmento de texto se almacena junto con su vector correspondiente,
    manteniendo una relación uno-a-uno entre texto y embedding. La colección
    debe existir previamente y estar configurada con un campo vectorial
    compatible con la dimensión de los embeddings generados.

    :param vectors: Lista de embeddings generados a partir de los fragmentos de texto.
    :type vectors: list[list[float]]
    :param chunks: Lista de fragmentos de texto originales asociados a los embeddings.
    :type chunks: list[str]
    :param collection_name: Nombre de la colección de Milvus donde se insertarán
                            los datos.
    :type collection_name: str
    :return: Número total de registros insertados en la colección.
    :rtype: int
    :raises ValueError: Si el número de fragmentos y vectores no coincide.
    '''

    if len(vectors) != len(chunks):
        raise ValueError("Vectors y chunks deben tener la misma longitud")

    rows = []

    for text, vector in zip(chunks, vectors):
        rows.append({
            "text": text,
            "vector": vector
        })

    try:
        milvus_client = get_milvus()
    except Exception as e:
        print("ERROR CONECTANDO A LA BASE DE DATOS:", e)

    try:
        milvus_client.insert(
        collection_name=collection_name,
        data=rows
        )

        milvus_client.flush(collection_name)

    except Exception as e:
        print("ERROR INGESTANDO EN LA MILVUS: ",e)

    return len(rows)