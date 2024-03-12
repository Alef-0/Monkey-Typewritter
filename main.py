import google.generativeai as genai
import constants as cnsts


genai.configure(api_key=cnsts.GEMINI_KEY)
model_g = genai.GenerativeModel(
                model_name=cnsts.GEMINI,
                safety_settings = cnsts.SAFETY_GEMINI,
                generation_config=cnsts.GENERATION_GEMINI
            ); 

response = model_g.generate_content("Hello")
print(response.text)