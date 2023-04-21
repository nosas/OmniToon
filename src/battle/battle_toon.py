from dataclasses import dataclass, field
from typing import List

from src.factories.attack_factory import create_toon_attack
from src.core.toon import Toon
from src.gags.gag import Gag
from src.gags.gag_globals import TRACK

from .attack import Attack
from .battle_entity import BattleEntity


@dataclass
class BattleToon(BattleEntity):
    entity: Toon

    # Initialize default values for all properties
    _entity: Toon = field(init=False, repr=False)
    _battle: object = field(default=None, init=False, repr=False)

    @property
    def battle(self):
        return self._battle

    def leave_battle(self) -> None:
        self._battle = None

    def join_battle(self, new_battle) -> None:
        self._battle = new_battle

    @property
    def entity(self) -> Toon:
        return self._entity

    @entity.setter
    def entity(self, new_entity: Toon) -> None:
        if not isinstance(new_entity, Toon):
            raise ValueError("BattleToon.entity must be of type Toon")
        self._entity = new_entity

    @property
    def available_gags(self) -> List[Attack]:
        """Return a list of available Gags which can be used to attack a target"""
        return self.entity.gags.available_gags

    @staticmethod
    def _gag_is_possible(gag: Gag, target: BattleEntity) -> bool:
        """Return True if the Gag can be used against the target, regardless if there's a reward
        Certain Gags cannot be used against BattleCogs. For example...
            - a Lure Gag cannot be used against a Lured Cog
                UNLESS, there are other non-Lured Cogs in the Battle
            - a Trap Gag cannot be used against a Lured/Trapped Cog
                UNLESS, there are other non-Trapped Cogs in the Battle
            - a Heal (Toon-Up) Gag cannot be used against a Cog
        Args:
            gag (Gag): Gag object from the BattleToon.entity.gags
            target (BattleCog): BattleCog object to be attacked
        Returns:
            bool: True if the Gag can be used against the target
        """
        impossible_rules = [
            gag.track == TRACK.HEAL,
            target.is_lured and gag.track == TRACK.LURE,
            target.is_lured and gag.track == TRACK.TRAP,
            target.is_trapped and gag.track == TRACK.TRAP,
        ]
        return any(impossible_rules) is False

    def _gag_is_viable(self, gag: Gag, target: BattleEntity) -> bool:
        """Return True if the Gag is possible and provides a reward
        Viable Gags are possible to use against the target and provide a rewards because the
        level of the Gag is lower than the target.
        Args:
            gag (Gag): Gag object from the BattleToon.entity.gags
            target (BattleCog): BattleCog object to be attacked
        Returns:
            bool: True if the Gag can be used against the target and provides a reward
        """
        unviable_rules = [
            self._gag_is_possible(gag=gag, target=target) is False,
            gag.level >= target.level,
        ]
        return any(unviable_rules) is False

    def get_possible_attacks(self, target: BattleEntity) -> List[Attack]:
        """Return a list of possible attacks against a BattleCog target, ignore EXP reward
        Trap Gags are not returned against a Lured/Trapped Cog.
        Lure Gags are not returned against a Lured Cog.
        Args:
            target (BattleCog): BattleCog to be attacked
        Returns:
            List[ToonAttack]: List of possible attacks againt target, ignores EXP reward
        """
        possible_attacks = []
        for gag in self.available_gags:
            if self._gag_is_possible(gag=gag, target=target):
                attack = create_toon_attack(gag=gag)
                possible_attacks.append(attack)

        return possible_attacks

    def get_viable_attacks(self, target: BattleEntity) -> List[Attack]:
        """Return a list of viable attacks against a BattleCog target, weigh EXP rewards
        Trap Gags are not returned against a Lured/Trapped Cog.
        Lure Gags are not returned against a Lured Cog.
        Args:
            target (BattleCog): BattleCog to be attacked
        Returns:
            List[ToonAttack]: List of viable attacks againt target, weigh EXP rewards
        """
        possible_attacks = self.get_possible_attacks(target=target)
        return [
            attack for attack in possible_attacks if attack.gag.level < target.level
        ]

    def choose_action(self):
        return super().choose_action()
