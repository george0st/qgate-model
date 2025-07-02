import uuid
from enum import Enum, Flag, IntFlag
from generator.base_data import BaseData
from faker import Faker
from faker.providers import internet, phone_number
from generator.basic_party import BasicParty


class ContactEnum(IntFlag):
    Phone = 1,
    Email = 2,
    Full = 3,

class BasicContact(BaseData):

    NAME= "02-basic_contact"

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
            contacts= 1 if party['party_type'] != "Customer" else self.rnd_choose([1, 2, 3], [0.85, 0.1, 0.05])
            for count in range(contacts):

                # add new model
                model = self.model_item()

                # "name": "contact_id",
                model['contact_id']=str(uuid.uuid4())

                # "name": "party_id",
                model['party_id']=party['party_id']

                # generate different amount of contact information
                # Customer = email + phone
                # !Customer = random email or phone
                contact_detail=ContactEnum.Full if party['party_type']=="Customer" else ContactEnum.Email \
                    if self.rnd_bool() else ContactEnum.Phone

                # "name": "contact_email"
                if contact_detail & ContactEnum.Email:
                    model['contact_email'] = self.fake.email()
                else:
                    model['contact_email'] = ""

                # "name": "contact_phone"
                if contact_detail & ContactEnum.Phone:
                    model['contact_phone'] = self.fake.phone_number()
                else:
                    model['contact_phone'] = ""

                # "name": "contact_state"
                if count==0:
                    model['contact_state']= "Active"
                elif count==1:
                    model['contact_state']=self.rnd_choose(["Active", "InActive"], [0.95, 0.05])
                else:
                    model['contact_state']= "InActive"
                self.apply_none_value(model, 'contact_state', "InActive", probability_multiplicator=0.5)

                # "name": "record-date"
                model['record_date']=self.gmodel["NOW"]

                self.model.append(model)
