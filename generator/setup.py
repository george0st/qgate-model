import json
import math
import uuid
import os
import numpy as np

class Singleton (type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Setup(metaclass=Singleton):

    def __init__(self, model_path):
        self._model_setting={}

        with open(os.path.join(model_path, "model.json"), "r") as json_file:
            setting = json.load(json_file)

        self._model_setting=setting["spec"]

    @property
    def csv_separator(self):
        return self._model_setting["CSV_SEPARATOR"]

    @property
    def csv_decimal(self):
        return self._model_setting["CSV_DECIMAL"]
