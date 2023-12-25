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
    COMMUNICATION_HISTORY_DAYS = 90

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

            # only 3 months back history
            # max 0-2 bandl of communication per day

            # generate communication with history EVENT_HISTORY_DAYS
            party_customer=party['party-type'] == "Customer"
            communication_date = self.now - datetime.timedelta(days=float(BasicCommunication.COMMUNICATION_HISTORY_DAYS))

            # iteration cross days
            while True:

                # day for communication
                #   for customer:       more active
                #   for non customer:   small amount of activities
                if party_customer:
                    day = int(1.1 * self.rnd_choose(range(10),[0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0.9]))
                else:
                    day = int(1.3 * self.rnd_choose(range(15), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.05, 0.05, 0.9]))
                communication_date = communication_date + datetime.timedelta(days=float(day))
                if communication_date > self.now:
                    break

                # define bundle
                #   for customer:       size 2-15x events (bigger amount of activities)
                #   for non-customer:   size 2-10x events (small amount of activites)
                session_id = str(uuid.uuid4())
                session_communications=self.rnd_choose(range(2, 15)) if party_customer else self.rnd_choose(range(2, 10))
                session_datetime = datetime.datetime(communication_date.year,
                                                     communication_date.month,
                                                     communication_date.day,
                                                     self.rnd_int(0,24),
                                                     self.rnd_int(0, 60),
                                                     self.rnd_int(0, 60))
                for event in range(session_communications):

                    # add new model
                    model = self.model_item()

                    # "name": "communication-id",
                    model['communication-id'] = str(uuid.uuid4())

                    # "name": "party-id",
                    model['party-id'] = party['party-id']


                    # TODO: add content
                    # "name": "content",
                    model['content'] = ""


                    # "name": "content-type",
                    model['content-type'] = "text"

                    # "name": "channel",
                    model['channel'] = self.rnd_choose(["email", "chat"], [0.8, 0.2])

                    # "name": "communication-date",
                    #model['communication-date'] = self.gmodel["NOW"]
                    session_datetime = session_datetime + datetime.timedelta(seconds=float(self.rnd_int(0,13)))
                    model['communication-date']=session_datetime.strftime("%Y-%m-%d %H:%M:%S")

                    # "name": "record-date"
                    model['record-date'] = self.gmodel["NOW"]

                    self.model.append(model)