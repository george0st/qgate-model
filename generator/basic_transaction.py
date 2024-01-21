import datetime
import math
import uuid

from generator.base_data import BaseData
from faker import Faker
from generator.basic_account import BasicAccount
from faker.providers import bank

class BasicTransaction(BaseData):

    NAME= "05-basic-transaction"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicTransaction.NAME)
        self.fake = Faker(['en_US'])
        self.fake_at = Faker(['de_AT'])
        self.fake_de = Faker(['de_DE'])
        self.fake_ch = Faker(['de_CH'])
        self.fake_pl = Faker(['pl_PL'])
        self.fake_it = Faker(['it_IT'])
        self.fake_es = Faker(['es_ES'])
        self.fake_tr = Faker(['tr_TR'])
        self.fake_az = Faker(['az_AZ'])
        self.fake_ru = Faker(['ru_RU'])

    def generate(self, count):

        # reference to the data from BasicAccount
        accounts = self.gmodel[BasicAccount.NAME]

        # iteration cross all accounts
        for account in accounts:

            date_from=account['account-createdate']

            if account['account-nonactivedate'] ==  self.MAX_DATE:
                date_to=datetime.date.today()
            else:
                date_to=account['account-nonactivedate']

            dif_date=round((date_to-date_from).days/30)

            for mounth in range(dif_date):
                a=mounth*30
                b=int(self.rnd_int(1,30))
                new_date=date_from+datetime.timedelta(days=a+b)

                model=self.model_item()

                # "name": "transaction-id",
                # "description": "Unique transaction identificator",
                model['transaction-id']=str(uuid.uuid4())

                # "name": "account-id",
                # "description": "Relation to account identificator",
                model['account-id']=account['account-id']

                # "name": "transaction-direction",
                # "description": "Transaction direction e.g. incoming, outgoing",
                # TODO: Add both directions
                model['transaction-direction'] = "Incoming"

                # "name": "transaction-type",
                # "description": "Transaction type",
                model['transaction-type']=self.rnd_choose(["Standard", "Instant"], [0.7, 0.3])

                # "name": "transaction-value",
                # "description": "Transaction value",
                #TODO: generate negative items also
                model['transaction-value']=self.rnd_choose(range(1000, 5000))

                # "name": "transaction-currency",
                # "description": "Transaction currency",
                model['transaction-currency']="USD"

                # "name": "transaction-description",
                # "description": "Transaction description",
                model["transaction-description"] = self.fake.text(max_nb_chars=64)

                # "name": "transaction-date",
                # "description": "Transaction date",
                model['transaction-date']=new_date

                # "name": "counterparty-name",
                # "description": "Transaction counterparty name",
                model["counterparty-name"] = self.fake.name()

                # "name": "counterparty-iban",
                # "description": "Transaction counterparty IBAN",
                if int(self.rnd_choose([0,1],[0.998, 0.002]))==0:
                    iban=self.fake.iban()
                else:
                    tmp_fake=self.rnd_choose([self.fake_at, self.fake_de, self.fake_ch,
                                                    self.fake_pl, self.fake_it, self.fake_es,
                                                    self.fake_tr, self.fake_az, self.fake_ru],
                                          [0.3, 0.2, 0.2, 0.1, 0.1, 0.025, 0.025, 0.025, 0.025])
                    iban=tmp_fake.iban()
                model["counterparty-iban"]=iban

                # "name": "counterparty-other",
                # "description": "Transaction counterparty other information",
                # TODO: Add

                # "name": "transaction-fraudanomaly",
                # "description": "Possible fraud anomaly detection (min. 0 - without anomaly detection, max. 1)",
                model["transaction-fraudanomaly"] = 0

                # "name": "transaction-fraud",
                # "description": "Identification of fraud (True - fraud, False - without fraud)",
                model["transaction-fraud"] = False

            # "name": "record-date",
                # "description": "The date when the record was created",
                model['record-date']=self.gmodel["NOW"]

                self.model.append(model)
