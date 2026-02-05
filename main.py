from chat.chatbot import build_chatbot_chain


if __name__ == "__main__":
    engine=True
    print("CONSOLA DE CHATBOT")

    chatbot = build_chatbot_chain()
    respuesta = chatbot.invoke("Dime 3 juegos de accion para jugar este verano")
    print(respuesta)