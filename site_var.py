import libs.monkey as mk

# System Variables
class Variables:
    def __init__(self):
        self.chat = None
        self.speed_up = False
        self.key_gemini = ""
    def change_speed(self, s):
        self.speed_up = s; print("Speed changed")
    def change_key(self, k):
        self.key_gemini = k; print("Key changed")
    def create_new_chat(self):
        model = mk.create_model(self.key_gemini)
        if model: self.chat = mk.create_chat(model)

sys = Variables()