import dataclasses
import json
from dataclasses import dataclass
from typing import List

from pygame import Vector2 as Vec

from src.constants import Files
from src.entities.decor import Rock, Beer


@dataclass
class Elt:
    type: str
    pos: Vec

    @classmethod
    def load(cls, obj):
        return cls(**obj)

    @staticmethod
    def name_to_class(name):
        return {
            c.__name__: c
            for c in [Rock, Beer]
        }[name]

    @staticmethod
    def class_to_name(cls):
        return cls.__name__



class Structure:
    def __init__(self, name, elts):
        self.elts: List[Elt] = elts
        self.name = name

    def save(self):
        file = self.name_to_file(self.name)

        j = {
            "name": self.name,
            "objs": [dataclasses.asdict(o) for o in self.elts]
        }

        file.write_text(json.dumps(j))

    @staticmethod
    def name_to_file(name):
        return Files.STRUCTURE / (name + ".s")

    @classmethod
    def load(cls, name):
        s = cls.name_to_file(name).read_text()
        d = json.loads(s)
        name = d["name"]
        elts = [Elt.load(o) for o in d["objs"]]

        struct = cls(name, elts)

        return struct





