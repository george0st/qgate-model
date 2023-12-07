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

            # "name": "party-id",
            # "description": "Relation to party ID",
            #
            # "name": "communication-id",
            # "description": "Unigue communication identificator",
            #
            # "name": "content",
            # "description": "Content of communication",
            #
            # "name": "content-type",
            # "description": "Type of content",
            #
            # "name": "channel",
            # "description": "Communication channel",
            #
            # "name": "record-date",
            # "description": "The date when the record was created",

            self.model.append(model)