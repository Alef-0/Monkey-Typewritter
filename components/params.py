import gradio as gr
from site_var import sys
import libs.prompts_templates as pt
from operator import itemgetter

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
# from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser


class Prompt_Master(BaseModel):
    history : str = Field(description=pt.PARSER_HISTORY)
    timeline : list[str] = Field(description=pt.PARSER_TIMELINE)
    sheets : list[list[str]] = Field(description= pt.PARSER_SHEETS)

def length_function(text):
    return len(text)


class ParamsStory:
    def __init__(self):
        self.parser = PydanticOutputParser(pydantic_object=Prompt_Master)

        self.prompt = PromptTemplate(
            template =
                'You are a book writer. Your task is to write {genre} stories in a vivid and intriguing language. ' +
                # 'The title of the book is {title}. The story takes place in {location}. The tone of the story is {tone}. The pacing should be {pacing}'
                "\n{format_instructions}\n{input}\n",
            # input_variables=['input', 'genre', 'title', 'location', 'tone', 'pacing'],
            input_variables=['input', 'genre'],
            partial_variables={'format_instructions': self.parser.get_format_instructions()},
        )

    def buildChain(self):
        self.chain = self.prompt | sys.chat | StrOutputParser()

ps = ParamsStory()

def generate(input=str, genre=str, title=str, location=str, tone=str, pacing=str):
    print(input, genre)
    if sys.chat == None: return "KEY INVALIDA", '', ''
    else:
        ps.buildChain()
        resposta = ps.chain.invoke({"input": input,"genre": genre})
        dicionario : Prompt_Master = ps.parser.parse(resposta)
        return dicionario.history, dicionario.sheets, dicionario.timeline


with gr.Blocks() as window_params_story:
    gr.Markdown("""### Digite os detalhes da sua história que ele irá cria-la, e separar os detalhes da timeline e dos personagens. No futuro também adicionaremos fazer isso com texto, e maneira incremental de fazer os prompts.""")
    with gr.Row() as params:
        genre = gr.Textbox(label="Gênero")
        title = gr.Textbox(label="Título")
        location = gr.Textbox(label="Location")
        tone = gr.Textbox(label="Tom")
        pacing = gr.Textbox(label="Ritmo")

    input = gr.Textbox(label="Detalhes gerais")

    btn = gr.Button("Gerar")

    gr.Markdown("# Resultado")

    historia = gr.Textbox(label="Narrativa", placeholder="Esperando o prompt", lines=5, interactive=False, autoscroll=True)
    with gr.Row() as saidas:
        personagens = gr.JSON(label="Personagens")
        timeline = gr.JSON(label="Timeline")

    btn.click(fn=generate, inputs=[input, genre, title, location, tone, pacing], outputs=[historia, personagens, timeline])
