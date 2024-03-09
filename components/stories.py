import gradio as gr
import constants as cnsts
from monkey import sys, Prompt_Master

def criar(prompt : str):
    resposta = sys.chain.invoke(prompt)
    dicionario : Prompt_Master = sys.parser.parse(resposta)
    return dicionario.history, dicionario.sheets, dicionario.timeline
        
def stories():
    with gr.Blocks() as windows_stories:
        gr.Markdown("""### Digite os detalhes da sua história que ele irá cria-la, e separar os detalhes da timeline e dos personagens. No futuro também adicionaremos fazer isso com texto, e maneira incremental de fazer os prompts.""")
        entrada = gr.Textbox(lines=3, placeholder="Press Shift+Enter to send")

        gr.Markdown("# Resultado")

        historia = gr.Textbox(label="Narrativa", placeholder="Esperando o prompt", lines=5, interactive=False, autoscroll=True)
        with gr.Row() as saidas:
            personagens = gr.JSON(label="Personagens")
            timeline = gr.JSON(label="Timeline")

        entrada.submit(criar, [entrada], [historia, personagens, timeline])
    
    return windows_stories
    