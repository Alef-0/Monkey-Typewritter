import gradio as gr
from monkey import sys
import constants as cnst

from components.chat import chat
from components.create import create
from components.edit import edit

QUANTITY = 3

def creating_chat(key):
        if sys.create(key):
            return [gr.Button("VALID KEY")] + [gr.Tabs(visible=True)] * QUANTITY
        else: return [gr.Button("Try again")] + [gr.Tab(visible=False)] * QUANTITY

def automatic():
    if (cnst.GEMINI_KEY): print("Env detected"); return creating_chat(cnst.GEMINI_KEY)
    else: return [gr.Button("Try Again")] + [gr.Tab(visible=False)] * QUANTITY
        
with gr.Blocks() as demo:
    with gr.Tabs() as main_tabs:
        with gr.Tab("Boas Vindas", id=1) as key_tab:
            gr.Markdown("# Coloque uma chave válida para continuar, pegue sua na [Google AI Studio](https://aistudio.google.com/app/apikey)")
            with gr.Row():
                key = gr.Textbox(placeholder="API Key", scale=4, show_label=False, container=False)
                test = gr.Button("See if it's valid", scale=1)
        with gr.Tab("Criar História",id=2, visible=False) as h_tab:    create()
        with gr.Tab("Editar História", id=3, visible=False) as e_tab:     edit()
        with gr.Tab("Assistente", id=99, visible=False) as c_tab:    chat()
    
    all_tabs = [h_tab, e_tab, c_tab]

    test.click(creating_chat, inputs=[key], outputs=[test, *all_tabs], show_progress=True)
    demo.load(automatic, outputs=[test, *all_tabs], show_progress=True)
    
            
demo.launch()

