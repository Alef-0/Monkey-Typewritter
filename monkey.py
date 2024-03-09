from enum import Enum
import libs.prompts_templates as pt
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import OpenAI,ChatOpenAI
import constants as cnsts

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
        self.master_prompt = PromptTemplate(
            template = pt.PROMPT_TEMPLATE + "\n{format_instructions}\n{input}\n",
            input_variables=['input'],
            partial_variables={'format_instructions': self.parser.get_format_instructions()},
        )    
        
    def create_chain(self):
        if self.chat != None:
            self.chain = ({'input': RunnablePassthrough()} | self.master_prompt | self.chat | StrOutputParser())
    
    def change_speed(self, s):
        self.speed_up = s; print("Speed changed")
    
    def change_key(self, k):
        self.key = k; print("Key changed")

    # Principais
    def create_new_chat(self, type):
        print("Tentando criar chat")
        if (type == "Gemini"): 
            model = GoogleGenerativeAI(
                model=cnsts.GEMINI,
                max_output_tokens=8192,
                google_api_key = self.key,
                safety_settings = cnsts.SAFETY_GEMINI,
                convert_system_message_to_human=True
            ); 
            print("Trying Gemini")
        else: model = ChatOpenAI(api_key = self.key); print("Trying GPT")

        try: 
            response  = model.invoke("Are you connected? Yes or no. Short answer")
            print(response)
            self.chat = model
            self.create_chain()
        except: 
            print("Key Error")

sys = Variables()