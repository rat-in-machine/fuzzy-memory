from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from utils.config import OPENAI_API, OPENAI_MODEL


llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0,
    api_key=OPENAI_API
)


def llamar_llm_openai(prompt_usuario: str,prompt_sistema: Optional[str] = None,id_chat: Optional[str] = None) -> str:

    try:
        messages = []
    
        if prompt_sistema:
            messages.append(SystemMessage(content=prompt_sistema))

        messages.append(HumanMessage(content=prompt_usuario))
    except Exception as e:
        print("ERROR A LA HORA DE CONSTRUIR EL MENSAJES PARA EL MODELO DE LENGUAJE",e)

    config = {}
    if id_chat:
        config["configurable"] = {"thread_id": id_chat}

    try:
        response = llm.invoke(messages, config=config)
    except Exception as e:
        print("ERROR A LA HORA DE CREAR EL RESPONSE OPENAI: ",e)

    try:
        return response.content
    except Exception as e:
        print("ERROR A LA HORA DE CREAR EL CONTENIDO DE RESPONSE OPENAI: ",e)