from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from src.core.cog_globals import get_cog_vitals
from src.core.entity import Entity


@dataclass
class Cog(Entity):
    key: str
    relative_level: Optional[int] = field(default=0)

    name: str = field(init=False)
    hp: int = field(init=False)

    def __post_init__(self):
        self.vitals = get_cog_vitals(
            cog_key=self.key, relative_level=self.relative_level
        )
        self.hp_max = self.vitals["hp"]
        super().__init__(name=self.vitals["name"], hp=self.vitals["hp"])

        self.attacks = self.vitals["attacks"]
        self.defense = self.vitals["def"]
        self.level = self.vitals["level"]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'lvl {self.level} "{self.name}" ({self.hp}/{self.hp_max}hp)'
