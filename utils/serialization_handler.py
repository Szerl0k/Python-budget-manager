import json
import os
from json import JSONDecodeError

from models.transaction import Transaction


class SerializationHandler:
    def __init__(self, path: str=""):
        self.path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path: str):
        self._path = "data/"+path


    def deserialize(self):
        if not os.path.isfile(self.path):
            raise FileNotFoundError("File to deserialize does not exist!")

        try:
            with open(self.path, "r") as outfile:
                data = json.load(outfile)
        # w przypadku jak json jest pusty
        except JSONDecodeError:
            return []

        # Mapujemy każdy element na Transakcję i wrzucamy do listy wynikowej
        result = list()
        for t in data:
            result.append(Transaction.from_json(t))
        return result

    def serialize(self, data: list):

        # Mapujemy każdą transakcję jako dict
        data = [t.to_dict() for t in data]

        with open(self.path, "w") as outfile:
            json.dump(data, outfile, indent=2)