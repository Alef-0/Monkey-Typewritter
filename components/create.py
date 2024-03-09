import gradio as gr
import constants as cnsts
from langchain.output_parsers import PydanticOutputParser
import models.narrator as nar
import models.director as dir
import models.editor as edi
import models.user_save as usr
from time import sleep


def redo(historia):
    yield {"STILL MAKING IT"}, {"STILL MAKING IT"}, gr.File(visible=False)
    personagens : dir.Sheets_Json = dir.chain.call_chain(historia)
    yield personagens.dict(), {"STILL MAKING IT"}, gr.File(visible=False)
    timeline : edi.Timeline_json = edi.chain.call_chain(historia)
    
    res_path = usr.create_json(historia, personagens.dict(), timeline.dict())
    yield personagens.dict(), timeline.dict(), gr.File(label = "Saida como arquivo", visible=True, value = res_path, show_label=True)

def criar(prompt : str):        
    # Criar saida  da historia
    chain = nar.create_chain()
    stream = chain.stream({'input': prompt})
    historia = ""
    for parts in stream:
        for char in parts:
            historia += char
            sleep(0.001)
            yield historia, {"STILL MAKING IT"}, {"STILL MAKING IT"}, gr.File(visible=False)
    
    while True:
        try: personagens : dir.Sheets_Json = dir.call_chain(historia); break
        except: print("Falhou a criação de personagens")
    yield historia, personagens.dict(), {"STILL MAKING IT"}, gr.File(visible=False),
    while True:
        try: timeline : edi.Timeline_json = edi.call_chain(historia);break
        except: print("Falhou a criação de timeline")
    res_path = usr.create_json(historia, personagens.dict(), timeline.dict())
    
    yield (
        historia, personagens.dict(), timeline.dict(), 
        gr.File(label = "Arquivo atual",visible=True, value= [res_path], show_label=True),
    )


def create():
    with gr.Blocks() as create_main:
        gr.Markdown("""### Digite os detalhes da sua história que ele irá cria-la, e separar os detalhes da timeline e dos personagens. No futuro também adicionaremos fazer isso com texto, e maneira incremental de fazer os prompts.""")
        entrada = gr.Textbox(lines=3, placeholder="Press Shift+Enter to send", scale= 10, label="Escreva detalhes da sua historia")
        gerar = gr.Button("Gerar")

        gr.Markdown("# Se não der certo, tente novamente, as vezes da erro.")
        download = gr.File(visible=False)
        historia = gr.Textbox(label="Narrator", show_copy_button=True, max_lines=10, lines=5, placeholder="You can also type your history here.", interactive=True)
        retry = gr.Button("Retry")
        with gr.Row() as saidas:
            personagens = gr.JSON(label="Personagens")
            timeline = gr.JSON(label="Timeline")

        entrada.submit(criar, [entrada], [historia, personagens, timeline, download])
        gerar.click(criar, [entrada], [historia, personagens, timeline, download])
        retry.click(redo, [historia], [personagens, timeline, download])

    return create_main  