import datetime
import time

from generator.basic_party import BasicParty
from generator.basic_contact import BasicContact
from generator.basic_relation import BasicRelation
from generator.basic_account import BasicAccount
from generator.basic_transaction import BasicTransaction
from generator.basic_event import BasicEvent
from generator.basic_communication import BasicCommunication
from generator.base_data import BaseData
from generator.base_test import BaseTest
from generator.data_hint import DataHint
from generator.setup import Setup

class SyntheticData:

    def __init__(self, model_path="01-model", output_path="02-data", test_path="03-test"):

        # init setup singleton
        Setup(model_path)

        self._model_path=model_path
        self._output_path=output_path
        self._test_path=test_path

        self._gmodel={}
        self._gmodel["NOW"]=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._entities=[BaseData]

        self._tmodel={}
        self._tests=[BaseTest]

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

        self._tests.clear()
        self._create_test(DataHint(self._model_path, self._gmodel))

    def _create(self, new_entity: BaseData):
        self._entities.append(new_entity)
        self._gmodel[new_entity.name] = new_entity.model

    def _create_test(self, new_test: BaseTest):
        self._tests.append(new_test)
        self._tmodel[new_test.name] = new_test.model

    def _save_all(self, label, compress):
        for entity in self._entities:
            entity.save(self._output_path, label, compress)

    def _close(self):
        for entity in self._entities:
            entity.close()

    def _save_test_all(self, label):
        for test in self._tests:
            test.save(self._test_path, label)

    def _clean_all(self):
        for entity in self._entities:
            entity.clean()
        for test in self._tests:
            test.clean()

    def generate(self, label, count, bulk_max=1000, compress=True):
        print(f"Creating label: '{label}', count: {count} ...")
        # start time
        start_time = time.time()

        current_count = 0
        while (current_count < count):
            # generate data in bulk size based on party amount
            bulk = bulk_max if count > (current_count + bulk_max) else count - current_count
            print(f"  Bundle {current_count} -> {current_count+bulk} generate ...")
            for entity in self._entities:
                print(f"    '{entity.name}' ...")
                entity.generate(bulk)

            self._save_all(label, compress)

            self.generate_test(3)
            self._save_test_all(label)

            self._clean_all()
            current_count = current_count + bulk
        self._close()
        diff_time=time.time()-start_time
        print(f"DONE Duration: {round(diff_time,6)} seconds ({datetime.timedelta(seconds=diff_time)})")

    def generate_test(self, test_max):
        # test, if all test entities were added
        for test in self._tests:
            test.generate(test_max, True)
            test.generate(test_max, False)
