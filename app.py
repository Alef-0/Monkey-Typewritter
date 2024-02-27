import gradio as gr
import libs.monkey as mk
from time import sleep
from site_var import sys

from components.chat import chat_main
from components.stories import windows_stories


# Lançando o site
demo = gr.TabbedInterface([chat_main, windows_stories], ["Chat", "Create"])
demo.launch()
