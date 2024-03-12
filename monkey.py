import constants as cnst
import google.generativeai as genai

# System Variables
class Variables:
    def __init__(self):
        self.chat = None
        self.model = None

    # Principais
    def create(self, key):
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel(
            model_name=cnst.GEMINI,
            generation_config=cnst.GENERATION_GEMINI,
            safety_settings=cnst.SAFETY_GEMINI
        )
        try:
            response = self.model.generate_content("Are you connected? Give me a simple yes or no.")
            print(response.text)
            self.chat = self.model.start_chat(history=[])
            return True
        except Exception as e:
            print("Ocorreu um erro")
            print(e)
            return False

sys = Variables()