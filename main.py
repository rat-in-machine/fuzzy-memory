from pipeline.rag_pipeline import rag_system_call
from ingest.process import generate_text_from_json, create_chunks, vector_generator, ingest_db
from mongo.services import get_games
from llm_rag.NextAI.llm import llm_call
from utils.config import MILVUS_COLLECTION_NAME


def realizar_ingesta():
    juegos = get_games()
    print(juegos)
    texto_final = generate_text_from_json(json_package=juegos)
    print(texto_final)

    chunks= create_chunks(text=texto_final)
    vectors = vector_generator(chunks=chunks)
    ingest_db(vectors=vectors, chunks=chunks, collection_name=MILVUS_COLLECTION_NAME)

def preguntar_rag(pregunta: str, collection: str = MILVUS_COLLECTION_NAME):
    response= rag_system_call(pregunta=pregunta, collection_name=collection)
    print(response)

def probar_modelo(pregunta: str):
    response = llm_call(prompt_usuario=pregunta)
    print(response)



if __name__ == "__main__":
    engine=True
    print("CONSOLA DE RAG")
    while engine:
        seleccion = int(input("indique la opcion a realizar para pruebas de RAG: \n1) Probar modelo.\n2) Preguntar con Rag.\n3) Ingestar datos de prueba en Milvus (NO HACER SI YA HAY DATOS) \n4) Salir.\n>"))
        match seleccion:
            case 1:
                pregunta = str(input("Indique la pregunta para el modelo: \n>"))
                probar_modelo(pregunta=probar_modelo)
            case 2:
                pregunta= str(input("Indique la pregunta a realizar usando los datos de la Milvus:\n>"))
                preguntar_rag(pregunta=pregunta)
            case 3:
                print("Realizando ingesta....")
                realizar_ingesta()
                print("Ingesta terminada.")
            case 4:
                print("Hasta luego.")
                exit()
            case _:
                print("Lo siento, no es una opción válida. Intente de nuevo.")

