from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from src.battle.attack import Attack
from src.core.entity import Entity


@dataclass
class BattleEntity(ABC):
    battle_id: int = field(hash=True)
    entity: Entity

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
    def choose_action(self, actions: list[Attack]):
        raise NotImplementedError
