from __future__ import annotations

from dataclasses import dataclass, field
from random import choice as rand_choice
from random import randint
from typing import Optional

from .CogGlobals import COG_ATTRIBUTES, get_cog_vitals
from .Entity import Entity


@dataclass
class Cog(Entity):
    key: str
    relative_level: Optional[int] = field(default=0)

    # Prevent needing to pass in Attack's required arguments
    # Instead, pass in the required arguments during __post_init__()
    name: str = field(init=False)
    hp: int = field(init=False)
    # # For testing purposes. See `test_cog_attack_damages_multiple_toons`

    def __post_init__(self):
        self.vitals = get_cog_vitals(cog_key=self.key,
                                     relative_level=self.relative_level)
        self.name = self.vitals['name']
        self.hp_max = self.vitals['hp']

        super().__init__(name=self.name, hp=self.hp_max)
        self.attacks = self.vitals['attacks']
        self.defense = self.vitals['def']
        self.level = self.vitals['level']

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'lvl {self.level} "{self.name}" ({self.hp}/{self.hp_max}hp)'


def get_random_cog() -> Cog:

    cog_key = rand_choice(list(COG_ATTRIBUTES.keys()))
    relative_level = randint(0, 4)
    return Cog(key=cog_key, relative_level=relative_level)
