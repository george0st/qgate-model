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

        events_init = {"access": ["login", "logout"]}

        # list of groups and group probability
        #   [[group, group probability], ...]
        events_group=[["user profile", 0.01],
                      ["product", 0.2],
                      ["offer", 0.8]]

        # list of categorie and probabilities for show and change
        #   "group": [["category", show probability, change probability], ...]
        events_category = {"user profile": [["income", 0.999, 0.001],
                                                  ["expences", 0.9995, 0.0005],
                                                  ["address", 0.999, 0.001],
                                                  ["email", 0.995, 0.005],
                                                  ["phone", 0.998, 0.002],
                                                  ["children", 0.99995, 0.00005]],
                     "product": [["contract detail", 0.99, 0.01],
                                 ["account detail", 0.99, 0.01],
                                 ["legal conditions", 0.9999, 0.0001],
                                 ["sanctions", 0.9999, 0.0001]],
                     "offer": [["product list"],
                               ["service list"],
                               ["legal conditions"],
                               ["sanctions"]]}

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

            # only 3 months back history
            # max 0-2 bandl of events per day
            # mix of actions
                # access - login, logout
                # profile - income, expences, address, email, phone, children
                # product - contract detail, account detail, legal conditions, sanctions
                # offer - product list, service list, legal conditions, sanctions



            # "name": "event-group",
            # "name": "event-category",
            # "name": "event-action",

            # "name": "event-detail",
            # "name": "event-date",

            # "name": "record-date"
            model['record-date']=self.gmodel["NOW"]

            self.model.append(model)

