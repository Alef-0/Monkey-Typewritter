import gradio as gr
from time import sleep
from monkey import sys
import constants as cnts

# Definindo funções
def talk(message : str, history : list[list[str,str]]):
    response = sys.chat.send_message(message, stream=True)
    history.append([message, ""])
    for chunk in response:
        for i in chunk.text:
            sleep(0.005)
            history[-1][1] += i
            yield history
    yield history

def clear_history(history : list[list[str,str]]):
    nova = "You find a monkey in you room and a letter directed to you:\n\"" + sys.first_message + "\"\n You can talk to them now."
    history = [[nova, None]]
    sys.chat.history = sys.first_history
    return history

def introducao(history : list[list[str,str]]):
    nova = "You find a monkey in you room and a letter directed to you:\n\"" + sys.first_message + "\"\n You can talk to them now."
    history = [[nova, None]]
    return history

# Definindo Layout
def chat():
    with gr.Blocks() as chat_main:
        chatbot = gr.Chatbot(layout="bubble", value=[], 
                             show_label=False, show_copy_button=True, scale=3, height=400,
                             avatar_images=(None, "logofinal.png")) 
        with gr.Row() as chat_place:
            question = gr.Textbox(placeholder="What are you asking? [Press Shift + Enter to send]", lines=7, show_label=False, scale=3)
            with gr.Column(scale=2):
                gr.Markdown("## [O modelo possui memória limitada]")
                send = gr.Button("Enviar pergunta.")
                restart = gr.Button("Reiniciar a conversa.")
        # Eventos
        question.submit(talk, [question, chatbot], [chatbot])
        question.submit(lambda _: "",inputs=[question], outputs=[question]) # Limpar questão
        send.click(lambda _: "", inputs=[question], outputs=[question])
        send.click(talk, [question, chatbot], [chatbot])

        restart.click(clear_history, [chatbot], [chatbot])
        chat_main.load(introducao, chatbot, chatbot)

    return chat_main
