import datetime
import json
import os


class Base:

    def __init__(self):
        pass

    @staticmethod
    def create(path, definition_file) -> dict:

        model_definition = {}
        path=os.path.join(path,"02-feature-set", definition_file+".json")

        with open(path, "r") as json_file:
            definition = json.load(json_file)

        # create entities
        for entity in definition['spec']['entities']:
            model_definition[entity['name']]=None

        # create features
        for feature in definition['spec']['features']:
            model_definition[feature['name']]=None

        return model_definition