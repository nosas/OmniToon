from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Entity:
    name: str = field(hash=True)
    hp: int

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, new_hp: int) -> None:
        if not isinstance(new_hp, int):
            try:
                new_hp = int(new_hp)
            except ValueError:
                raise ValueError(f"new_hp {new_hp!r} must be of type int!")
        self._hp = new_hp

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        if not isinstance(new_name, str):
            raise ValueError(f"new_name {new_name!r} must be of type str!")
        self._name = new_name

    @property
    def is_defeated(self) -> bool:
        return self.hp <= 0
