import datetime
import math
import uuid
import os

from generator.base_test import BaseTest
from generator.basic_party import BasicParty
from generator.basic_contact import BasicContact
from generator.basic_relation import BasicRelation


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

            # iteration cross all gmodel entities

            # start with party
                # random selection party from current bundle

            # iteration cross other entities and select random values based on defined party

        self.model.append(model)

    def save(self, path, dir: str):
        # (self._output_path, label, compress)
        if not os.path.exists(path):
            os.makedirs(path)

        os.path.join(path, f"{dir}.json"),

        # print(f"Creating: {'APPEND' if append else 'WRITE'}, name: '{self.name}', dir: '{dir}'...")
        #df=pd.DataFrame(self.model)
