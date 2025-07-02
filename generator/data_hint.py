from datetime import datetime, date, time
import json
import os
import numpy as np
from generator.base_test import BaseTest
from generator.basic_party import BasicParty
from generator.basic_contact import BasicContact
from generator.basic_relation import BasicRelation
from generator.basic_account import BasicAccount
from generator.basic_transaction import BasicTransaction
from generator.basic_event import BasicEvent
from generator.basic_communication import BasicCommunication


class DataHint(BaseTest):
    NAME = "02-data-hint"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, DataHint.NAME)

    def generate(self, count, last_values = True):
        for i in range(count):
            self._generate(i, last_values)

    def _generate(self, i, last_values=True):
        """
        Generate data hints.

        :param i:               Current iteration
        :param last_values:     True - generate last value from collection (not random), useful for on-line feature store
                                where only the last value is stored on e.g. Redis, etc.
        """
        # generate one data set
        model = {}

        # random party (focus on 'Customer' because they have accounts and transactions also)
        parties = self.gmodel[BasicParty.NAME]
        parties_customer = [c for c in parties if c['party_type']=='Customer']
        # if it is not possible to select 'Customer' because only a few parties, I will use some parties (such as lead, etc.)
        if len(parties_customer)==0:
            parties_customer = parties
        party=parties_customer[self.rnd_int(0, len(parties_customer))]
        partyid = party['party_id']
        model[BasicParty.NAME] = party

        # random contact based on party
        contacts = self.gmodel[BasicContact.NAME]
        contacts_party = [c for c in contacts if c['party_id']==partyid]
        if len(contacts_party)>0:
            contact = contacts_party[-1] if last_values else contacts_party[self.rnd_int(0, len(contacts_party))]
            model[BasicContact.NAME] = contact

        # random relation
        relations = self.gmodel[BasicRelation.NAME]
        relation_party = [r for r in relations if r['party_id'] == partyid]
        if len(relation_party) > 0:
            relation = relation_party[-1] if last_values else relation_party[self.rnd_int(0, len(relation_party))]
            model[BasicRelation.NAME] = relation

        # random account
        accountid=None
        accounts = self.gmodel[BasicAccount.NAME]
        account_party = [a for a in accounts if a['party_id'] == partyid]
        if len(account_party) > 0:
            account = account_party[-1] if last_values else account_party[self.rnd_int(0, len(account_party))]
            accountid = account["account_id"]
            model[BasicAccount.NAME] = account

        # transaction
        if accountid:
            transactions = self.gmodel[BasicTransaction.NAME]
            transaction_account = [t for t in transactions if t['account_id'] == accountid]
            if len(transaction_account) > 0:
                transaction = transaction_account[-1] if last_values else transaction_account[self.rnd_int(0, len(transaction_account))]
                model[BasicTransaction.NAME] = transaction

        # event
        events = self.gmodel[BasicEvent.NAME]
        event_party = [e for e in events if e['party_id'] == partyid]
        if len(event_party) > 0:
            event = event_party[-1] if last_values else event_party[self.rnd_int(0, len(event_party))]
            model[BasicEvent.NAME] = event

        # communication
        communications = self.gmodel[BasicCommunication.NAME]
        communication_party = [c for c in communications if c['party_id'] == partyid]
        if len(communication_party) > 0:
            communication = communication_party[-1] if last_values else communication_party[self.rnd_int(0, len(communication_party))]
            model[BasicCommunication.NAME] = communication

        if last_values:
            self.model["spec"][f"HintLast-{i}"] = model
        else:
            self.model["spec"][f"Hint-{i}"] = model


    def save(self, path, dir: str):
        if not os.path.exists(path):
            os.makedirs(path)

        json_path=os.path.join(path, f"{dir}.json")

        self.model["name"] = dir
        self.model["description"] = f"Data hints (sample of data) for testing '{dir}'"

        with open(json_path, "w") as out_file:
            json.dump(self.model, out_file, indent=2, default=self.datetime_handler)

        # print(f"Creating: {'APPEND' if append else 'WRITE'}, name: '{self.name}', dir: '{dir}'...")
        #df=pd.DataFrame(self.model)

    def datetime_handler(self,obj):
        if isinstance(obj, (datetime, date, time)):
            return str(obj)

        if isinstance(obj, np.int32):
            return int(obj)
