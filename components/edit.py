import gradio as gr
import json
from models.user_save import tags
from models.user_save import save_from_editor

COUNT = 100
atual : dict = {tags.chars: [], tags.time:{tags.summ:"", tags.time: []}, tags.narr: ""}

def add_new_element(lista : list[str]):
    lista.append("")
    return [gr.Textbox(""), gr.Row(visible=True)]
def first_textboxes():
    new_rows = []; new_boxes = [] # Separar os dois para visibilidade
    delete_buttons = []; 
    for i in range(COUNT):
        with gr.Row(visible=False) as row:
            new_box = gr.Textbox(show_label=False, visible=True, interactive=True, container=False, scale=10)
            delete = gr.Button(f"Delete", visible=True, scale=1)
            new_rows += [row]; new_boxes += [new_box]; delete_buttons += [delete]
    with gr.Row(visible=True) as row:
        create_button = gr.Button("Create New")
    new_rows +=[row]

    return [new_rows, new_boxes, delete_buttons, create_button]
def create_textboxes(iterador):
    new_rows = []; new_boxes = []
    for i in iterador:
        new_box = gr.Textbox(f"{i}")
        new_rows += [gr.Row(visible=True)]; new_boxes += [new_box];
    for _ in range(COUNT - len(iterador)):
        new_rows += [gr.Row(visible=False)]
        new_boxes += [gr.Textbox()];
    new_rows += [gr.Row(visible=True)] # Create Button

    return [new_rows, new_boxes]

def carregar_json(file):
    with open(file, 'r') as f:
        global atual; atual = json.loads(f.read())
        del atual[tags.narr]
    new_names = []
    for i in atual[tags.chars]:
        new_names.append(i[tags.name])
    new_names = gr.Dropdown(choices=new_names, label='Names', interactive=True, visible=True)
    sumario = gr.Textbox(atual[tags.time][tags.summ], visible=True)
    # textboxes
    [row_appearances, new_appearances, _, _] = first_textboxes()
    [row_personalities,new_personalities, _, _] = first_textboxes()
    [row_traits,new_traits, _, _] = first_textboxes()
    [row_timeline, new_timeline_items] = create_textboxes(atual[tags.time][tags.time])
    return [new_names, *new_appearances, *new_personalities, *new_traits, sumario, *new_timeline_items,
            *row_appearances, *row_personalities, *row_traits, *row_timeline,
            gr.Accordion(visible=True), gr.Tab(visible=True)]

def change_name(char):
    for i in atual[tags.chars]:
        if i[tags.name] == char: selected = i
    # apperance
    [row_appearances, new_appearance] = create_textboxes(selected[tags.appear])
    [row_personality, new_personality] = create_textboxes(selected[tags.person])
    [row_traits, new_traits] = create_textboxes(selected[tags.traits])
    return [*new_appearance, *new_personality, *new_traits,
            *row_appearances, *row_personality, *row_traits,
            gr.Tab(visible=True),gr.Tab(visible=True),gr.Tab(visible=True)]

def add_new_character(new_name : str, old_names : list[str]):
    if new_name:
        new_char = {}
        new_char[tags.name] = new_name
        new_char[tags.person] = []
        new_char[tags.appear] = []
        new_char[tags.traits] = []
        atual[tags.chars].append(new_char)
    # Get all names
    all_names = []
    for i in atual[tags.chars]:
        all_names.append(i[tags.name])
    
    return [gr.Textbox(""), gr.Dropdown(choices=all_names)]

def create_new_thing(chars, place, name):
    # Achar onde modar
    if chars:
        for i in atual[tags.chars]: 
            if i[tags.name] == name: selecionar = i;
        selecionar = selecionar[place]
    else: selecionar = atual[tags.time][tags.time]
    selecionar.append("")
    # Mudar valores
    new_rows = []; new_boxes = [];
    for i in selecionar:
        new_rows.append(gr.Row(visible=True))
        new_boxes.append(gr.Textbox(i, visible=True))
    for _ in range(COUNT - len(selecionar)):
        new_rows.append(gr.Row(visible=False))
        new_boxes.append(gr.Textbox(visible=False))
    new_rows += [gr.Row(visible=True)] # Button Create
    
    return [*new_rows, *new_boxes]

def summary_change(s): atual[tags.time][tags.summ] = s
def timeline_change(s, num): atual[tags.time][tags.time][num] = s
def character_change(s, num, name, tag): 
    for i in atual[tags.chars]:
        if i[tags.name] == name: select = i
    select[tag][num] = s

def delete_timeline(num): 
    atual[tags.time][tags.time].pop(num)
    # Reconstruir timeline
    [row_timeline, new_timeline_items] = create_textboxes(atual[tags.time][tags.time])
    return [*row_timeline, *new_timeline_items]
def delete_things(num, name, tag):
    for i in atual[tags.chars]:
        if i[tags.name] == name: select = i
    select[tag].pop(num)
    [row_tag, tag_item] = create_textboxes(select[tag])
    return [*row_tag, *tag_item]

