import datetime
import json
import pandas as pd
import numpy as np
import os
from generator.base import Base


class BaseData(Base):

    MAX_DATE=datetime.date(2200,1,1)

    def __init__(self, path, gmodel, name):
        super().__init__()
        self._model_definition=Base.create(path, name)
        self.model=[]
        # self._gen = np.random.default_rng()
        self.gmodel = gmodel
        self._name = name
        self.clean()

    @property
    def name(self):
        return self._name

    def clean(self):
        self.model.clear()

    def model_item(self) -> dict:
        """Return new empty item"""
        return self._model_definition.copy()

    def generate(self, count):
        pass

    def save(self, path, append: bool, dir: str, compress: bool):

        path=os.path.join(path, dir)
        if not os.path.exists(path):
            os.makedirs(path)

        # print(f"Creating: {'APPEND' if append else 'WRITE'}, name: '{self.name}', dir: '{dir}'...")
        df=pd.DataFrame(self.model)
        if compress:
            compression_opts = dict(method='gzip')
            df.to_csv(os.path.join(path,f"{self.name}.csv.gz"),
                      header=False if append else True,
                      index=False,
                      mode="a" if append else "w",
                      encoding='utf-8',
                      sep=";",
                      decimal=",",
                      compression=compression_opts)

#             df.to_parquet(os.path.join(path,f"{self.name}.parquet"),
#                           engine="pyarrow",
#                           compression='gzip',
# #                          header=False if append else True,
#                           index=False,
#                           mode = "a" if append else "w")

        else:
            df.to_csv(os.path.join(path,f"{self.name}.csv"),
                      header=False if append else True,
                      index=False,
                      mode="a" if append else "w",
                      encoding='utf-8',
                      sep=";",
                      decimal=",")

            # df.to_parquet(os.path.join(path,f"{self.name}.parquet"),
            #                            engine='fastparquet',
            #                            append=True if append else False,
            #                            compression = "snappy",
            #                            index = False)

            # df.to_parquet(os.path.join(path,f"{self.name}.parquet"),
            #                            engine="pyarrow",
            #               compression="snappy",
            #               index=False)

        del df

