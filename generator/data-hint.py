import datetime
import math
import uuid

from generator.base_data import BaseData


class DataHint(BaseData):
    NAME = "02-data-hint"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, DataHint.NAME)

    def generate(self, count):
        pass