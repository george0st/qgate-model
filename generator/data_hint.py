import datetime
import math
import uuid

from generator.base_test import BaseTest
from generator.basic_party import BasicParty

class DataHint(BaseTest):
    NAME = "02-data-hint"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, DataHint.NAME)

    def generate(self, count):
        for i in range(count):
            self._generate()

    def _generate(self):
        # generate one data set
        model = []

        # reference to the data from BasicParty
        parties = self.gmodel[BasicParty.NAME]
        party=parties[self.rnd_int(0, len(parties))]
        partyid=party['party-id']
        print(partyid)

            # iteration cross all gmodel entities

            # start with party
                # random selection party from current bundle

            # iteration cross other entities and select random values based on defined party

        self.model.append(model)
