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

    messages = []

    if prompt_sistema:
        messages.append(SystemMessage(content=prompt_sistema))

    messages.append(HumanMessage(content=prompt_usuario))

    config = {}
    if id_chat:
        config["configurable"] = {"thread_id": id_chat}

    response = llm.invoke(messages, config=config)
    return response.content