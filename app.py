import gradio as gr
from monkey import sys
import constants as cnst

from components.chat import chat
from components.create import create


def creating_chat(key):
        if sys.create(key):
            return gr.Button("VALID KEY"), gr.Tabs(visible=True), gr.Tabs(visible=False)
        else: return gr.Button("Try again"), gr.Tabs(), gr.Tabs()

def automatic():
    if (cnst.GEMINI_KEY): print("Env detected"); return creating_chat(cnst.GEMINI_KEY)
    else: return gr.Button("Try Again"), gr.Tabs(), gr.Tabs()
        
with gr.Blocks() as demo:
    with gr.Tabs(visible=False) as main_tabs:
        with gr.Tab("Create",id=1):     create()
        with gr.Tab("Chat", id=99):      chat()
    
    with gr.Tabs() as key_tab:
        with gr.Tab("KEY", id = 99):
            gr.Markdown("# Coloque uma chave válida para continuar, pegue sua na [Google AI Studio](https://aistudio.google.com/app/apikey)")
            with gr.Row():
                key = gr.Textbox(placeholder="API Key", scale=4, show_label=False, container=False)
                test = gr.Button("See if it's valid", scale=1)

    test.click(creating_chat, inputs=[key], outputs=[test, main_tabs, key_tab], show_progress=True)
    demo.load(automatic, outputs=[test, main_tabs, key_tab], show_progress=True)
    
            
demo.launch()

