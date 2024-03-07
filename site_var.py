import libs.monkey as mk
from enum import Enum
import libs.prompts_templates as pt

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field, validator
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class Prompt_Master(BaseModel):
    history : str = Field(description=pt.PARSER_HISTORY)
    timeline : list[str] = Field(description=pt.PARSER_TIMELINE)
    sheets : list[list[str]] = Field(description= pt.PARSER_SHEETS)


# System Variables
class Variables:
    def __init__(self):
        self.chat = None
        self.speed_up = False
        self.key = ""

        self.parser = PydanticOutputParser(pydantic_object=Prompt_Master)

        self.prompt = PromptTemplate(
            template = pt.PROMPT_TEMPLATE + "\n{format_instructions}\n{input}\n",
            input_variables=['input'],
            partial_variables={'format_instructions': self.parser.get_format_instructions()},
        )
        # print(self.parser.get_format_instructions())
    
    def create_prompt(self):
        if self.chat != None:
            self.chain = ({'input': RunnablePassthrough()} | self.prompt | self.chat | StrOutputParser())

    def change_speed(self, s):
        self.speed_up = s; print("Speed changed")
    def change_key(self, k):
        self.key = k; print("Key changed")

    # Principais
    def create_new_chat(self, model):
        self.chat = mk.create_model(model, self.key)

sys = Variables()