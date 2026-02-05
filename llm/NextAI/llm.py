from utils.config import NEXTAI_API, NEXTAI_MODEL, NEXTAI_URL, NEXTAI_USER

import uuid
import requests


def define_payload(prompt_usuario: str, prompt_sistema:str = None, id_chat: str =None)-> dict[str] :
    '''
    Método para la defición de la carga que le pasamos a la petición de NextAI con las credenciales y parámetros de la petición
    
    :param prompt_usuario: Prompt del usuario con la petición indicada
    :type prompt_usuario: str
    :param prompt_sistema: Prompt del sistema que agrega instrucciones para que el modelo realice la petición del usuario
    :type prompt_sistema: str
    :param id_chat: ID del chat
    :type id_chat: str
    :return: el Header y el Body de la petición a NextAI
    :rtype: dict[str, Any]
    '''

    data = {
    "model": NEXTAI_MODEL,
    "uuid": generate_uuid() if id_chat==None else id_chat,
    "message": {
        "role": "user",
        "content": prompt_usuario
    },
    "prompt": prompt_sistema, 
    "temperature": 0,
    "language": "es",
    "user": NEXTAI_USER
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": NEXTAI_API
    }

    return data, headers


def generate_uuid()-> str:
    '''
    Genera automáticamente un uuid.
    '''

    return str(uuid.uuid4())

def llm_call(prompt_usuario: str, prompt_sistema:str = None, id_chat: str =None)->dict:
    '''
    Método de llamada de LLM para poder usar los modelos de NextAI
    
    :param prompt_usuario: Prompt del usuario con la petición indicada
    :type prompt_usuario: str
    :param prompt_sistema: Prompt del sistema que agrega instrucciones para que el modelo realice la petición del usuario
    :type prompt_sistema: str
    :param id_chat: ID del chat
    :type id_chat: str
    '''

    data, headers = define_payload(prompt_usuario=prompt_usuario, prompt_sistema=prompt_sistema, id_chat=id_chat)
    try:
        with requests.post(NEXTAI_URL, json=data, headers=headers, stream=True) as response:
            response.raise_for_status() 

            return response.json()["content"]
    except requests.exceptions.RequestException as e:
        print("ERROR EN LA SOLICITUD: ", e)
