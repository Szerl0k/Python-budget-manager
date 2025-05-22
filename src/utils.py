import json
import os


class SerializationHandler:
    def __init__(self, path: str="/data/test_data.json"):
        self.path = path

        @property
        def path(self):
            return self._path

        @path.setter
        def path(self, path: str):
            self._path = path


    def deserialize(self):
        if not os.path.isfile(self.path):
            raise FileNotFoundError("File to deserialize does not exist!")

        result = dict()

        with open(self.path, "r") as outfile:
            result = json.load(outfile)

        return result

    def serialize(self, data: list):

        data = [t.to_dict() for t in data]

        with open(self.path, "w") as outfile:
            json.dump(data, outfile, indent=2)