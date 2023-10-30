import datetime
import uuid

from generator.base import Base
from faker import Faker
from faker.providers import internet, phone_number
from generator.basic_party import BasicParty

import faker.providers
import numpy


class BasicPartyRelation(Base):

    NAME= "03-basic-partyrelation"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicPartyRelation.NAME)
        self.fake=Faker(['en_US'])
        self.fake.add_provider(internet)
        self.fake.add_provider(phone_number)

    @property
    def Name(self):
        return BasicPartyRelation.NAME

    def generate(self, count):

        # reference to the data from BasicParty
        parties = self.gmodel[BasicParty.NAME]

        # iteration cross all parties
        for party in parties:

            #contacts=self.rnd_choose([1, 2, 3], [0.85, 0.1, 0.05])
            relations=self.rnd_choose(range(0,5), [0.1, 0.5, 0.2, 0.15, 0.05])
            for relation in range(relations):

                # add new model
                model = self.model_item()

                # "name": "relation-id",
                model['relation-id']=str(uuid.uuid4())


                # "name": "relation-parentid",
                # "name": "relation-childid",
                # "name": "relation-type",
                # "name": "relation-date",


                # "name": "record-date"
                model['record-date']=self.gmodel["NOW"]

                self.model.append(model)

