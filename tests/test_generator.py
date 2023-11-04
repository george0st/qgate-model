import os
import unittest
import time
from os import path
import shutil
from generator.synthetic_data import SyntheticData


class TestGenerator(unittest.TestCase):

    OUTPUT_ADR = "../tests_output/synthetic_data/"

    @classmethod
    def setUpClass(cls):
        # setup the same dir for different unit test execution
        if os.path.split(os.getcwd())[-1]!="tests":
            os.chdir("tests")
            print(f"!!! Change directory for test execution to '{os.getcwd()}' !!!")

        shutil.rmtree(TestGenerator.OUTPUT_ADR, True)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_generate_compress(self):
        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR)
        generator.generate(label="0-size-20,20-compress", count=20, bulk_max=20, compress=True)

    def test_generate_compress_smallbulk(self):
        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR)
        generator.generate(label="0-size-20,6-compress", count=20, bulk_max=6, compress=True)

    def test_generate(self):
        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR)
        generator.generate(label="0-size-200,20", count=200, bulk_max=20, compress=False)

    def test_generate_smallbulk(self):
        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR)
        generator.generate(label="0-size-20,6", count=20, bulk_max=6, compress=False)

    def test_generate_bigbulk(self):
        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR)
        generator.generate(label="0-size-2000,2000", count=2000, bulk_max=2000, compress=False)