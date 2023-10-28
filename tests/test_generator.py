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
        if os.path.split(os.getcwd())[-1]!="tests":
            os.chdir("tests")
            print(f"!!! Change directory for test execution to '{os.getcwd()}' !!!")
        shutil.rmtree(TestGenerator.OUTPUT_ADR, True)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_generate_data(self):
        generator = SyntheticData(os.path.join("..","01-model"),TestGenerator.OUTPUT_ADR)

        generator.generate(label="0-size-100", count=100, bulk_max=100, compress=True)
        generator.generate(label="1-size-1K", count=1000, bulk_max=1000, compress=True)

#        self.assertFalse(False)

