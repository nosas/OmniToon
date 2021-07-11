from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Entity:
    name: str
    hp: int
    # TODO #25, Create Publisher object to push notifications

    # ! This will cause issues if 2+ Toons have the same name
    def __hash__(self) -> int:
        return hash(self.name)

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, new_hp: int) -> None:
        if not isinstance(new_hp, int):
            raise ValueError("new_hp must be of type int!")
        self._hp = new_hp

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        if not isinstance(new_name, str):
            raise ValueError("new_name must be of type str!")
        self._name = new_name

    @property
    def is_defeated(self) -> bool:
        return self.hp <= 0
