import gradio as gr
import libs.monkey as mk
from time import sleep
from site_var import sys

from components.chat import chat_main
from components.stories import windows_stories
from components.params import window_params_story


# Lançando o site
demo = gr.TabbedInterface([window_params_story, chat_main, windows_stories], ["Params", "Chat", "Create"])
demo.launch()
