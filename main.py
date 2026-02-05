from pipeline.rag_pipeline import rag_system_call
from ingest.process import generate_text_from_json, create_chunks, vector_generator, ingest_db
from mongo.services import get_games
from llm.NextAI.llm import llm_call


if __name__ == "__main__":
    response= rag_system_call(pregunta="Dime un juego para jugar que sea de aventuras", collection_name="Pruebas_Juegos")
    print(response)




    # juegos = get_games()
    # # print (juegos)
    # texto_final = generate_text_from_json(json_package=juegos)
    # print(texto_final)

    # chunks= create_chunks(text=texto_final)
    # vectors = vector_generator(chunks=chunks)
    # ingest_db(vectors=vectors, chunks=chunks, collection_name="Pruebas_Juegos")

    
    # response = llm_call(prompt_usuario="Esto funciona correctamente? responde solo con si o no")
    # print(response)

