import os
from dotenv import load_dotenv
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory
load_dotenv()

GEMINI_KEY = os.getenv('GEMINI_KEY') 

SAFETY_GEMINI = { 
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}

GENERATION_GEMINI = {
  "temperature": 0.9,
  # Maximum possible, probably overshooting. 2048 - 8192
  "max_output_tokens": 8192, 
}

GEMINI = "gemini-1.0-pro-latest"
GEMINI_VISION = "gemini-1.0-pro-vision-latest"

#Precisa de um arquivo .env
