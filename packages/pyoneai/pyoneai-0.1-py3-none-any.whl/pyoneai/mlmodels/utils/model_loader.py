import pickle
from typing import Self

import joblib


class ModelLoader:

    def __init__(self, format: str):
        match format:
            case "pickle":
                self._loader = pickle.load
            case "joblib":
                self._loader = joblib.load
            case _:
                raise ValueError(f"{format} is not supported")

    def predict(self, x):
        return self._model.predict(x.reshape(1, len(x)))

    def load(self, path: str) -> Self:
        with open(path, "rb") as file:
            self._model = self._loader(file)
        return self
