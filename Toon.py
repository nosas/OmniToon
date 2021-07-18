from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .Entity import Entity
from .Gag import Gags
from .GagGlobals import DEFAULT_GAG_LIMIT

DEFAULT_BEAN_COUNT = 0
DEFAULT_BEAN_LIMIT = 40
DEFAULT_HP = 15


@dataclass
class Inventory:

    gags: Gags = field(default_factory=Gags)
    jellybeans: int = field(default=DEFAULT_BEAN_COUNT)

    max_jellybeans: int = field(default=DEFAULT_BEAN_LIMIT)
    max_gags: Optional[int] = field(default=DEFAULT_GAG_LIMIT)

    # TODO #38, We should move this to Strategy, when we make Strategies.
    # TODO #38, Make sure to check against the highest level Cog in the battle
    # However, if the Cog being attacked is at a lower level than the gag,
    # then the toon will receive no skill points.
    # https://toontown.fandom.com/wiki/Skill_points#Earning_skill_points

    def has_gags(self) -> bool:
        """True if Toon has any available Gags, checks quantity of all Gags

        Returns:
            bool: True if Toon has any available Gags
        """
        # [[0]*7]*7 == 2-D list, 7x7, initialized with 0's
        # Return True if the 2-D list is NOT empty, aka Toon has Gags
        # return self.gags != [[0]*7]*7
        return self.gags._count_all_gags() != 0


@dataclass
class Toon(Entity):
    """Toon object class

    Args:
        name (str): Name of the Toon
        hp (int, optional): Laff-o-Meter (health points) of a Toon
        gags (list, optional): 2-D list, ex: `gags[GAG_TRACK][GAG]`.
            Defaults to DEFAULT_GAGS.
            Example `gags` ::
                gags = [[0,   0,  0,  5,  5,  3, -1],  # 0 Toon-up
                        [-1, -1, -1, -1, -1, -1, -1],  # 1 Trap (locked)
                        [0,   0,  0,  0,  5,  3,  1],  # 2 Lure
                        [0,   0,  0,  0,  5,  3, -1],  # 3 Sound
                        [0,   2,  1,  4,  4,  2, -1],  # 4 Throw
                        [0,   0,  0,  5,  5,  3, -1],  # 5 Squirt
                        [0,   9,  5, -1, -1, -1, -1]]  # 6 Drop

        gag_exps (list, optional): List containing Gag track EXP.
            Defaults to DEFAULT_EXPS.
            Example `gag_exps` ::
                gag_exps = [7421,   # 0 Toon-up
                            0,      # 1 Trap (locked)
                            10101,  # 2 Lure
                            9443,   # 3 Sound
                            8690,   # 4 Throw
                            6862,   # 5 Squirt
                            191]    # 6 Drop

        gag_levels (list, optional): List containing Gag track levels.
            Defaults to DEFAULT_LEVELS.
            Example `gag_levels` ::
                gag_levels = [5,   # 0 Toon-up
                                -1,  # 1 Trap (locked)
                                6,   # 2 Lure
                                5,   # 3 Sound
                                5,   # 4 Throw
                                5,   # 5 Squirt
                                2]   # 6 Drop

        gag_limit (int, optional): Maximum number of Gags a Toon can carry.
            Defaults to DEFAULT_GAG_LIMIT.
    """

    inventory: Inventory = field(default_factory=Inventory)
    hp: Optional[int] = field(default=DEFAULT_HP)

    def __post_init__(self):
        super().__init__(name=self.name, hp=self.hp)

    def __str__(self):
        return f'"{self.name}" ({self.hp}/{self.hp_max}hp)'

    def __repr__(self):
        return self.__str__()
