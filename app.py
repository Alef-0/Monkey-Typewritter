import gradio as gr
import libs.monkey as mk
from time import sleep
from site_var import sys

from components.chat import chat_main


# Lançando o site
demo = gr.TabbedInterface([chat_main],['Chat'])
demo.launch()
