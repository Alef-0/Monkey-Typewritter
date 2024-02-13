import google.generativeai as genai
import constants as cnts

def create_model():
    genai.configure(api_key=cnts.GEMINI_KEY)
    return genai.GenerativeModel(
        cnts.GEMINI, cnts.SAFETY_SETTINGS, cnts.GENERATION_CONFIG
    )

def create_chat(model : genai.GenerativeModel):
    chat = model.start_chat(history=[])
    return chat