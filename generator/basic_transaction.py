import datetime
import math
import uuid

from generator.base import Base
from faker import Faker
from generator.basic_account import BasicAccount
import faker.providers
import numpy
import pandas as pd

class BasicTransaction(Base):

    NAME= "05-basic-transaction"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicTransaction.NAME)
        self.fake = Faker(['en_US'])

    @property
    def Name(self):
        return BasicTransaction.NAME

    def generate(self, count):

        # reference to the data from BasicAccount
        account = self.gmodel[BasicAccount.NAME]

        # iteration cross all accounts
        for account_index in range(len(account['account-id'])):

            date_from=account['account-createdate'][account_index]

            if account['account-nonactivedate'][account_index] ==  self.MAX_DATE:
                date_to=datetime.date.today()
            else:
                date_to=account['account-nonactivedate'][account_index]

            dif_date=round((date_to-date_from).days/30)

            for mounth in range(dif_date):
                a=mounth*30
                b=(int)(self.rnd_int(1,30)[0])
                new_date=date_from+datetime.timedelta(days=a+b)

                # "name": "transaction-date",
                # "description": "Transaction date",
                self.model['transaction-date'].append(new_date)

                # "name": "transaction-id",
                # "description": "Unique transaction identificator",
                self.model['transaction-id'].append(str(uuid.uuid4()))

                # "name": "account-id",
                # "description": "Relation to account identificator",
                self.model['account-id'].append(account['account-id'][account_index])

                # "name": "party-id",
                # "description": "Relation to party identificator",
                self.model['party-id'].append(account['party-id'][account_index])

                # "name": "transaction-value",
                # "description": "Transaction value",

                #TODO: generate negative items also
                self.model['transaction-value'].append(self.rnd_choose(range(1000, 5000)))

                # "name": "transaction-currency",
                # "description": "Transaction currency",
                self.model['transaction-currency'].append("USD")

                # "name": "record-date",
                # "description": "The date when the record was created",
                self.model['record-date'].append(datetime.date.today())
