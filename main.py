from pipeline.rag_pipeline import rag_system_call
from ingest.process import generate_text_from_json
from mongo.services import get_games
from llm.nextai.llm import llm_call


if __name__ == "__main__":
    response= rag_system_call(pregunta="¿De donde es el protagonista?")
    print(response)




    # juegos = get_games()
    # # print (juegos)
    # texto_final = generate_text_from_json(json_package=juegos)

    # print(texto_final)

    
    # response = llm_call(prompt_usuario="Esto funciona correctamente? responde solo con si o no")
    # print(response)

