import constants as cnst
import google.generativeai as genai

MESSAGE_HELPER = """
You are going to chat as if you were a fictitious monkey that can talk and is a great writer.
When a user asks for tips on writing you will give sugestions and reference famous books as references.
If a user asks anything other than writing tips give them a joke response, as if a monkey would give them, but still in a formal way.
Please introduce yourself as an answer to this prompt, and talk about your capabilities.
""".strip()

# System Variables
class Variables:
    def __init__(self):
        self.chat = None
        self.model = None

    # Principais
    def create(self, key):
        genai.configure(api_key=key, 
                        transport='rest' # Isso pode ser util se for muitos normalmente
                        )
        self.model = genai.GenerativeModel(
            model_name=cnst.GEMINI,
            generation_config=cnst.GENERATION_GEMINI,
            safety_settings=cnst.SAFETY_GEMINI
        )
        try:
            response = self.model.generate_content("Are you connected? Give me a simple yes or no.")
            print(response.text)
            self.chat = self.model.start_chat(history=[])
            self.chat.send_message(MESSAGE_HELPER)
            self.first_message = self.chat.last.text
            self.first_history = self.chat.history
            # print(self.first_message)
            return True
        except Exception as e:
            print("Ocorreu um erro")
            print(e)
            return False

sys = Variables()