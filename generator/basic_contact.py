import datetime
import uuid
from enum import Enum, Flag, IntFlag

from generator.base_data import BaseData
from faker import Faker
from faker.providers import internet, phone_number
from generator.basic_party import BasicParty

import faker.providers
import numpy

class ContactEnum(IntFlag):
    Phone = 1,
    Email = 2,
    Full = 3,

class BasicContact(BaseData):

    NAME= "02-basic-contact"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicContact.NAME)
        self.fake=Faker(['en_US'])
        self.fake.add_provider(internet)
        self.fake.add_provider(phone_number)

    def generate(self, count):

        # reference to the data from BasicParty
        parties = self.gmodel[BasicParty.NAME]

        # iteration cross all parties
        for party in parties:

            # max 3 contacts for Customers and only one contact for Leads or Prospects
            contacts= 1 if party['party-type'] != "Customer" else self.rnd_choose([1, 2, 3], [0.85, 0.1, 0.05])
            for count in range(contacts):

                # add new model
                model = self.model_item()

                # "name": "contact-id",
                model['contact-id']=str(uuid.uuid4())

                # "name": "party-id",
                model['party-id']=party['party-id']

                # generate different amount of contact information
                # Customer = email + phone
                # !Customer = random email or phone
                contact_detail=ContactEnum.Full if party['party-type']=="Customer" else ContactEnum.Email\
                    if self.rnd_bool() else ContactEnum.Phone

                if contact_detail & ContactEnum.Email:
                    # "name": "contact-email"
                    model['contact-email']=self.fake.email()

                if contact_detail & ContactEnum.Phone:
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

