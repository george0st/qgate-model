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

        self.none_values=Setup.none_values
        self.none_values_probability=Setup.none_values_probability

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
            self._parquet_writer = None

    def save(self, path, dir: str, compress: bool):

        if len(self.model)==0:
            return

        path=os.path.join(path, dir)
        if not os.path.exists(path):
            os.makedirs(path)

        setup=Setup()

        df=pd.DataFrame(self.model)
        compression_opts = 'gzip' if compress else None

        # write CSV
        output_csv = os.path.join(path, f"{self.name}.csv.gz" if compress else f"{self.name}.csv")
        append_csv=False if (self._parquet_writer is None) else True
        df.to_csv(output_csv,
                  header=False if append_csv else True,
                  index=False,
                  mode="a" if append_csv else "w",
                  encoding='utf-8',
                  sep=setup.csv_separator,
                  decimal=setup.csv_decimal,
                  compression=compression_opts)

        # write parquet
        table = pa.Table.from_pandas(df)
        if self._parquet_writer is None:
            self._parquet_writer = pq.ParquetWriter(os.path.join(path, f"{self.name}.parquet"), table.schema, compression=compression_opts)
        self._parquet_writer.write_table(table=table)

        # free memory
        del df

    def add_none_value(self, current_value, default_value):
        """Change default value to None, based on project setting (see setting in model.json,
         config values 'NONE_VALUES' and 'NONE_VALUES_PROBABILITY')"""
        if self.none_values:
            if current_value == default_value:
                if self.rnd_bool(self.none_values_probability):
                    return default_value
        return current_value

