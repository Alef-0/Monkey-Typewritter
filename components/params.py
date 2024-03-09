import gradio as gr
from monkey import sys
import libs.prompts_templates as pt

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
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
                'You are a book writer. Your task is to write stories in a vivid and intriguing language. ' +
                "It's a {genre} story, and it has the following title: {title}. Please keep as close to these information as possible. " +
                "The details about this story are the following: {input}\n\n" +
                # 'The title of the book is {title}. The story takes place in {location}. The tone of the story is {tone}. The pacing should be {pacing}'
                "Follow the following format: \n{format_instructions}\n{input}\n",
            input_variables=['input', 'genre', 'title'],
            partial_variables={'format_instructions': self.parser.get_format_instructions()},
        )
        # print(self.parser.get_format_instructions())

    def buildChain(self):
        self.chain = self.prompt | sys.chat | StrOutputParser()

ps = ParamsStory()

def generate(input=str, genre=str, title=str):
    print(input, genre)
    if sys.chat == None: return "KEY INVALIDA", '', ''
    else:
        ps.buildChain()
        resposta = ps.chain.invoke({"input": input,"genre": genre, "title": title})
        dicionario : Prompt_Master = ps.parser.parse(resposta)
        return dicionario.history, dicionario.sheets, dicionario.timeline

def params():
    with gr.Blocks() as window_params_story:
        gr.Markdown("""### Digite os detalhes da sua história que ele irá cria-la, e separar os detalhes da timeline e dos personagens. No futuro também adicionaremos fazer isso com texto, e maneira incremental de fazer os prompts.""")
        with gr.Row() as params:
            genre = gr.Textbox(label="Gênero")
            title = gr.Textbox(label="Título")

        details = gr.Textbox(label="Detalhes gerais", lines=5)
        btn = gr.Button("Gerar")
        
        gr.Markdown("# Resultado")
        historia = gr.Textbox(label="Narrativa", placeholder="Esperando o prompt", lines=5, interactive=False, autoscroll=True)
        with gr.Row() as saidas:
            personagens = gr.JSON(label="Personagens")
            timeline = gr.JSON(label="Timeline")

        btn.click(fn=generate, inputs=[details, genre, title], outputs=[historia, personagens, timeline], scroll_to_output=True)
        details.submit(fn=generate, inputs=[details, genre, title], outputs=[historia, personagens, timeline], scroll_to_output=True)
    return window_params_story
