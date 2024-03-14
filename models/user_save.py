import json
from os.path import join, abspath

class tags:
    chars = 'characters'
    narr = 'narrative'
    time = 'timeline'
    summ = 'summary'
    name = 'name'
    appear = 'appearance'
    person = 'personality'
    traits = 'traits'

def create_json(historia, personagens, timeline):
    everything = {}
    everything[tags.narr] = historia
    everything[tags.chars] = personagens[tags.chars]
    everything[tags.time] = timeline
    nome = 'new_chapter.json'
    nome = join('jsons', nome)
    
    f = open(nome, 'w')
    f.write(json.dumps(everything, indent=4))
    return abspath(f.name)

def save_from_editor(atual : dict):
    atual[tags.narr] = ""
    nome = 'Chapter_editado.json'
    nome = join('jsons', nome)
    
    f = open(nome, 'w')
    f.write(json.dumps(atual, indent=4))
    return abspath(f.name)