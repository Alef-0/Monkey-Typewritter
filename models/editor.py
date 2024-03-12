from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field, validator
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from langchain_google_genai import GoogleGenerativeAI
import constants as cnsts
from monkey import sys

class Timeline_json(BaseModel):
    summary : str = Field(description="A brief summary of what happened so far.")
    timeline : list[str] = Field(description="A list with the events that define the narrative, in cronological order. Keep it in short phrases, to maintain simplicity.")

base_prompt = """
You are going to read a text and create a list with the events in cronological order and a brief summary of what happened thus far.
It's necessary that you keep all of them as concise as possible.
Answer using the following formating rules:
""".strip()

parser = PydanticOutputParser(pydantic_object=Timeline_json)

prompt = PromptTemplate(
    template="{base_prompt}"+"\n{format_instructions}\nHere's the Text:\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions(), "base_prompt" : base_prompt},
)

def call_editor(entrada : str):
    response = sys.model.generate_content(prompt.format(query=entrada))
    return parser.parse(response.text)
