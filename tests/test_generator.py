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
        generator.generate(label="0-size-10-compress", count=10, bulk_max=10, compress=True)

    def test_generate_compress_smallbulk(self):
        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR)
        generator.generate(label="0-size-10,3-compress", count=10, bulk_max=3, compress=True)

    def test_generate(self):
        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR)
        generator.generate(label="0-size-10", count=10, bulk_max=10, compress=False)

    def test_generate_smallbulk(self):
        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR)
        generator.generate(label="0-size-10,3", count=10, bulk_max=3, compress=False)
