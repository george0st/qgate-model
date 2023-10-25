import datetime
import math
import uuid

from generator.base import Base
from faker import Faker
import faker.providers
import numpy
import pandas as pd
from generator.basic_party import BasicParty


class BasicAccount(Base):

    NAME = "04-basic-account"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicAccount.NAME)
        self.fake = Faker(['en_US'])

    @property
    def Name(self):
        return BasicAccount.NAME

    def generate(self, count):
        # iteration cross all parties
        for party_index in range(len(self.gmodel['01-basic-party']['party-id'])):

            # accounts will be generated only for customers
            if self.gmodel['01-basic-party']['party-type'][party_index] != "Customer":
                continue

            # customer can have from 1 to 4 accounts
            party_accounts=self.rnd_choose([1, 2, 3, 4], [0.85, 0.1, 0.04, 0.01])
            active_account_count=0
            for count in range(party_accounts):

                # "name": "account-id",
                # "description": "Unique account identificator",
                self.model['account-id'].append(str(uuid.uuid4()))

                # "name": "party-id",
                # "description": "Party identificator",
                self.model['party-id'].append(self.gmodel['01-basic-party']['party-id'][party_index])

                # "name": "account-type",
                # "description": "Type of party account (saving account, current account, etc.)",
                self.model['account-type'].append(self.rnd_choose(["current account", "saving account"], [0.93, 0.07]))

                # "name": "account-state",
                # "description": "Account state (e.g. active, closed, etc.)",
                self.model['account-state'].append(self.rnd_choose(["active", "closed", "blocked"], [0.98, 0.018, 0.002]))

                # "name": "account-createdate",
                # "description": "Date for account creation",
                if self.model['account-state'][-1]=="active":
                    active_account_count=active_account_count+1
                    if active_account_count==1:
                        # only first account will have date for counterparty established
                        self.model['account-createdate'].append(
                            self.gmodel['01-basic-party']['party-typedate'][party_index])
                    else:
                        # other active accounts, date will be between today and date for counterparty established
                        self.model['account-createdate'].append(
                            self.fake.date_between_dates(
                                self.gmodel['01-basic-party']['party-typedate'][party_index],
                                datetime.date.today())
                        )
                else:
                    # account is in state closed or blocked date will be between today and date for countrparty established
                    self.model['account-createdate'].append(
                        self.fake.date_between_dates(
                            self.gmodel['01-basic-party']['party-typedate'][party_index],
                            datetime.date.today())
                    )

                # "name": "account-nonactivedate",
                # "description": "Date when account state was closed or blocked",
                if self.model['account-state'][-1]=="active":
                    self.model['account-nonactivedate'].append(self.MAX_DATE)
                else:
                    self.model['account-nonactivedate'].append(
                        self.fake.date_between_dates(
                            self.model['account-createdate'][-1],
                            datetime.date.today())
                    )

                # "name": "record-date",
                # "description": "The date when the record was created",
                self.model['record-date'].append(datetime.date.today())
