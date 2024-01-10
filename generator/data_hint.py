import datetime
import math
import uuid
import os

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

    def generate(self, count):
        for i in range(count):
            self._generate()

    def _generate(self):
        # generate one data set
        model = []

        # random party
        parties = self.gmodel[BasicParty.NAME]
        party=parties[self.rnd_int(0, len(parties))]
        partyid = party['party-id']
        model.append(party)

        # random contact based on party
        contacts = self.gmodel[BasicContact.NAME]
        contacts_party = [c for c in contacts if c['party-id']==partyid]
        if len(contacts_party)>0:
            contact=contacts_party[self.rnd_int(0, len(contacts_party))]
            model.append(contact)

        # random relation
        relations = self.gmodel[BasicRelation.NAME]
        relation_party = [r for r in relations if r['party-id'] == partyid]
        if len(relation_party) > 0:
            relation = relation_party[self.rnd_int(0, len(relation_party))]
            model.append(relation)

        # random account
        accounts = self.gmodel[BasicAccount.NAME]
        account_party = [a for a in relations if a['party-id'] == partyid]
        if len(account_party) > 0:
            account = account_party[self.rnd_int(0, len(account_party))]
            model.append(account)

        # TODO: add transaction
        # transaction
        # accounts = self.gmodel[BasicAccount.NAME]
        # account_party = [a for a in relations if a['party-id'] == partyid]
        # if len(account_party) > 0:
        #     account = account_party[self.rnd_int(0, len(account_party))]
        #     model.append(account)

        # event
        events = self.gmodel[BasicEvent.NAME]
        event_party = [e for e in events if e['party-id'] == partyid]
        if len(event_party) > 0:
            event = event_party[self.rnd_int(0, len(event_party))]
            model.append(event)

        # communication
        communications = self.gmodel[BasicCommunication.NAME]
        communication_party = [c for c in communications if c['party-id'] == partyid]
        if len(communication_party) > 0:
            communication = communication_party[self.rnd_int(0, len(communication_party))]
            model.append(communication)

        self.model.append(model)

    def save(self, path, dir: str):
        # (self._output_path, label, compress)
        if not os.path.exists(path):
            os.makedirs(path)

        os.path.join(path, f"{dir}.json"),

        # print(f"Creating: {'APPEND' if append else 'WRITE'}, name: '{self.name}', dir: '{dir}'...")
        #df=pd.DataFrame(self.model)
