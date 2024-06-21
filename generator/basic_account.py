import datetime
import math
import uuid

from generator.base_data import BaseData
from faker import Faker
import faker.providers
import numpy
import pandas as pd
from generator.basic_party import BasicParty


class BasicAccount(BaseData):

    NAME = "04-basic_account"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicAccount.NAME)
        self.fake = Faker(['en_US'])

    def generate(self, count):

        # reference to the data from BasicParty
        parties = self.gmodel[BasicParty.NAME]

        # iteration cross all parties
        for party in parties:

            # accounts will be generated only for customers
            if party['party_type'] != "Customer":
                continue

            # customer can have from 1 to 4 accounts
            party_accounts=self.rnd_choose([1, 2, 3, 4], [0.85, 0.1, 0.04, 0.01])
            active_account_count=0
            for count in range(party_accounts):

                model=self.model_item()

                # "name": "account-id",
                # "description": "Unique account identificator",
                model['account_id']=str(uuid.uuid4())

                # "name": "party_id",
                # "description": "Party identificator",
                model['party_id']=party['party_id']

                # "name": "account-type",
                # "description": "Type of party account (saving account, current account, etc.)",
                model['account_type']=self.rnd_choose(["Current account", "Saving account"], [0.93, 0.07])

                # "name": "account-state",
                # "description": "Account state (e.g. active, closed, etc.)",
                model['account_state']=self.rnd_choose(["Active", "Closed", "Blocked"], [0.98, 0.018, 0.002])
                self.apply_none_value(model, 'account_state', "Closed",lower_probability=0.2)

                # "name": "account-createdate",
                # "description": "Date for account creation",
                if model['account_state']=="Active":
                    active_account_count=active_account_count+1
                    if active_account_count==1:
                        # only first account will have date for counterparty established
                        model['account_createdate']=party['party_typedate']
                    else:
                        # other active accounts, date will be between today and date for counterparty established
                        model['account_createdate']=self.fake.date_between_dates(party['party_typedate'],datetime.date.today())
                else:
                    # account is in state closed or blocked date will be between today and date for countrparty established
                    model['account_createdate']=self.fake.date_between_dates(party['party_typedate'],datetime.date.today())

                # "name": "account-nonactivedate",
                # "description": "Date when account state was closed or blocked",
                if model['account_state']=="Active":
                    model['account_nonactivedate']=self.MAX_DATE
                else:
                    model['account_nonactivedate']=self.fake.date_between_dates(model['account_createdate'],datetime.date.today())

                # "name": "record-date",
                # "description": "The date when the record was created",
                model['record_date']=self.gmodel["NOW"]

                self.model.append(model)