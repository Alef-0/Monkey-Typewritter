from langchain.prompts import PromptTemplate
from monkey import sys
from models.user_save import tags

base_prompt="""
You are a great writer who is trying to help a user to create a story. The user will pass you details about the narrative, and your job will be to create the start of the first chapter including characters and dialogues. 
Don't write a chapter title, also don't finish the story, leave it with an open ending so the user can write the rest.
Write a long, drawn-out story. Be descriptive, fluid, and follow the context provided. 
Please write as much as you possibly can, it's of vital importance that we get as much text as possible, and the story should be interesting and charming.
You are going to be given a summary of a history, a list with the timeline of the events, and some characters. The characters will be an object with their names, appearance, personalities and traits.
Then you will need to create a story that follows the same rules and events, and use some or all of the characters making their characteristics consistent.
""".strip()

complete_prompt="""
{base}\nHere's the Summary of what should happen in the story:{summary}
Now here are the events and the order they should be in:{timeline}
Here are the characters and their characteristics:{characters}
Now write the story following these rules.
""".strip()

prompt = PromptTemplate(
    template = complete_prompt,
    input_variables=['summary', 'timeline', 'characters'],
    partial_variables={'base':base_prompt}
)

def call_creator(characters : dict, timeline : dict):
    response = sys.model.generate_content(prompt.format(
        characters=str(characters),
        timeline=timeline[tags.time],
        summary=timeline[tags.summ]
    ))
    return response