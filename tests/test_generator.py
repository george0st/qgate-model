import os
import unittest
import time
from os import path
import shutil
from generator.synthetic_data import SyntheticData
from generator.basic_communication import BasicCommunication


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
        self.assertTrue(os.path.exists(path.join(dir, f"{BasicCommunication.NAME}.csv.gz")))

    def test_generate_compress_smallbulk(self):
        lbl="0-size-20,6-compress"

        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
        generator.generate(label=lbl, count=20, bulk_max=6, compress=True)

        dir=path.join(TestGenerator.OUTPUT_ADR, lbl)
        self.assertTrue(os.path.exists(dir))
        self.assertTrue(os.path.exists(path.join(dir, f"{BasicCommunication.NAME}.csv.gz")))

    def test_generate_compress_smallbulk(self):
        lbl="0-size-20,6-compress"

        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
        generator.generate(label=lbl, count=20, bulk_max=6, compress=True)

        dir=path.join(TestGenerator.OUTPUT_ADR, lbl)
        self.assertTrue(os.path.exists(dir))
        self.assertTrue(os.path.exists(path.join(dir, f"{BasicCommunication.NAME}.csv.gz")))

    def test_generate_compress_super_smallbulk(self):
        lbl="0-size-s-10,6-compress"

        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
        generator.generate(label=lbl, count=10, bulk_max=6, compress=True)

        dir=path.join(TestGenerator.OUTPUT_ADR, lbl)
        self.assertTrue(os.path.exists(dir))
        self.assertTrue(os.path.exists(path.join(dir, f"{BasicCommunication.NAME}.csv.gz")))

    def test_generate(self):
        lbl = "0-size-200,20"

        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
        generator.generate(label=lbl, count=200, bulk_max=20, compress=False)

        dir=path.join(TestGenerator.OUTPUT_ADR, lbl)
        self.assertTrue(os.path.exists(dir))
        self.assertTrue(os.path.exists(path.join(dir, f"{BasicCommunication.NAME}.csv")))

    def test_generate_smallbulk(self):
        lbl = "0-size-20,6"

        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
        generator.generate(label=lbl, count=20, bulk_max=6, compress=False)

        dir = path.join(TestGenerator.OUTPUT_ADR, lbl)
        self.assertTrue(os.path.exists(dir))
        self.assertTrue(os.path.exists(path.join(dir, f"{BasicCommunication.NAME}.csv")))

    def test_generate_super_smallbulk(self):
        lbl = "0-size-s-10,6"

        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
        generator.generate(label=lbl, count=10, bulk_max=6, compress=False)

        dir = path.join(TestGenerator.OUTPUT_ADR, lbl)
        self.assertTrue(os.path.exists(dir))
        self.assertTrue(os.path.exists(path.join(dir, f"{BasicCommunication.NAME}.csv")))

    def test_generate_bigbulk(self):
        lbl = "0-size-2000,2000"

        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR, TestGenerator.OUTPUT_ADR)
        generator.generate(label=lbl, count=2000, bulk_max=2000, compress=False)

        dir = path.join(TestGenerator.OUTPUT_ADR, lbl)
        self.assertTrue(os.path.exists(dir))
        self.assertTrue(os.path.exists(path.join(dir, f"{BasicCommunication.NAME}.csv")))

    # TODO: Add batch size under limit, it will generate wrong dataset