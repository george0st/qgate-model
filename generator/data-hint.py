import datetime
import math
import uuid

from generator.base import Base


class DataHint(Base):
    NAME = "02-data-hint"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, DataHint.NAME)

    def generate(self, count):
        pass