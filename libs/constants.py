import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_KEY = os.getenv('GEMINI_KEY') #Precisa de um arquivo .env
GEMINI = 'gemini-pro'
GEMINI_VISION = 'gemini-pro-vision'

GENERATION_CONFIG = {
                    'candidate_count': 1, # Não mudar quantidade, da um erro
                    'temperature': 1.0
                    }
SAFETY_SETTINGS = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

