import json
import os, glob
import pandas as pd

from generator.basic_party import BasicParty
from generator.basic_account import BasicAccount
from generator.basic_transaction import BasicTransaction
from generator.base import Base
from enum import Enum


class Factory:
    class Entity(Enum):
        Party = 1
        Account = 2
        Transaction = 3

    def __init__(self, path, count, compress):
        self._path=path
        self._count=count
        self._compress=compress
        self._global_model={}

    def create(self, typing):
        ret=None
        if Factory.Entity.Party==typing:
            ret=BasicParty(self._path, self._global_model)
        elif Factory.Entity.Account==typing:
            ret=BasicAccount(self._path, self._global_model)
        elif Factory.Entity.Transaction==typing:
            ret=BasicTransaction(self._path, self._global_model)
        return ret

    def generate(self, entity: Base, count=1):
        entity.generate(count)
        self._global_model[entity.Name] = entity.model

if __name__ == '__main__':

    path=os.path.join(os.getcwd(), "..", "qgate-model", "01-model", "02-feature-set")
    count=1000
    compress=True
    label="1k"

    factory=Factory(path, count, compress)

    party=factory.create(Factory.Entity.Party)
    account=factory.create(Factory.Entity.Account)
    transaction=factory.create(Factory.Entity.Transaction)

    # TODO: vlozit generovane tridy do list kolekce

    count = 0
    while (count < 5):

        # generate data, one iteration
        factory.generate(party,10)
        factory.generate(account)
        factory.generate(transaction)

        # save data
        if count==0:
            # write to CSV
            party.save(False, "1k", True)
            account.save(False, "1k", True)
            transaction.save(False, "1k", True)
        else:
            # append to CSV
            party.save(True, "1k", True)
            account.save(True, "1k", True)
            transaction.save(True, "1k", True)
        party.clean()
        count = count + 1

    print("")


