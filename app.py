import gradio as gr
import libs.monkey as mk
from time import sleep
import site_var

sys = site_var.Variables()

# Definindo funções
def talk(message : str, history : list[list[str,str]]):
    if not sys.chat: 
        print("Entered None")
        history.append([None,"Put a valid key"])
        yield history; return; # O return para tudo
    response = sys.chat.send_message(message, stream=True)
    history.append([message, ""])
    for chunk in response:
        if sys.speed_up:
            history[-1][1] += chunk.text
            yield history
        else:
            for i in range(len(chunk.text)):
                sleep(0.005)
                history[-1][1] += chunk.text[i]
                yield history
    yield history
def delete():
    if sys.chat:
        while len(sys.chat.history): sys.chat.rewind()
    return '',[]
def validate(new_key : str, chatbot : list[list[str,str]]):
    new_key = new_key.replace(" ", "").strip()
    sys.change_key(new_key.replace(" ", ""))
    sys.create_new_chat()
    if sys.chat != None: 
        return (
            gr.Button(value= "Chat online ✅"), 
            gr.Chatbot(layout="bubble", value=[], show_label=False, show_copy_button=True, scale=3, height=400),
            gr.Accordion(label="Gemini Key", open=False)
            )
    else: return (gr.Button(value="Invalid Key"), chatbot, gr.Accordion(label="Gemini Key", open=True))

# Definindo Layout
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(layout="panel", show_label=False, value=[
        ("Put a valid gemini Key to start talking", None)
    ], show_copy_button=True, scale=3, height=400)

    with gr.Row() as buttons_place:
        question = gr.Textbox(placeholder="What are you asking? [Press Shift + Enter to send]", lines=4, show_label=False, scale=3)
        with gr.Column():
            clear = gr.Button(value='Restart Conversation', scale=1)
            speed = gr.Checkbox(label="Speed Up", info="This will make the chat stop slowly printing", scale=4)
            
    with gr.Accordion(label="Gemini Key", open=True) as tray:
        with gr.Row() as key_place:
            key = gr.Textbox(placeholder="Gemini Key", scale=4, show_label=False)
            test = gr.Button("See if it's valid", scale=1)


    # Eventos
    clear.click(delete, outputs=[question, chatbot])
    question.submit(talk, [question, chatbot], [chatbot])
    question.submit(lambda _: "", [question], [question])
    speed.change(fn = lambda s: sys.change_speed(s), inputs=[speed])
    # Deveria fechar mas ta quebrado #issue #7172
    test.click(fn = validate, inputs = [key, chatbot], outputs = [test, chatbot, tray], show_progress=True)

# Lançando o site
demo.launch()
