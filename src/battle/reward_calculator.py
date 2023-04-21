from dataclasses import dataclass
from typing import List

from .attack import Attack
from .attack_globals import MULTIPLIER
from .battle_cog import BattleCog
from .toon_attack import ToonAttack


@dataclass
class RewardCalculator:
    building_floor: int = 1
    is_invasion: bool = False

    @property
    def base_reward(self) -> List[int]:
        return [1, 2, 3, 4, 5, 6, 7]

    @property
    def reward_table(self) -> List[int]:
        return [round(reward * self.get_multiplier()) for reward in self.base_reward]

    @property
    def multiplier_building(self) -> float:
        """Return the multipler value from being in a Cog Building"""
        return MULTIPLIER.get_building_multiplier_from_floor(floor=self.building_floor)

    @property
    def multiplier_invasion(self) -> float:
        """Return the multipler value from being in a Cog Building"""
        return MULTIPLIER.get_invasion_multiplier_from_bool(
            is_invasion=self.is_invasion
        )

    def get_multiplier(self) -> float:
        """Return the reward multiplier
        Returns:
            float: Value used to calculate a BattleToon's ToonAttack reward
        """
        return self.multiplier_building * self.multiplier_invasion

    def get_base_reward(self, attack: ToonAttack) -> int:
        """Return the base reward of a Gag
        Args:
            attack (ToonAttack): BattleToon Attack containing that Gag and target BattleCog
        Returns:
            int: Base reward of a ToonAttack
        """
        return self.base_reward[attack.gag.level]

    def calculate_reward(self, attack: ToonAttack, target: BattleCog) -> int:
        """Calculate the BattleToon's reward, given a ToonAttack
        Return -1 if the Gag's level exceeds the target BattleCog's level, meaning the Gag is
        possible, but not viable.
        Return ((gag.level + 1) * multiplier) if the Gag's level is lower than the target's level.
        Args:
            attack (ToonAttack): BattleToon Attack containing that Gag and target BattleCog
        Returns:
            int: Skill points awarded for successfully landing the ToonAttack
        """
        if attack.gag.level >= target.level:
            return -1
        # Round upwards because the reward could be x.5
        return self.reward_table[attack.gag.level]
