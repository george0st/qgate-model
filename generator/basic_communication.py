import datetime
import math
import uuid

from generator.base import Base
from faker import Faker
import faker.providers
import numpy
import pandas as pd
from generator.basic_party import BasicParty


class BasicCommunication(Base):

    NAME = "07-basic-communication"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicCommunication.NAME)
        self.fake = Faker(['en_US'])

    @property
    def Name(self):
        return BasicCommunication.NAME

    def generate(self, count):

        # reference to the data from BasicParty
        parties = self.gmodel[BasicParty.NAME]

        # iteration cross all parties
        for party in parties:

            model=self.model_item()

            # add new model
            model = self.model_item()

            # "name": "communication-id",
            model['communication-id'] = str(uuid.uuid4())

            # "name": "party-id",
            model['party-id'] = party['party-id']

            # "name": "content",
            model['content'] = ""

            # "name": "content-type",
            model['content-type'] = "text"

            # "name": "channel",
            model['channel'] = self.rnd_choose(["email", "chat"], [0.8, 0.2])

            # "name": "record-date"
            model['record-date'] = self.gmodel["NOW"]

            self.model.append(model)