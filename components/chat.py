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
            sleep(0.05)
            history[-1][1] += i
            yield history
    yield history

def clear_history(history : list[list[str,str]]):
    history = []
    sys.chat.history = []
    return history

# Definindo Layout
def chat():
    with gr.Blocks() as chat_main:
        chatbot = gr.Chatbot(layout="bubble", value=[], show_label=False, show_copy_button=True, scale=3, height=400) 
        with gr.Row() as chat_place:
            question = gr.Textbox(placeholder="What are you asking? [Press Shift + Enter to send]", lines=6, show_label=False, scale=3)
            with gr.Column(scale=2):
                gr.Markdown("## [O modelo possui memória limitada]")
                send = gr.Button("Send Question")
                restart = gr.Button("Restart Conversation")
        # Eventos
        question.submit(talk, [question, chatbot], [chatbot])
        question.submit(lambda _: "",inputs=[question], outputs=[question]) # Limpar questão
        send.click(lambda _: "", inputs=[question], outputs=[question])
        send.click(talk, [question, chatbot], [chatbot])

        restart.click(clear_history, [chatbot], [chatbot])
        
    return chat_main
