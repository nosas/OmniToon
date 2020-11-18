from Entity import Entity
from Cog import Cog
from Gag import Gag
from GagGlobals import (
    LEVELS, get_gag_carry_limits, get_gag_damage
)

DEFAULT_LEVELS = [0, 0, 0, 0, 1, 1, 0]
# DEFAULT_EXPS = [0, 0, 0, 0, 10, 10, 0]
# Populate DEFAULT_EXP from Gag track levels in DEFAULT_LEVELS
DEFAULT_EXPS = [LEVELS[idx][level] for idx, level in enumerate(DEFAULT_LEVELS)]
DEFAULT_GAGS = [[0, 0, 0, 0, 0, 0, 0],  # Toon-Up
                [0, 0, 0, 0, 0, 0, 0],  # Trap
                [0, 0, 0, 0, 0, 0, 0],  # Lure
                [0, 0, 0, 0, 0, 0, 0],  # Sound
                [0, 0, 0, 0, 0, 0, 0],  # Throw
                [0, 0, 0, 0, 0, 0, 0],  # Squirt
                [0, 0, 0, 0, 0, 0, 0]]  # Drop
DEFAULT_GAG_LIMIT = 20


class Toon(Entity):
    def __init__(self, name, health, gags=DEFAULT_GAGS, gag_exps=DEFAULT_EXPS,
                 gag_levels=DEFAULT_LEVELS, gag_limit=DEFAULT_GAG_LIMIT):
        """Toon object class

        Args:
            name (str): Name of the Toon
            health (int): Laff-o-Meter of a toon
            gags (list, optional): 2-D array, ex: `[GAG_TRACK][GAG]`. Defaults
                to DEFAULT_GAGS.
            gag_exps ([type], optional): [description]. Defaults to DEFAULT_EXPS.
            gag_levels ([type], optional): [description]. Defaults to DEFAULT_LEVELS.
            gag_limit ([type], optional): [description]. Defaults to DEFAULT_GAG_LIMIT.
        """  # noqa
        self.name = name
        self.health = health
        self.gags = gags  # ? Do we want a 2D array of type Gag or int?
        self.gag_levels = gag_levels
        self.gag_exps = gag_exps
        self.gag_limit = gag_limit

        # ? Possible States: Dead (0), Battle (1), Heal (2)
        # self.state = None

    def do_attack(self, target: Cog, gag: Gag) -> None:
        # TODO : Return 1 if hit, 0 if miss?

        super().do_attack(target=target, amount=gag.damage)
