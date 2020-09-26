import dataclasses
import json
from dataclasses import dataclass
from typing import List

from pygame import Vector2 as Vec

from src.constants import Files, DEBUG_STRUCT
from src.entities import Entity
from src.entities.decor import Rock, Beer, Trunk, Bush, Bounce, Boost, Text, BoostDown, BoostUp

OBJECTS = [Rock, Beer, Trunk, Bush, Bounce, Boost, BoostDown, BoostUp]
"""Collection of objects in structures."""

@dataclass
class Elt:
    type: str
    pos: Vec

    @property
    def klass(self):
        return self.name_to_class(self.type)

    @classmethod
    def load(cls, obj):
        return cls(**obj)

    @staticmethod
    def name_to_class(name):
        return {
            c.__name__: c
            for c in OBJECTS
        }[name]

    @staticmethod
    def class_to_name(cls):
        return cls.__name__

    def spawn(self, pos):
        return self.klass(pos + self.pos)


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

        print(f"Saved {len(j['objs'])} objects to {file}.")

    @staticmethod
    def name_to_file(name):
        return Files.STRUCTURES / (name + ".s")

    @classmethod
    def load(cls, name):
        s = cls.name_to_file(name).read_text()
        d = json.loads(s)
        name = d["name"]
        elts = [Elt.load(o) for o in d["objs"]]

        struct = cls(name, elts)

        return struct

    def spawn(self, pos) -> List[Entity]:
        entities = [
            e.spawn(pos)
            for e in self.elts
        ]

        if DEBUG_STRUCT:
            entities.append(Text(pos - Vec(1, 1), self.name))

        return entities


    @property
    def width(self):
        return max(e.pos[0] for e in self.elts) # - min(e.pos[0] for e in self.elts)

    @property
    def height(self):
        return max(e.pos[1] for e in self.elts) # - min(e.pos[1] for e in self.elts)



