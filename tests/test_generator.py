import os
import unittest
from os import path
import shutil
import pandas as pd
from generator.synthetic_data import SyntheticData
from generator import basic_party, basic_contact, basic_relation, basic_account, basic_transaction, basic_event, basic_communication


class TestGenerator(unittest.TestCase):

    OUTPUT_ADR = "../tests_output/synthetic_data/"

    @classmethod
    def setUpClass(cls):
        # setup the same dir for different unit test execution
        if os.path.split(os.getcwd())[-1]!="tests":
            os.chdir("tests")
            print(f"ONLY INFO: Change directory for test execution to '{os.getcwd()}'.")

        shutil.rmtree(TestGenerator.OUTPUT_ADR, True)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_generate_compress(self):

        lbl="0-size-20,20-compress"
        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
        generator.generate(label=lbl, count=20, bulk_max=20, compress=True)

        dir=path.join(TestGenerator.OUTPUT_ADR, lbl)
        self.assertTrue(os.path.exists(dir))
        self.assertTrue(os.path.exists(path.join(dir, f"{basic_communication.BasicCommunication.NAME}.csv.gz")))
        self.assertTrue(os.path.exists(path.join(dir, f"{basic_contact.BasicContact.NAME}.csv.gz")))

    def test_generate_compress_smallbulk(self):
        lbl="0-size-20,6-compress"

        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
        generator.generate(label=lbl, count=20, bulk_max=6, compress=True)

        dir=path.join(TestGenerator.OUTPUT_ADR, lbl)
        self.assertTrue(os.path.exists(dir))
        self.assertTrue(os.path.exists(path.join(dir, f"{basic_communication.BasicCommunication.NAME}.csv.gz")))
        self.assertTrue(os.path.exists(path.join(dir, f"{basic_contact.BasicContact.NAME}.csv.gz")))

    def test_generate_compress_super_smallbulk(self):
        lbl="0-size-s-10,6-compress"

        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
        generator.generate(label=lbl, count=10, bulk_max=6, compress=True)

        dir=path.join(TestGenerator.OUTPUT_ADR, lbl)
        self.assertTrue(os.path.exists(dir))
        self.assertTrue(os.path.exists(path.join(dir, f"{basic_communication.BasicCommunication.NAME}.csv.gz")))
        self.assertTrue(os.path.exists(path.join(dir, f"{basic_contact.BasicContact.NAME}.csv.gz")))

    def test_generate(self):
        lbl = "0-size-200,20"

        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
        generator.generate(label=lbl, count=200, bulk_max=20, compress=False)

        dir=path.join(TestGenerator.OUTPUT_ADR, lbl)
        self.assertTrue(os.path.exists(dir))
        self.assertTrue(os.path.exists(path.join(dir, f"{basic_party.BasicParty.NAME}.csv")))
        self.assertTrue(os.path.exists(path.join(dir, f"{basic_contact.BasicContact.NAME}.csv")))

    def test_generate_smallbulk_repeat(self):
        """Repeat generation of small files"""

        for i in range(25):
            lbl = f"0-size-iter{i}-8,6"

            generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
            generator.generate(label=lbl, count=8, bulk_max=6, compress=False)

            dir = path.join(TestGenerator.OUTPUT_ADR, lbl)
            self.assertTrue(os.path.exists(dir))
            self.assertTrue(os.path.exists(path.join(dir, f"{basic_party.BasicParty.NAME}.csv")))
            self.assertTrue(os.path.exists(path.join(dir, f"{basic_contact.BasicContact.NAME}.csv")))

    def test_generate_smallbulk(self):
        lbl = "0-size-20,6"

        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
        generator.generate(label=lbl, count=20, bulk_max=6, compress=False)

        dir = path.join(TestGenerator.OUTPUT_ADR, lbl)
        self.assertTrue(os.path.exists(dir))
        self.assertTrue(os.path.exists(path.join(dir, f"{basic_party.BasicParty.NAME}.csv")))
        self.assertTrue(os.path.exists(path.join(dir, f"{basic_contact.BasicContact.NAME}.csv")))

    def test_generate_super_smallbulk(self):
        lbl = "0-size-s-10,6"

        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
        generator.generate(label=lbl, count=10, bulk_max=6, compress=False)

        dir = path.join(TestGenerator.OUTPUT_ADR, lbl)
        self.assertTrue(os.path.exists(dir))
        self.assertTrue(os.path.exists(path.join(dir, f"{basic_party.BasicParty.NAME}.csv")))
        self.assertTrue(os.path.exists(path.join(dir, f"{basic_contact.BasicContact.NAME}.csv")))

    def test_generate_bigbulk(self):
        lbl = "0-size-2000,2000"

        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
        generator.generate(label=lbl, count=2000, bulk_max=2000, compress=False)

        dir = path.join(TestGenerator.OUTPUT_ADR, lbl)
        self.assertTrue(os.path.exists(dir))
        self.assertTrue(os.path.exists(path.join(dir, f"{basic_party.BasicParty.NAME}.csv")))
        self.assertTrue(os.path.exists(path.join(dir, f"{basic_contact.BasicContact.NAME}.csv")))

    def test_generate_bigbulk_repeat(self):
        for i in range(5):
            lbl = f"0-size-iter{i}-1000,1000"

            generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
            generator.generate(label=lbl, count=1000, bulk_max=1000, compress=False)

            dir = path.join(TestGenerator.OUTPUT_ADR, lbl)
            self.assertTrue(os.path.exists(dir))
            self.assertTrue(os.path.exists(path.join(dir, f"{basic_party.BasicParty.NAME}.csv")))
            self.assertTrue(os.path.exists(path.join(dir, f"{basic_contact.BasicContact.NAME}.csv")))


    def _check_csv_header(self, filename, key_texts: list):
        if os.path.exists(filename):
            content = pd.read_csv(filename).to_string()
            for key_text in key_texts:
                self.assertTrue(content.find(key_text) >= 0)

    def test_csv_structure(self):
        """All csv have header"""
        lbl = "0-size-csvcheck-10,6"

        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
        generator.generate(label=lbl, count=10, bulk_max=6, compress=False)

        dir = path.join(TestGenerator.OUTPUT_ADR, lbl)
        self.assertTrue(os.path.exists(dir))
        self._check_csv_header(path.join(dir, f"{basic_party.BasicParty.NAME}.csv"),
                               ["party_id", "party_gender"])
        self._check_csv_header(path.join(dir, f"{basic_contact.BasicContact.NAME}.csv"),
                               ["party_id", "contact_id", "contact_state"])
        self._check_csv_header(path.join(dir, f"{basic_relation.BasicRelation.NAME}.csv"),
                               ["party_id", "relation_id", "relation_type"])
        self._check_csv_header(path.join(dir, f"{basic_account.BasicAccount.NAME}.csv"),
                               ["party_id", "account_id", "account_state"])
        self._check_csv_header(path.join(dir, f"{basic_transaction.BasicTransaction.NAME}.csv"),
                               ["account_id", "transaction_id", "transaction_direction"])
        self._check_csv_header(path.join(dir, f"{basic_event.BasicEvent.NAME}.csv"),
                               ["party_id", "event_id", "session_id"])
        self._check_csv_header(path.join(dir, f"{basic_communication.BasicCommunication.NAME}.csv"),
                               ["party_id", "communication_id", "content"])

    # TODO: Add batch size under limit, it will generate wrong dataset