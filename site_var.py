import libs.monkey as mk
from enum import Enum

class ModelType(Enum): 
    Gemini = 1
    GPT = 2

# System Variables
class Variables:
    def __init__(self):
        self.chat = None
        self.speed_up = False
        self.key = ""
        self.model : ModelType = ModelType.Gemini

    def change_speed(self, s):
        self.speed_up = s; print("Speed changed")
    def change_key(self, k):
        self.key = k; print("Key changed")
    def change_model(self, choice):
        if choice == "Gemini": sys.model = ModelType.Gemini
        else: sys.model = ModelType.GPT
        print("Model Changed to:", sys.model)

    # Principais
    def create_new_chat(self):
        self.chat = mk.create_model(self.model, self.key)

sys = Variables()