import google.generativeai as genai
import libs.constants as cnts

def create_model(api_key = cnts.GEMINI_KEY):
    genai.configure(api_key = api_key)
    model = genai.GenerativeModel(
        cnts.GEMINI, cnts.SAFETY_SETTINGS, cnts.GENERATION_CONFIG
    )
    # Testar se e valida
    try:
        response = model.generate_content(["Are you valid?"])
        print(response)
        return model
    except:
        print("Invalid key")
        return None

def create_chat(model : genai.GenerativeModel):
    chat = model.start_chat(history=[])
    return chat