import gradio as gr

import models.narrator as nar
import models.director as dir
import models.editor as edi
from models.creator import call_creator
from models.user_save import tags

import models.user_save as usr
import constants as cnst
from time import sleep
from monkey import sys
import json

sys.create(cnst.GEMINI_KEY)

def redo(historia : str):    
    if not historia.strip(): 
        yield {"Nada a ler"},{"Nada a ler"}, gr.File()
    else:
        while True:
            try: personagens : dir.Sheets_Json = dir.call_director(historia); break
            except: print("Falhou a criação de personagens")
        yield personagens.dict(), {"Tentando fazer"}, gr.File(visible=False),
        while True:
            try: timeline : edi.Timeline_json = edi.call_editor(historia);break
            except: print("Falhou a criação de timeline")
        res_path = usr.create_json(historia, personagens.dict(), timeline.dict())
        yield (
        personagens.dict(), timeline.dict(), 
        gr.File(label = "Arquivo atual",visible=True, value= [res_path], show_label=True),
    )

def criar(prompt : str):        
    # Criar saida  da historia
    yield cnst.AVISO, {"Tentando fazer"}, {"Tentando fazer"}, gr.File(visible=False)
    while True:
        try:
            stream = nar.call_narrator(prompt, False)
            historia = stream.text
            break
        except: print("Deu algo errado na criação da narrativa.")
    yield historia, {"Tentando fazer"}, {"Tentando fazer"}, gr.File(visible=False)
            
    while True:
        try: personagens : dir.Sheets_Json = dir.call_director(historia); break
        except: print("Falhou a criação de personagens")
    yield historia, personagens.dict(), {"Tentando fazer"}, gr.File(visible=False),
    
    while True:
        try: timeline : edi.Timeline_json = edi.call_editor(historia);break
        except: print("Falhou a criação de timeline")
    
    res_path = usr.create_json(historia, personagens.dict(), timeline.dict())
    yield (
        historia, personagens.dict(), timeline.dict(), 
        gr.File(label = "Arquivo atual",visible=True, value= [res_path], show_label=True),
    )

def upar(local : str):
    atual = {}
    with open(local, "r") as f:
        atual = json.loads(f.read())
    return atual[tags.chars], atual[tags.time]

def recriar(personagens, timeline):
    yield cnst.AVISO
    response = call_creator(personagens, timeline)
    yield response.text

def create():
    with gr.Blocks() as create_main:
        gr.Markdown("""### Digite os detalhes da sua história""")
        gr.Markdown("""
        Após criar a história iremos separar os detalhes da timeline e dos personagens. 
        Aqui é apenas para criar o primeiro capítulo, depois você precisará criar a continuação.
        """.strip())
        entrada = gr.Textbox(lines=3, placeholder="Aperte Shift+Enter para enviar", scale= 10, label="Escreva detalhes da sua historia")
        gerar = gr.Button("Gerar história.")

        gr.Markdown("# Se não der certo, tente novamente, as vezes da erro.")
        download = gr.File(visible=False)
        historia = gr.Textbox(label="Narrator", show_copy_button=True, max_lines=10, lines=5, placeholder="Você também pode digitar sua história aqui.", interactive=True)
        with gr.Row():
            retry = gr.Button("Gerar Caracteristicas ⬇️.")
            upload = gr.UploadButton("Fazer upload de uma historia")
            recreate = gr.Button("Gerar uma nova historia ⬆️")
        with gr.Row() as saidas:
            personagens = gr.JSON(label="Personagens")
            timeline = gr.JSON(label="Timeline")

        entrada.submit(criar, [entrada], [historia, personagens, timeline, download])
        gerar.click(criar, [entrada], [historia, personagens, timeline, download])
        retry.click(redo, [historia], [personagens, timeline, download])
        upload.upload(upar, [upload], [personagens, timeline])
        recreate.click(recriar, [personagens, timeline], [historia])

    return create_main