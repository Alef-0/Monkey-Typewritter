PARSER_HISTORY = """
Create a summary of a story created using the user prompt. It should focus on the beggining, but leave the ending open, if no title is provided give it a title as well, and put at the beggining of the text.
""".strip()

PARSER_TIMELINE = """
Create in the form of a list a series of events important to the story created.
""".strip()

PARSER_SHEETS = """
Give in the form of a list, the names of the important characters of that story, along with their important characteristics, including personality and appearance. Every list should start with the name of the character, followed by thier traits in a form of a list. If there is a notable trait for background characters, it should stay as the last list, with 'others' as their name, but only if necessary.
""".strip()

PROMPT_TEMPLATE = """
Create a story with the following characteristics, based around the user prompt.
""".strip()