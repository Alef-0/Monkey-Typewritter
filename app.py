import gradio as gr
import libs.Old_monkey as mk
from time import sleep
from monkey import sys
import constants as cnst

from components.chat import chat
from components.create import create

# demo = gr.TabbedInterface([params(), chat(), stories()], ["Params", "Chat", "Create"])

def creating_chat(choice, key):
        sys.change_key(key)
        sys.create_new_chat(choice)
        if sys.chat != None:
            return gr.Button("VALID KEY"), gr.Tabs(visible=True), gr.Tabs(visible=False)
        else: return gr.Button("Try again"), gr.Tabs(), gr.Tabs()

def automatic():
    if (cnst.GEMINI_KEY): return creating_chat("Gemini", cnst.GEMINI_KEY)
    else: return gr.Button("See if it's valid"), gr.Tabs(), gr.Tabs()
        
with gr.Blocks() as demo:
    with gr.Tabs(visible=False) as main_tabs:
        with gr.Tab("Create",id=1):     create()
        with gr.Tab("Chat", id=99):      chat()
        # Talvez não utilize mais essas
        # with gr.Tab("Teste", id=2):  params()
        # with gr.Tab("Create", id=3):  stories()
    
    with gr.Tabs() as key_tab:
        with gr.Tab("KEY", id = 99):
            gr.Markdown("# Coloque uma chave válida para continuar")
            with gr.Row():
                key = gr.Textbox(placeholder="API Key", scale=4, show_label=False, container=False)
                choice = gr.Radio(choices=["Gemini", "GPT"], scale=1, container=False, interactive=True, value="Gemini")
                test = gr.Button("See if it's valid", scale=1)

    test.click(creating_chat, inputs=[choice, key], outputs=[test, main_tabs, key_tab], show_progress=True)
    demo.load(automatic, outputs=[test, main_tabs, key_tab], show_progress=True)
    
            
demo.launch()

