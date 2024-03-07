import gradio as gr
import libs.monkey as mk
from time import sleep
from site_var import sys
import libs.constants as cnts

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
with gr.Blocks() as chat_main:
    chatbot = gr.Chatbot(layout="panel", show_label=False, value=[
        ("Put a valid API Key to start talking", None)
    ], show_copy_button=True, scale=3, height=400)

    with gr.Row(visible=False) as chat_place:
        question = gr.Textbox(placeholder="What are you asking? [Press Shift + Enter to send]", lines=4, show_label=False, scale=3)
        with gr.Column():
            gr.Markdown("## [O modelo não possui memória]",)
            speed = gr.Checkbox(label="Speed Up", info="This will make the chat stop slowly printing", scale=4)
    with gr.Accordion(label="API KEY", open=True) as tray_place:
        with gr.Row():
            key = gr.Textbox(placeholder="Gemini Key", scale=4, show_label=False, container=False, lines=3)
            with gr.Column():
                choice = gr.Radio(choices=["Gemini", "GPT"], scale=2, container= False, value="Gemini", label="Modelo")
                test = gr.Button("See if it's valid", scale=1)
    
    # Eventos
    # @clear.click(outputs=[question, chatbot]) #Essa é uma forma direta
    # @choice.change(inputs=[choice])
    question.submit(talk, [question, chatbot], [chatbot])
    question.submit(lambda _: "", [question], [question])
    speed.change(fn = sys.change_speed, inputs=[speed])
    
    test.click(fn = validate, inputs = [key, choice, chatbot], outputs = [test, chatbot, tray_place, chat_place], show_progress=True)
    chat_main.load(see_if_key, inputs=[choice, chatbot], outputs = [test, chatbot, tray_place, chat_place])
