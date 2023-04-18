from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from src.core.entity import Entity
from src.core.toon_globals import (DEFAULT_BEAN_COUNT, DEFAULT_BEAN_LIMIT,
                                   DEFAULT_HP)
from src.gags.gag import Gags
from src.gags.gag_globals import DEFAULT_GAG_LIMIT


@dataclass
class Inventory:
    """Represent Toon's inventory, such as Gags, Jellybeans, SOS cards, etc.

    Args:
        gags (Gags): Gags objects containing Toon's Gag count, exp, levels.
            Defaults to Gags objects without arguments (lvl 0 Throw and lvl 0 Squirt only)
        jellybeans (int): Toon's current number of jellybeans.
            Defaults to DEFAULT_BEAN_COUNT
        max_jellybeans (int, optional): Toon's maximum jellybean capacity.
            Defaults to DEFAULT_BEAN_LIMIT
        max_gags (int. optional): Toon's maximum Gag capacity.
            Defaults to DEFAULT_GAG_LIMIT
    """
    gags: Optional[Gags] = field(default_factory=Gags)
    jellybeans: Optional[int] = field(default=DEFAULT_BEAN_COUNT)

    max_jellybeans: Optional[int] = field(default=DEFAULT_BEAN_LIMIT)
    max_gags: Optional[int] = field(default=DEFAULT_GAG_LIMIT)

    def has_gags(self) -> bool:
        """True if Toon has any available Gags, checks quantity of all Gags

        Returns:
            bool: True if Toon has any available Gags
        """
        return len(self.gags.available_gags) != 0


@dataclass
class Toon(Entity):
    """Toon base class, contains an inventory with jellybeans and Gags

    Args:
        name (str): Name of the Toon
        hp (int, optional): Laff-o-Meter (health points) of a Toon.
            Defaults to DEFAULT_HP (15)
        inventory (Inventory): Toon's inventory, such as Gags, Jellybeans, SOS cards, etc.
            Defaults to Inventory() factory with no gags, default limits, etc.
    """

    inventory: Inventory = field(default_factory=Inventory)
    hp: Optional[int] = field(default=DEFAULT_HP)

    def __post_init__(self):
        super().__init__(name=self.name, hp=self.hp)
        self.hp_max = self.hp

    def __str__(self):
        return f'"{self.name}" ({self.hp}/{self.hp_max}hp)'

    @property
    def gags(self) -> Gags:
        return self.inventory.gags

    def has_gags(self) -> bool:
        """True if Toon has any available Gags, checks quantity of all Gags

        Returns:
            bool: True if Toon has any available Gags
        """
        return self.inventory.has_gags()
