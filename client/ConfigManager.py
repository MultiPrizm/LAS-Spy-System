import json

class Configs():

    def __init__(self, update_delay):
        self.update_delay = update_delay

config: Configs = None

with open("config.json") as f:
    data = json.load(f)

    config = Configs(data["UDelay"])