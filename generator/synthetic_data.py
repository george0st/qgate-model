import datetime
import os, glob
import time

from generator.basic_party import BasicParty
from generator.basic_contact import BasicContact
from generator.basic_relation import BasicRelation
from generator.basic_account import BasicAccount
from generator.basic_transaction import BasicTransaction
from generator.basic_event import BasicEvent
from generator.basic_communication import BasicCommunication
from generator.base import Base

class SyntheticData:

    def __init__(self, model_path="01-model", output_path="02-data"):
        self._model_path=model_path
        self._output_path=output_path

        self._gmodel={}
        self._gmodel["NOW"]=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._entities=[Base]

        self._create_all()

    def _create_all(self):
        self._entities.clear()

        self._create(BasicParty(self._model_path, self._gmodel))
        self._create(BasicContact(self._model_path, self._gmodel))
        self._create(BasicRelation(self._model_path, self._gmodel))
        self._create(BasicAccount(self._model_path, self._gmodel))
        self._create(BasicTransaction(self._model_path, self._gmodel))
        self._create(BasicEvent(self._model_path, self._gmodel))
        self._create(BasicCommunication(self._model_path, self._gmodel))

    def _create(self, new_entity: Base):
        self._entities.append(new_entity)
        self._gmodel[new_entity.Name] = new_entity.model

    def _save_all(self, append, label, compress):
        for entity in self._entities:
            entity.save(self._output_path, append, label, compress)

    def _clean_all(self):
        for entity in self._entities:
            entity.clean()

    def generate(self, label, count, bulk_max=1000, compress=True):

        print(f"Creating label: '{label}', count: {count} ...")
        # start time
        start_time = time.time()

        current_count = 0
        while (current_count < count):
            # generate data in bulk size based on party amount
            bulk = bulk_max if count > (current_count + bulk_max) else count - current_count
            for entity in self._entities:
                entity.generate(bulk)

            self._save_all(False if current_count == 0 else True, label, compress)
            self._clean_all()
            current_count = current_count + bulk
        diff_time=time.time()-start_time
        print(f"... DONE Duration: {round(diff_time,6)} seconds ({datetime.timedelta(seconds=diff_time)})")
