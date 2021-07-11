from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Union

from .Attack import Attack
from .Exceptions import InvalidAttackType, InvalidTargetError, TargetDefeatedError


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
class BattleEntity:

    battle_id: int
    _attack: Attack = field(init=False, default=None)
    _targets: Union[BattleEntity | List[BattleEntity]] = field(init=False, default=None)

    @property
    def battle_id(self) -> int:
        return self._battle_id

    @battle_id.setter
    def battle_id(self, new_id: int) -> None:
        self._battle_id = new_id

    @property
    def targets(self) -> BattleEntity:
        return self._target

    @targets.setter
    def targets(self, new_targets: BattleEntity) -> None:
        # If passed in a single target, add the target to an empty list
        if isinstance(new_targets, BattleEntity):
            new_targets = [new_targets]
        if not isinstance(new_targets, list):
            raise InvalidTargetError("Targets must be a list of BattleEntities")

        for target in new_targets:
            if not isinstance(target, BattleEntity):
                raise InvalidTargetError("Target must be a subclass of BattleEntity")
            if type(target) == type(self):
                raise InvalidTargetError("Target must not be of the same type")
            if target.is_defeated:
                raise TargetDefeatedError(f"Cannot attack defeated {type(target)}")

        self._targets = new_targets

    @property
    def attack(self) -> Attack:
        return self._attack

    @attack.setter
    def attack(self, new_attack: Attack) -> None:
        if not isinstance(new_attack, Attack):
            raise InvalidAttackType
        self._attack = new_attack

    def __hash__(self) -> int:
        return hash((self.hp, self.name, self.battle_id))

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
            if self.targets.is_defeated and overdefeat is False:
                # Multiple Toons attack the same Cog with the same Gag track
                raise TargetDefeatedError(f"Cannot attack defeated {type(self.targets)}")

            target_hp_before = self.targets.get_hp()
            target._get_attacked(amount=damage)
            class_name = self.__class__.__name__
            # TODO Add attack name and object name
            print(f"            [-] {class_name} `do_attack()` {self} "
                  f"{self.attack.name} {hit_miss} {target} -> {target_hp_before}hp-"
                  f"{damage}dmg")

        return attack_hit
