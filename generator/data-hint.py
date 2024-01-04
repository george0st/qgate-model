import datetime
import math
import uuid

from generator.base_test import BaseTest


class DataHint(BaseTest):
    NAME = "02-data-hint"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, DataHint.NAME)

    def generate(self, count):
        for i in range(count):
            self._generate()

    def _generate(self):

        # model = self.model_item()

            # iteration cross all gmodel entities

            # start with party
                # random selection party from current bundle

            # iteration cross other entities and select random values based on defined party

        # self.model.append(model)
        pass
