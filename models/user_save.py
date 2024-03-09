import json
from os import getcwd
from os.path import join, abspath

def create_json(historia, personagens, timeline):
    everything = {}
    everything[0] = historia
    everything[1] = personagens
    everything[2] = timeline
    # print(everything)

    f = open('chapter01.json', 'w')
    f.write(json.dumps(everything))
    return abspath(f.name)