from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Union

from .Attack import Attack
from .Exceptions import (InvalidAttackType, InvalidTargetError,
                         TargetDefeatedError)


@dataclass
class Entity:

    name: str = field(hash=True)
    hp: int

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, new_hp: int) -> None:
        # TODO try casting new_hp to int if it's a str or float
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
class BattleEntity(Entity):

    battle_id: int = field(hash=True)
    _attack: Attack = field(init=False, default=None)
    _targets: list[BattleEntity] = field(init=False, default=None)

    def __post_init__(self):
        super().__init__(name=self.name, hp=self.hp)

    @property
    def attack(self) -> Attack:
        return self._attack

    @attack.setter
    def attack(self, new_attack: Attack) -> None:
        if not isinstance(new_attack, Attack):
            raise InvalidAttackType
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
                raise TypeError("battle_id must be an integer")
        self._battle_id = new_id

    @property
    def targets(self) -> list[BattleEntity]:
        return self._targets

    @targets.setter
    def targets(self, new_targets: Union[BattleEntity | List[BattleEntity]]) -> None:
        # If passed in a single target, add the target to an empty list
        if isinstance(new_targets, BattleEntity):
            new_targets = [new_targets]
        if not isinstance(new_targets, list):
            raise InvalidTargetError("Targets must be a list of BattleEntities")
        if len(new_targets) > 4:
            raise Exception("Cannot have more than 4 targets")

        for target in new_targets:
            if not isinstance(target, BattleEntity):
                raise InvalidTargetError("Target must be a subclass of BattleEntity")
            if type(target) == type(self) or target == self:
                raise InvalidTargetError("Target must not be one self or of the same type")
            if target.is_defeated:
                raise TargetDefeatedError(f"Cannot attack defeated {type(target)}")

        self._targets = new_targets

    def _get_attacked(self, amount: int):
        self.hp -= amount

    def _get_healed(self, amount: int):
        self.hp += amount

    def do_attack(self, overdefeat: bool = False, force_miss: bool = False) -> bool:
        # TODO #10, Add chance_to_hit
        attack_hit = False if force_miss else True
        hit_miss = 'misses'
        damage = 0

        if attack_hit:
            hit_miss = 'hits'
            damage = self.attack.damage

        for target in self.targets:
            if target.is_defeated and overdefeat is False:
                # Multiple Toons attack the same Cog with the same Gag track
                raise TargetDefeatedError(f"Cannot attack defeated {type(target)}")

            target_hp_before = target.get_hp()
            target._get_attacked(amount=damage)
            class_name = self.__class__.__name__
            # TODO Add attack name and object name
            print(f"            [-] {class_name} `do_attack()` {self} "
                  f"{self.attack.name} {hit_miss} {target} -> {target_hp_before}hp-"
                  f"{damage}dmg")

        return attack_hit
