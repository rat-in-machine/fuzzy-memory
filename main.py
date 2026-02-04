from llm.openai.petition import rag_system_call


if __name__ == "__main__":
    response= rag_system_call(pregunta="¿De donde es el protagonista de la historia?")
    print(response)
