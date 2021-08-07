from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from .Attack import Attack


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


@dataclass
class BattleEntity(ABC):

    battle_id: int = field(hash=True)
    entity: Entity

    _attack: Attack = field(init=False, default=None)
    _targets: list[BattleEntity] = field(init=False, default=None)

    @property
    def entity(self) -> Entity:
        return self._entity

    @entity.setter
    @abstractmethod
    def entity(self, new_entity) -> None:
        if not isinstance(new_entity, Entity):
            raise ValueError("BattleEntity.entity must be of type Entity")
        self._entity = new_entity

    @property
    def attack(self) -> Attack:
        return self._attack

    @attack.setter
    def attack(self, new_attack: Attack) -> None:
        if not isinstance(new_attack, Attack):
            raise ValueError("BattleEntity.attack must be of type Attack")
        self._attack = new_attack

    @property
    def battle_id(self) -> int:
        return self._battle_id

    @battle_id.setter
    def battle_id(self, new_id: int) -> None:
        if not isinstance(new_id, int):
            try:
                new_id = int(new_id)
            except ValueError:
                raise ValueError("battle_id must be an integer")
        self._battle_id = new_id

    @property
    def hp(self) -> int:
        return self.entity.hp

    @property
    def name(self) -> str:
        return self.entity.name

    @property
    def is_defeated(self) -> bool:
        return self.entity.is_defeated

    def _get_attacked(self, amount: int):
        self.entity.hp -= amount

    def _get_healed(self, amount: int):
        self.entity.hp += amount

    @abstractmethod
    def choose_attack(self, target: BattleEntity):
        pass
