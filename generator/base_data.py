import datetime
import json
import pandas as pd
import numpy as np
import os
from generator.base import Base
from generator.setup import Setup
import pyarrow as pa
import pyarrow.parquet as pq



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
        self._parquet_writer = None

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

    def close(self):
        if self._parquet_writer:
            self._parquet_writer.close()

    def save(self, path, append: bool, dir: str, compress: bool):

        if len(self.model)==0:
            return

        path=os.path.join(path, dir)
        if not os.path.exists(path):
            os.makedirs(path)

        setup=Setup()

        # print(f"Creating: {'APPEND' if append else 'WRITE'}, name: '{self.name}', dir: '{dir}'...")
        df=pd.DataFrame(self.model)
        compression_opts = 'gzip' if compress else None
        output_csv = f"{self.name}.csv.gz" if compress else f"{self.name}.csv"

        df.to_csv(os.path.join(path, output_csv),
                  header=False if append else True,
                  index=False,
                  mode="a" if append else "w",
                  encoding='utf-8',
                  sep=setup.csv_separator,
                  decimal=setup.csv_decimal,
                  compression=compression_opts)

        self._parquet_writer = self._append_to_parquet(df, os.path.join(path, f"{self.name}.parquet"), self._parquet_writer)

        del df

    def _append_to_parquet(self, dataframe, filepath=None, writer=None):
        """Method writes/append dataframes in parquet format.

        This method is used to write pandas DataFrame as pyarrow Table in parquet format. If the methods is invoked
        with writer, it appends dataframe to the already written pyarrow table.

        :param dataframe: pd.DataFrame to be written in parquet format.
        :param filepath: target file location for parquet file.
        :param writer: ParquetWriter object to write pyarrow tables in parquet format.
        :return: ParquetWriter object. This can be passed in the subsequent method calls to append DataFrame
            in the pyarrow Table
        """
        table = pa.Table.from_pandas(dataframe)
        if writer is None:
            writer = pq.ParquetWriter(filepath, table.schema)
        writer.write_table(table=table)
        return writer

