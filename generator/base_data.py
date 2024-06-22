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

        self._none_values=Setup().none_values
        self._none_values_probability=Setup().none_values_probability

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

    def apply_none_value(self, current_collection, property_name, default_value, lower_probability=1, none_value=None):
        """Apply None value, in case that current value is default.
         It is based on project setting (see setting in file 'model.json',
         with config values 'NONE_VALUES' and 'NONE_VALUES_PROBABILITY')

         :param current_collection:     current value (e.g. model)
         :param property_name:          name of property in current collection (e.g. 'transaction-type')
         :param default_value:          default value (what can consider such as default value)
         :param none_value:             changed value, default is ''
         :param lower_probability:      the value 1 = the same probability, 0.5 = 50% of lower probability, default is 1
         """
        if current_collection[property_name] == default_value:
            if self._none_values:
                if self.rnd_bool(self._none_values_probability * lower_probability):
                    current_collection[property_name] = none_value

