import json


class JsonConfig:
    def __init__(self):
        with open('configuration.json') as f:
            self.data = json.load(f)


configData = JsonConfig().data
