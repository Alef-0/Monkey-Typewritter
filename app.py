import gradio as gr
from monkey import sys
import constants as cnst
from gradio.themes.utils import sizes

from components.chat import chat
from components.create import create
from components.edit import edit

QUANTITY = 3

def creating_chat(key):
        if sys.create(key):
            return [gr.Button("Chave Válida,")] + [gr.Tabs(visible=True)] * QUANTITY + [gr.Textbox(value="", visible=False)]
        else: return [gr.Button("Tente novamente")] + [gr.Tab(visible=False)] * QUANTITY + [gr.Textbox(value="", visible=False)]

def automatic():
    if (cnst.GEMINI_KEY): print("Env detected"); return creating_chat(cnst.GEMINI_KEY)
    else: return [gr.Button("Validar chave")] + [gr.Tab(visible=False)] * QUANTITY
        
with gr.Blocks(theme=gr.themes.Monochrome(text_size=sizes.text_lg), title="Monkey Typewritter") as demo:
    with gr.Tabs() as main_tabs:
        with gr.Tab("Boas Vindas", id=1) as key_tab:
            gr.Markdown("# Coloque uma chave válida para continuar, pegue sua na [Google AI Studio](https://aistudio.google.com/app/apikey)")
            with gr.Row():
                key = gr.Textbox(placeholder="API Key", scale=4, show_label=False, container=False)
                test = gr.Button("Validar chave", scale=1)
            gr.Markdown("""
# MonkeyTypewriter
> **Você entra com a ideia e o MonkeyTyperiter te ajuda com o resto.**

Cansado de encarar a tela em branco? O MonkeyTypewriter te ajuda a dar vida às suas ideias com a ajuda da inteligência artificial. Explore personagens cativantes, tramas envolventes e timelines detalhadas para impulsionar sua escrita e transformar suas ideias em histórias épicas.

**Como Funciona:** 

**1. Criação:**

Comece digitando uma breve descrição da sua história na tela de criação.
O MonkeyTypewriter irá gerar uma **narrativa mais elaborada**, incluindo:
-   **Resumo da História:**  Uma visão geral da trama.
-   **Descrição dos Personagens:**  Nomes, aparência, personalidade e traços marcantes.
-   **Timeline:**  Uma linha do tempo com os eventos chave da história.

**2. Edição:**

-   **Personalize:**  Exporte o conteúdo gerado em um arquivo .json.
-   **Aprimore:**  Faça upload do arquivo .json na tela de edição.
-   **Refinar:**  Edite todos os detalhes da história resumida, personagens e timeline.
-   **Continue:**  Gere um arquivo .json atualizado e retorne à tela de criação para continuar desenvolvendo sua história.

**Recursos Adicionais:**

-   **Assistente de Chat:**  Converse com o Monkey e receba dicas e sugestões para aprimorar sua escrita. Torne-se um Shakespeare com a ajuda da IA!

**Dicas para Começar:**

-   **Seja específico:**  Na descrição da história, forneça detalhes sobre o gênero, tema, conflito principal e personagens.
-   **Explore diferentes estilos:**  Experimente diferentes tipos de histórias e veja como a IA te ajuda a criar.
-   **Edite e refine:**  Use a tela de edição para ajustar os detalhes da história e torná-la única.
-   **Divirta-se!:**  O MonkeyTypewriter é uma ferramenta para te auxiliar na sua jornada criativa. Relaxe, explore e divirta-se!
""")
        with gr.Tab("Criar História",id=2, visible=False) as h_tab:    create()
        with gr.Tab("Editar História", id=3, visible=False) as e_tab:     edit()
        with gr.Tab("Assistente", id=99, visible=False) as c_tab:    chat()
    
    all_tabs = [h_tab, e_tab, c_tab]

    test.click(creating_chat, inputs=[key], outputs=[test, *all_tabs, key], show_progress=True)
    demo.load(automatic, outputs=[test, *all_tabs, key], show_progress=True)
    
            
demo.launch(favicon_path="favicon.ico")