def create_download_file():
    global atual
    res_path = save_from_editor(atual)
    return gr.File(label = "Download seu capítulo", visible=True, value= [res_path], show_label=True)

def edit():
    with gr.Blocks() as edit_main:
        with gr.Blocks() as intructions:
            with gr.Row():
                gr.Markdown("# Envie um arquivo para editar a historia")
                upload_file = gr.UploadButton("Upload a file", type='filepath', file_types=['.json'])
        
        # Summary and timeline
        gr.Markdown("# Sumário da História e Eventos")
        summary = gr.Textbox(value = atual[tags.time][tags.summ],label="Sumário", visible=True, interactive=True, placeholder="Coloque o sumário")
        with gr.Accordion(label="Timeline", open=False, visible=True) as history:
            [row_timeline, timeline_items, timeline_delete, timeline_create] = first_textboxes()

        # Characters
        gr.Markdown("# Personagens e suas características")
        characters_names = gr.Dropdown([], label='Character Names', interactive=True, visible= True)
        # appearance, personality and traits
        with gr.Tabs(visible=True) as characters:
            with gr.Tab(visible=True, label="Create New Character"):
                with gr.Row():
                    new_name = gr.Textbox(interactive=True, placeholder="Put your new character name", container=False)
                    create_new_name = gr.Button("Create")
            with gr.Tab(visible=False, label="Appearance") as app_tab:
                [row_appearances, characters_appearances, delete_appearances, create_appearances] = first_textboxes()
            with gr.Tab(visible=False, label="Personality") as per_tab:
                [row_personality, characters_personality, delete_personalities, create_personalities] = first_textboxes()
            with gr.Tab(visible=False, label="Traits") as tra_tab:
                [row_traits, characters_traits, delete_traits, create_traits] = first_textboxes()
        
        # Debug and Download Area
        with gr.Row():
            see_json = gr.Button("Clique para ver como ficará o output")
            donwload_json = gr.Button("Create the download")
        files_downloads = gr.File(visible=False)
        with gr.Accordion(visible=True, label="Json de Saida", open=True):
            see = gr.JSON({"ATUALIZE PARA VER"})
        see_json.click(lambda: atual, [],[see])
        donwload_json.click(create_download_file, outputs=files_downloads)
        
        # PUT FUNCTIONS DOWN HERE
        # CONSTANTS
        TRUE = gr.Checkbox(value=True, visible=False); FALSE = gr.Checkbox(value=False, visible=False)
        TAGTIME = gr.Textbox(value=tags.time, visible=False)
        TAGAPP = gr.Textbox(value=tags.appear, visible=False)
        TAGTRA = gr.Textbox(value=tags.traits, visible=False)
        TAGPER = gr.Textbox(value=tags.person, visible=False) 
        numero = [gr.Number(i, visible=False) for i in range(COUNT)]       
        # Upload Functions
        upload_file.upload(
            carregar_json, 
            inputs=[upload_file], 
            outputs=[characters_names, *characters_appearances, *characters_personality, *characters_traits, 
                    summary, *timeline_items,
                    *row_appearances, *row_personality, *row_traits, *row_timeline,
                    characters, history])
        # Change character Function
        characters_names.input(change_name, characters_names, [
            *characters_appearances, *characters_personality, *characters_traits,
            *row_appearances, *row_personality, *row_traits,
            app_tab, per_tab, tra_tab
        ])
        # Create functions
        create_new_name.click(add_new_character, [new_name, characters_names], [new_name, characters_names])
        timeline_create.click(create_new_thing, [FALSE, TAGTIME, TAGTIME], [*row_timeline, *timeline_items])
        create_appearances.click(create_new_thing, [TRUE, TAGAPP, characters_names], [*row_appearances, *characters_appearances])
        create_personalities.click(create_new_thing, [TRUE, TAGPER, characters_names], [*row_personality, *characters_personality])
        create_traits.click(create_new_thing, [TRUE, TAGTRA, characters_names], [*row_traits, *characters_traits])
        # Change and delete functions
        summary.change(summary_change,inputs=[summary])
        for i in range(COUNT):
            # Change Functions
            timeline_items[i].change(timeline_change,inputs=[timeline_items[i], numero[i]])
            characters_appearances[i].change(character_change,inputs=[characters_appearances[i], numero[i], characters_names, TAGAPP])
            characters_personality[i].change(character_change,inputs=[characters_personality[i], numero[i], characters_names, TAGPER])
            characters_traits[i].change(character_change,inputs=[characters_traits[i], numero[i], characters_names, TAGTRA])
            #delete functions
            timeline_delete[i].click(delete_timeline, inputs=[numero[i]], outputs=[*row_timeline, *timeline_items])
            delete_appearances[i].click(delete_things, inputs=[numero[i], characters_names, TAGAPP], outputs=[*row_appearances,*characters_appearances])
            delete_personalities[i].click(delete_things, inputs=[numero[i], characters_names, TAGPER], outputs=[*row_personality, *characters_personality])
            delete_traits[i].click(delete_things, inputs=[numero[i], characters_names, TAGTRA], outputs=[*row_traits, *characters_traits])
        
    return edit_main