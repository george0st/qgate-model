import os, glob

from generator.basic_party import BasicParty
from generator.basic_account import BasicAccount
from generator.basic_transaction import BasicTransaction
from generator.base import Base

class SyntheticData:

    def __init__(self, path):
        self._path=path

        self._gmodel={}
        self._entities=[Base]

        self._create_all()

    def _create_all(self):
        self._entities.clear()

        self._create(BasicParty(self._path, self._gmodel))
        self._create(BasicAccount(self._path, self._gmodel))
        self._create(BasicTransaction(self._path, self._gmodel))

    def _create(self, new_entity: Base):
        self._entities.append(new_entity)
        self._gmodel[new_entity.Name] = new_entity.model

    def _save_all(self, append, label, compress):
        for entity in self._entities:
            entity.save(append, label, compress)

    def _clean_all(self):
        for entity in self._entities:
            entity.clean()

    def generate(self, label, count, bulk_max=1000, compress=True):

        current_count = 0
        while (current_count < count):
            # generate data in bulk size based on party amount
            bulk = bulk_max if count > (current_count + bulk_max) else count - current_count
            for entity in self._entities:
                entity.generate(bulk)

            self._save_all(False if current_count == 0 else True, label, compress)
            self._clean_all()
            current_count = current_count + bulk
