from langchain_text_splitters import RecursiveCharacterTextSplitter

from milvus.connection import get_milvus
from utils.config import MODELO_EMBEDDING

def create_chunks(text:str) ->list[str]:
    '''
    Docstring for create_chunks
    
    :param text: Description
    :type text: str
    :return: Description
    :rtype: list[str]
    '''
    splitter = RecursiveCharacterTextSplitter(chunk_size=480, chunk_overlap=50)
    chunks = splitter.split_text(text=text)

    return chunks

def vector_generator(chunks: list[str])-> list[list[float]]:
    '''
    Docstring for vector_generator
    
    :param chunks: Description
    :type chunks: list[str]
    '''
    return MODELO_EMBEDDING.embed_documents(chunks)

def ingest_db(vectors: list[list[float]],chunks: list[str],collection_name: str = "Pruebas") -> int:
    """
    Inserta chunks + embeddings en Milvus usando MilvusClient.
    """

    if len(vectors) != len(chunks):
        raise ValueError("Vectors y chunks deben tener la misma longitud")

    rows = []

    for text, vector in zip(chunks, vectors):
        rows.append({
            "text": text,
            "vector": vector
        })
    milvus_client = get_milvus()
    milvus_client.insert(
        collection_name=collection_name,
        data=rows
    )

    milvus_client.flush(collection_name)

    return len(rows)