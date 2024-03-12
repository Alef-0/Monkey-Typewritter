from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field, validator
from monkey import sys

class Narrator_json(BaseModel):
    narrative : str = Field("The story as written. It should be written as the first chapter of a bigger story.")
    title : str = Field("The title of the chapter.")
    genre : str = Field("The genre of the story")

base_prompt = """
You are a great writer who is trying to help a user to create a story. The user will pass you details about the narrative, and your job will be to create the start of the first chapter including characters and dialogues. 
Don't write a chapter title, also don't finish the story, leave it with an open ending so the user can write the rest.
Write a long, drawn-out story. Be descriptive, fluid, and follow the context provided. 
Please write as much as you possibly can, it's of vital importance that we get as much text as possible, and the story should be interesting and charming.
Here are the details of the story:
""".strip()

parser = PydanticOutputParser(pydantic_object=Narrator_json)

prompt = PromptTemplate(
    template="{prompt}" + "\n{input}",
    input_variables = ["input"],
    partial_variables = {"prompt": base_prompt}
)

def call_narrator(entrada : str, stream : bool):
    response = sys.model.generate_content(prompt.format(input=entrada), stream=stream)
    return response
