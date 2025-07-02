import json
import os


class Singleton (type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Setup(metaclass=Singleton):

    def __init__(self, model_path):
        self._model_setting={}

        with open(os.path.join(model_path, "model.json"), "r") as json_file:
            setting = json.load(json_file)

        self._model_setting=setting["spec"]

    @property
    def csv_separator(self):
        return self._model_setting["CSV_SEPARATOR"]

    @property
    def csv_decimal(self):
        return self._model_setting["CSV_DECIMAL"]

    @property
    def none_values(self):
        """Allow to generate None values (True - generate None values)"""
        return self._model_setting["NONE_VALUES"]

    @property
    def none_values_probability(self):
        """Probability of None value generation (1 = 100%, 0.1 = 10%, etc.)"""
        return self._model_setting["NONE_VALUES_PROBABILITY"]

    @property
    def data_hint_amount(self):
        """Amount of generated data hints"""
        return self._model_setting["DATA_HINT_AMOUNT"]
