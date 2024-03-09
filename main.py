from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import OpenAI,ChatOpenAI
import constants as cnsts

model_g = GoogleGenerativeAI(
                model=cnsts.GEMINI,
                max_output_tokens=8192,
                google_api_key = cnsts.GEMINI_KEY,
                safety_settings = cnsts.SAFETY_GEMINI,
                convert_system_message_to_human=True
            ); 

model = ChatOpenAI(api_key = cnsts.GPT_KEY)

response = model_g.invoke("Hello")
print(response)