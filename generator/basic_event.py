import datetime
import uuid

from generator.base import Base
from faker import Faker
from faker.providers import internet, phone_number
from generator.basic_party import BasicParty

import faker.providers
import numpy


class BasicEvent(Base):

    NAME= "06-basic-event"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicEvent.NAME)
        self.fake=Faker(['en_US'])
        self.fake.add_provider(internet)
        self.fake.add_provider(phone_number)

    @property
    def Name(self):
        return BasicEvent.NAME

    def generate(self, count):

        # reference to the data from BasicParty
        parties = self.gmodel[BasicParty.NAME]

        # iteration cross all parties
        for party in parties:

            # add new model
            model = self.model_item()

            # "name": "event-id",
            model['event-id']=str(uuid.uuid4())

            # "name": "party-id",
            model['party-id']=party['party-id']

            # only 3 months back
            # max 0-2 bandl per day
            # mix of action
                # login-logout or login only
                # profile, contract, check account state, list product, list services,

            # "name": "event-group",
            # "name": "event-category",
            # "name": "event-action",

            # "name": "event-detail",
            # "name": "event-date",

            # "name": "record-date"
            model['record-date']=self.gmodel["NOW"]

            self.model.append(model)

