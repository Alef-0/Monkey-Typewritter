import libs.constants as cnsts
from site_var import ModelType
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import OpenAI,ChatOpenAI

def create_model(type : ModelType, api_key = cnsts.GEMINI_KEY):    
    if (type == ModelType.Gemini): 
        model = GoogleGenerativeAI(
            model=cnsts.GEMINI,
            max_output_tokens=8192,
            google_api_key = api_key,
            safety_settings = cnsts.SAFETY_GEMINI,
            convert_system_message_to_human=True
        ); print("Trying Gemini")
    else: model = ChatOpenAI(api_key=api_key); print("Trying GPT")

    try: 
        response  = model.invoke("Are you connected? Yes or no. Short answer")
        print(response.strip())
        return model
    except: print("Key Error"); return None