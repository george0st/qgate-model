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
        party = self.gmodel[BasicParty.NAME]

        # iteration cross all parties
        for party_index in range(len(party['party-id'])):

            contacts=self.rnd_choose([1, 2, 3], [0.85, 0.1, 0.05])
            for count in range(contacts):

                # "name": "contact-id",
                self.model['contact-id'].append(str(uuid.uuid4()))

                # "name": "party-id",
                self.model['party-id'].append(party['party-id'][party_index])

                # "name": "contact-email"
                self.model['contact-email'].append(self.fake.email())

                # "name": "contact-phone"
                self.model['contact-phone'].append(self.fake.phone_number())

                # "name": "contact-state"
                if count==0:
                    self.model['contact-state'].append("Active")
                elif count==1:
                    self.model['contact-state'].append(self.rnd_choose(["Active","InActive"],[0.95,0.05]))
                else:
                    self.model['contact-state'].append("InActive")


                # "name": "record-date"
                self.model['record-date'].append(self.gmodel["NOW"])