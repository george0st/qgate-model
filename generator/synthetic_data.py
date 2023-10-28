import os, glob

from generator.basic_party import BasicParty
from generator.basic_account import BasicAccount
from generator.basic_transaction import BasicTransaction
from generator.base import Base

class SyntheticData:

    def __init__(self, path, label, count, bulk_max=1000, compress=True):
        self._path=path
        self._label=label
        self._count=count
        self._bulk_max=bulk_max
        self._compress=compress

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

    def _save_all(self, append):
        for entity in self._entities:
            entity.save(append, self._label, self._compress)

    def _clean_all(self):
        for entity in self._entities:
            entity.clean()

    def generate(self):

        count = 0
        while (count < self._count):
            # generate data in bulk size based on party amount
            bulk = self._bulk_max if self._count > (count + self._bulk_max) else self._count - count
            for entity in self._entities:
                entity.generate(bulk)

            self._save_all(False if count == 0 else True)
            self._clean_all()
            count = count + bulk
