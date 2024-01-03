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

    NAME = "04-basic-account"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicAccount.NAME)
        self.fake = Faker(['en_US'])

    def generate(self, count):

        # reference to the data from BasicParty
        parties = self.gmodel[BasicParty.NAME]

        # iteration cross all parties
        for party in parties:

            # accounts will be generated only for customers
            if party['party-type'] != "Customer":
                continue

            # customer can have from 1 to 4 accounts
            party_accounts=self.rnd_choose([1, 2, 3, 4], [0.85, 0.1, 0.04, 0.01])
            active_account_count=0
            for count in range(party_accounts):

                model=self.model_item()

                # "name": "account-id",
                # "description": "Unique account identificator",
                model['account-id']=str(uuid.uuid4())

                # "name": "party-id",
                # "description": "Party identificator",
                model['party-id']=party['party-id']

                # "name": "account-type",
                # "description": "Type of party account (saving account, current account, etc.)",
                model['account-type']=self.rnd_choose(["current account", "saving account"], [0.93, 0.07])

                # "name": "account-state",
                # "description": "Account state (e.g. active, closed, etc.)",
                model['account-state']=self.rnd_choose(["active", "closed", "blocked"], [0.98, 0.018, 0.002])

                # "name": "account-createdate",
                # "description": "Date for account creation",
                if model['account-state']=="active":
                    active_account_count=active_account_count+1
                    if active_account_count==1:
                        # only first account will have date for counterparty established
                        model['account-createdate']=party['party-typedate']
                    else:
                        # other active accounts, date will be between today and date for counterparty established
                        model['account-createdate']=self.fake.date_between_dates(party['party-typedate'],datetime.date.today())
                else:
                    # account is in state closed or blocked date will be between today and date for countrparty established
                    model['account-createdate']=self.fake.date_between_dates(party['party-typedate'],datetime.date.today())

                # "name": "account-nonactivedate",
                # "description": "Date when account state was closed or blocked",
                if model['account-state']=="active":
                    model['account-nonactivedate']=self.MAX_DATE
                else:
                    model['account-nonactivedate']=self.fake.date_between_dates(model['account-createdate'],datetime.date.today())

                # "name": "record-date",
                # "description": "The date when the record was created",
                model['record-date']=self.gmodel["NOW"]

                self.model.append(model)