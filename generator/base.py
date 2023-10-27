import datetime
import json
from io import TextIOWrapper

import pandas as pd
import numpy as np
import os
import time


class Base:

    MAX_DATE=datetime.date(2200,1,1)

    def __init__(self, path, gmodel, definition_file):
        self._create(path, definition_file)
        self._gen = np.random.default_rng()
        self.gmodel = gmodel
        self._name = definition_file

    @property
    def Name(self):
        return None

    def rnd_int(self, low, high):
        return self._gen.integers(low, high, 1)

    def rnd_choose(self, items: list=[], probability: list=None):
        """
        Generate random value from list and based on defined probabilities

        :param items:        item for selection
        :param probability:  probability items (total sum is 1, sample [0.5, 0.1, 0.1, 0.3]
        :return:             selected value
        """
        return self._gen.choice(items, size=1, p=probability)[0]

    def clean(self):

        for key in self.model.keys():
            self.model[key]=[]

    def _create(self, path, definition_file):

        self.model = {}
        with open(os.path.join(path, definition_file+".json"), "r") as json_file:
            definition = json.load(json_file)


        # create entities
        for entity in definition['spec']['entities']:
            self.model[entity['name']]=[]

        # create features
        for feature in definition['spec']['features']:
            self.model[feature['name']]=[]

    def generate(self, count):
        pass

    def save(self, append: bool, dir: str, compress: bool):

        path=os.path.join("02-data",dir)
        if not os.path.exists(path):
            os.mkdir(path)

        print(f"Creating: {'APPEND' if append else 'WRITE'}, name: '{self._name}', dir: '{dir}'...")
        df=pd.DataFrame(self.model)
        if compress:
            # start time
            start_time = time.time()

            compression_opts = dict(method='gzip')
            df.to_csv(os.path.join(path,f"{self._name}.csv.gz"),
                      header=False if append else True,
                      index=False,
                      mode="a" if append else "w",
                      encoding='utf-8',
                      sep=";",
                      decimal=",",
                      compression=compression_opts)
            # stop time
            diff_time=time.time()-start_time
            print(f"Duration: {round(diff_time,6)} seconds ({datetime.timedelta(seconds=diff_time)})")

#             # start time
#             start_time = time.time()
#             df.to_parquet(os.path.join(path,f"{self._name}.parquet"),
#                           engine="pyarrow",
#                           compression='gzip',
# #                          header=False if append else True,
#                           index=False,
#                           mode = "a" if append else "w")
#             # stop time
#             diff_time=time.time()-start_time
#             print(f"Duration: {round(diff_time,6)} seconds ({datetime.timedelta(seconds=diff_time)})")

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

        print(f"... Done")
        del df

