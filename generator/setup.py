import json
import math
import uuid
import os
import numpy as np

class Setup():

    def __init__(self, model_path):
        # get setup from json files
        path=os.path.join(model_path, "model.json")

        with open(path, "r") as json_file:
            definition = json.load(json_file)