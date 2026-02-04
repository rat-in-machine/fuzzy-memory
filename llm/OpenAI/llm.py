from utils.config import OPENAI_API, OPENAI_MODEL

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

from typing import Optional


llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0, api_key=OPENAI_API)

def llamar_llm_openai(prompt_usuario: str, prompt_sistema:Optional[str] = None, id_chat: Optional[str] =None)-> str:
    '''
    Método de llamada de LLM para poder usar los modelos de OpenAI
    
    :param prompt_usuario: Prompt del usuario con la petición indicada
    :type prompt_usuario: str
    :param prompt_sistema: Prompt del sistema que agrega instrucciones para que el modelo realice la petición del usuario
    :type prompt_sistema: str
    :param id_chat: ID del chat
    :type id_chat: str
    '''
    messages = []

    if prompt_sistema:
        messages.append(SystemMessage(content=prompt_sistema))
    
    messages.append(HumanMessage(content=prompt_usuario))

    config = {}

    if id_chat:
        config["configurable"] = {
            "thread_id": id_chat
        }
    
    response = llm.invoke(messages, config=config)

    return response.content