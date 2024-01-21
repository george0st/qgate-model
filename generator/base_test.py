import datetime
import json
import pandas as pd
import numpy as np
import os
from generator.base import Base


class BaseTest(Base):

    def __init__(self, path, gmodel, name):
        super().__init__()
        self._gen = np.random.default_rng()
        self.model = {}
        self.gmodel = gmodel
        self._name = name

        self.model["name"] = ""
        self.model["description"] = ""
        self.model["kind"]="test"
        self.model["spec"]={}

    @property
    def name(self):
        return self._name

    def clean(self):
        self.model.clear()
        self.model["name"] = ""
        self.model["description"] = ""
        self.model["kind"]="test"
        self.model["spec"]={}

    def generate(self, count, last_values):
        pass

    def save(self, path, dir: str):
        pass
