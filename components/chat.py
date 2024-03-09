import gradio as gr
import libs.Old_monkey as mk
from time import sleep
from monkey import sys
import constants as cnts

# Definindo funções
def talk(message : str, history : list[list[str,str]]):
    response = sys.chat.stream(message)
    history.append([message, ""])
    for chunk in response:
        if sys.speed_up:
            history[-1][1] += chunk
            yield history
        else:
            for i in range(len(chunk)):
                sleep(0.005)
                history[-1][1] += chunk[i]
                yield history
    yield history

def validate(new_key : str, choice : str, chatbot : list[list[str,str]]):
    new_key = new_key.strip()
    print("Choice = ", choice)
    sys.change_key(new_key)
    sys.create_new_chat(choice)
    
    if sys.chat != None: 
        # sys.create_prompt()
        return (gr.Button(visible=False), 
            gr.Chatbot(layout="bubble", value=[], show_label=False, show_copy_button=True, scale=3, height=400), 
            gr.Accordion(visible=False), gr.Row(visible=True))
    else: 
        return (gr.Button(value="Invalid Key"), chatbot, gr.Accordion(label="Gemini Key", open=True), gr.Row(visible=False))

def see_if_key(choice, chatbot):
    print("Entrou aqui")
    if cnts.GEMINI_KEY != None: return validate(cnts.GEMINI_KEY, choice, chatbot)

# Definindo Layout
def chat():
    with gr.Blocks() as chat_main:
        chatbot = gr.Chatbot(layout="bubble", value=[], show_label=False, show_copy_button=True, scale=3, height=400) 
        with gr.Row() as chat_place:
            question = gr.Textbox(placeholder="What are you asking? [Press Shift + Enter to send]", lines=4, show_label=False, scale=3)
            with gr.Column():
                gr.Markdown("## [O modelo não possui memória]",)
                speed = gr.Checkbox(label="Speed Up", info="This will make the chat stop slowly printing", scale=4)
        
        # Eventos
        # @clear.click(outputs=[question, chatbot]) #Essa é uma forma direta
        # @choice.change(inputs=[choice])
        question.submit(talk, [question, chatbot], [chatbot])
        question.submit(lambda _: "", [question], [question])
        speed.change(fn = sys.change_speed, inputs=[speed])
        
    return chat_main
