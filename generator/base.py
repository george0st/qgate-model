import datetime
import json
import os
import numpy as np


class Base:

    def __init__(self):
        self._gen = np.random.default_rng()


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

    def rnd_int(self, low, high) -> int:
        return self._gen.integers(low, high)

    def rnd_float(self, low, high, ndigits = 0) -> int:
        if ndigits > 0:
            return round(self._gen.uniform(low, high), ndigits)
        return self._gen.uniform(low, high)

    def rnd_bool(self) -> bool:
        return bool(self._gen.integers(0, 2))

    def rnd_choose(self, items: list=[], probability: list=None):
        """
        Generate random value from list and based on defined probabilities

        :param items:        item for selection
        :param probability:  probability items (total sum is 1, sample [0.5, 0.1, 0.1, 0.3]
        :return:             selected value
        """
        return self._gen.choice(items, size=1, p=probability)[0]
