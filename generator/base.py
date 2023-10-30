import datetime
import json
import pandas as pd
import numpy as np
import os


class Base:

    MAX_DATE=datetime.date(2200,1,1)

    def __init__(self, path, gmodel, definition_file):
        self._create(path, definition_file)
        self.model=[]
        self._gen = np.random.default_rng()
        self.gmodel = gmodel
        self._name = definition_file

    @property
    def Name(self):
        pass

    def rnd_int(self, low, high) -> int:
        return self._gen.integers(low, high)

    def rnd_choose(self, items: list=[], probability: list=None):
        """
        Generate random value from list and based on defined probabilities

        :param items:        item for selection
        :param probability:  probability items (total sum is 1, sample [0.5, 0.1, 0.1, 0.3]
        :return:             selected value
        """
        return self._gen.choice(items, size=1, p=probability)[0]

    def clean(self):
        self.model.clear()

    def _create(self, path, definition_file):

        self._model_definition = {}
        path=os.path.join(path,"02-feature-set", definition_file+".json")

        with open(path, "r") as json_file:
            definition = json.load(json_file)

        # create entities
        for entity in definition['spec']['entities']:
            self._model_definition[entity['name']]=None

        # create features
        for feature in definition['spec']['features']:
            self._model_definition[feature['name']]=None

    def model_item(self) -> dict:
        """Return new empty item"""
        return self._model_definition.copy()

    def generate(self, count):
        pass

    def save(self, path, append: bool, dir: str, compress: bool):

        path=os.path.join(path, dir)
        if not os.path.exists(path):
            os.makedirs(path)

        # print(f"Creating: {'APPEND' if append else 'WRITE'}, name: '{self._name}', dir: '{dir}'...")
        df=pd.DataFrame(self.model)
        if compress:
            compression_opts = dict(method='gzip')
            df.to_csv(os.path.join(path,f"{self._name}.csv.gz"),
                      header=False if append else True,
                      index=False,
                      mode="a" if append else "w",
                      encoding='utf-8',
                      sep=";",
                      decimal=",",
                      compression=compression_opts)

#             df.to_parquet(os.path.join(path,f"{self._name}.parquet"),
#                           engine="pyarrow",
#                           compression='gzip',
# #                          header=False if append else True,
#                           index=False,
#                           mode = "a" if append else "w")

        else:
            df.to_csv(os.path.join(path,f"{self._name}.csv"),
                      header=False if append else True,
                      index=False,
                      mode="a" if append else "w",
                      encoding='utf-8',
                      sep=";",
                      decimal=",")

            # df.to_parquet(os.path.join(path,f"{self._name}.parquet"),
            #                            engine='fastparquet',
            #                            append=True if append else False,
            #                            compression = "snappy",
            #                            index = False)

            # df.to_parquet(os.path.join(path,f"{self._name}.parquet"),
            #                            engine="pyarrow",
            #               compression="snappy",
            #               index=False)

        del df

