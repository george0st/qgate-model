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
    MAX_RELATIONS = 5

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

        # remove unlimited cycle for generation of relations
        if len(parties) < BasicPartyRelation.MAX_RELATIONS:
            return

        # iteration cross all parties
        for party in parties:

            relations=self.rnd_choose(range(0, BasicPartyRelation.MAX_RELATIONS), [0.55, 0.3, 0.1, 0.04, 0.01])
            for relation in range(relations):

                # add new model
                model = self.model_item()

                # "name": "relation-id",
                model['relation-id']=str(uuid.uuid4())

                # "name": "relation-parentid",
                model['relation-parentid']=party['party-id']

                # "name": "relation-childid",
                while (True):
                    random_id = parties[self.rnd_int(0, len(parties))]['party-id']
                    if random_id != model['relation-parentid']:
                        model['relation-childid'] = random_id
                        break

                # "name": "relation-type",
                model['relation-type']=None     # not used, right now

                # "name": "relation-date",
                model['relation-date']=None     # not used, right now

                # "name": "record-date"
                model['record-date']=self.gmodel["NOW"]

                self.model.append(model)

