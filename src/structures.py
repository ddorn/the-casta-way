import dataclasses
import json
from dataclasses import dataclass
from typing import List

from pygame import Vector2 as Vec

from src.constants import Files

@dataclass
class Elt:
    type: str
    pos: Vec

    @classmethod
    def load(cls, obj):
        cls(**obj)



class Structure:
    def __init__(self, name):
        self.elts: List[Elt] = []
        self.name = name

    def save(self):
        file = Files.STRUCTURE / (self.name + ".s")

        j = {
            "name": self.name,
            "objs": [dataclasses.asdict(o) for o in self.elts]
        }

        json.dump(j, file)

    @classmethod
    def load(cls, path):
        d = json.load(path)
        name = d["name"]
        elts = [Elt.load(o) for o in d["objs"]]

        struct = cls(name)
        struct.elts = elts

        return Structure





