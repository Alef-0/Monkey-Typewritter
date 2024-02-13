import gradio as gr
import monkey as mk

chat = mk.create_chat(mk.create_model())

def talk(message, history):
    response = chat.send_message(message)
    response.resolve()
    history.append((message, response.parts[0].text))
    return "", history

def delete(message, history):
    while len(chat.history): chat.rewind()
    return '',[]

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="What are you asking?")
    clear = gr.Button(value='Restart Conversation')

    clear.click(delete, [msg, chatbot], [msg, chatbot])
    msg.submit(talk, [msg, chatbot], [msg, chatbot])


demo.launch()
