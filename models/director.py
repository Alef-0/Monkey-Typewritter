from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field, validator
from monkey import sys

appearance_description ="""
Here should only be a list of external descriptions of a character appearance. 
Like their facial features, clothes, body shape and size etc. if relevant.
If they are an animal or creature, include the species.
""".strip()
personality_description = """
Here should only be a list of elements of the personality and mannerism of a character. 
They should complete the patern "He/She/It is...": Couregeous, kind, vile, good, caring etc.
Only how they act or think, things internal to the character.
""".strip()
traits_description = """
General traits specific of this character that didn't fit other categories. 
Should complete the pattern "He/She/It...": Did this..., Had/Has this...., Overcome this...
""".strip()

class Character_Sheet(BaseModel):
    name : str = Field(description="The name of the character or group.")
    appearance : list[str] = Field(description=appearance_description)
    personality : list[str] = Field(description=personality_description)
    traits : list[str] = Field(description=traits_description)

class Sheets_Json(BaseModel):
    characters : list[Character_Sheet] = Field(description="A list of characters with their name and descriptions")

base_prompt = """
You are going to read the a text and summarize the characters of that story, their personality and appearances.
It's necessary for good results to keep them as concise as possible, with only one phrase per trait at the limit.
Answer using the following formating rules:
""".strip()

parser = PydanticOutputParser(pydantic_object=Sheets_Json)

prompt = PromptTemplate(
    template="{base_prompt}"+"\n{format_instructions}\nHere's the Text:\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions(), "base_prompt" : base_prompt},
)

def call_director(entrada : str):
    response = sys.model.generate_content(prompt.format(query=entrada))
    return parser.parse(response.text)
