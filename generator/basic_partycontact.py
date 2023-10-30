import datetime
import uuid

from generator.base import Base
from faker import Faker
from faker.providers import internet, phone_number
from generator.basic_party import BasicParty

import faker.providers
import numpy


class BasicPartyContact(Base):

    NAME= "02-basic-partycontact"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicPartyContact.NAME)
        self.fake=Faker(['en_US'])
        self.fake.add_provider(internet)
        self.fake.add_provider(phone_number)

    @property
    def Name(self):
        return BasicPartyContact.NAME

    def generate(self, count):

        # reference to the data from BasicParty
        parties = self.gmodel[BasicParty.NAME]

        # iteration cross all parties
        for party in parties:

            contacts=self.rnd_choose([1, 2, 3], [0.85, 0.1, 0.05])
            for count in range(contacts):

                # add new model
                model = self.model_item()

                # "name": "contact-id",
                model['contact-id']=str(uuid.uuid4())

                # "name": "party-id",
                model['party-id']=party['party-id']

                # TODO: evaluate if email and phone has prospect and lead

                # "name": "contact-email"
                model['contact-email']=self.fake.email()

                # "name": "contact-phone"
                model['contact-phone']=self.fake.phone_number()

                # "name": "contact-state"
                if count==0:
                    model['contact-state']= "Active"
                elif count==1:
                    model['contact-state']=self.rnd_choose(["Active", "InActive"], [0.95, 0.05])
                else:
                    model['contact-state']= "InActive"

                # "name": "record-date"
                model['record-date']=self.gmodel["NOW"]

                self.model.append(model)

