import gradio as gr
import google.generativeai as genai
from monkey import sys

prompt = """
Pretend you are an writter and the following image is the opening scene of your book. Write some paragraphs describing the image.
Be descriptive, fluid, and flourish your words. Try not to repeat your expressions.
Be attentive to objects, expressions and people that appear interesting.
""".strip()

def generate_description(imagem):
    response = sys.vision.generate_content([prompt, imagem])
    return response.text

def art():
    with gr.Blocks() as art_main:
        gr.Markdown("# Coloque uma imagem para gerar uma escrita artística com ela.")
        
        with gr.Row():
            with gr.Column():
                imagem = gr.Image(type="pil", show_label=False)
                btn = gr.Button()
            descricao = gr.Textbox(label="Descrição da imagem.", lines=12,
                placeholder="Aqui ficará uma descrição de uma cena baseada na imagem.", interactive=True, show_copy_button=True)

        btn.click(generate_description, [imagem], [descricao])

    return art_main