from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Union

from .AttackGlobals import ATK_TGT_UNKNOWN
from .Battle import BattleCog
from .Entity import BattleEntity
from .Gag import Gag


@dataclass
class Attack():

    name: str
    damage: int
    accuracy: int
    target: int = field(default=ATK_TGT_UNKNOWN)  # Multi or single-target


@dataclass
class CogAttack(Attack):

    # TODO: Add freq as an attribute

    def __repr__(self) -> str:
        return str(self.__dict__)


@dataclass(init=False)
class ToonAttack(Attack):

    def __init__(self, gag: Gag, target_cogs: Union[BattleEntity, List[BattleEntity]]):
        self.gag = gag
        super().__init__(
            name=self.gag.name,
            damage=self.gag.damage,
            accuracy=self.gag.accuracy,
            target=self.gag.target
        )

        self.target_cogs = target_cogs
        if isinstance(self.target_cogs, BattleCog):
            self.target_cogs = [self.target_cogs]

        # Trap-specific attributes used for tracking EXP rewards
        self._is_attack = False
        self._is_setup = False

    @property
    def is_attack(self) -> bool:
        return self._is_attack

    @is_attack.setter
    def is_attack(self, new_is_attack: bool) -> None:
        assert isinstance(new_is_attack, bool)

        print(f"                [>] is_attack : {self.is_attack} -> {new_is_attack} on {self}")  # noqa
        self._is_attack = new_is_attack

    @property
    def is_setup(self) -> bool:
        return self._is_setup

    @is_setup.setter
    def is_setup(self, new_is_setup: bool) -> None:
        assert isinstance(new_is_setup, bool)
        print(f"                [>] is_setup : {self.is_setup} -> {new_is_setup} on {self}")  # noqa
        self._is_setup = new_is_setup
