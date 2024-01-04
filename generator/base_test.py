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
        self.model = []

    @property
    def name(self):
        return self._name

    def generate(self, count):
        pass