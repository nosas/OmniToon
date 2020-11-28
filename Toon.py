# %% Import functions and classes
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


# TODO Figure out how to properly initialize an Object.
# ? AssertionErrors when? During initialization of attributes or separate func?
# ? Should I use @property decorators again?
class Toon(Entity):
    def __init__(self, name, health, gags=DEFAULT_GAGS, gag_exps=DEFAULT_EXPS,
                 gag_levels=DEFAULT_LEVELS, gag_limit=DEFAULT_GAG_LIMIT):
        """Toon object class

        Args:
            name (str): Name of the Toon
            health (int): Laff-o-Meter of a toon
            # ? Gags = 2-D list : [type?][type?].. 2D array of type Gag or int?
            gags (list, optional): 2-D array, ex: `[GAG_TRACK][GAG]`. Defaults
                to DEFAULT_GAGS.
            gag_exps ([type], optional): [description]. Defaults to DEFAULT_EXPS.
            gag_levels ([type], optional): [description]. Defaults to DEFAULT_LEVELS.
            gag_limit ([type], optional): [description]. Defaults to DEFAULT_GAG_LIMIT.
        """  # noqa
        self.name = name
        self.health = health
        self.gag_limit = gag_limit

        # Verify total Gag count in `gags` doesn't exceed `gag_limit`
        # ! Raises AssertionError if Gag count exceeds `gag_limit`
        if self.count_all_gags(gags) <= gag_limit:
            self.gags = gags

        self.gag_levels = gag_levels
        self.gag_exps = gag_exps

        # ? Possible States: Dead (0), Battle (1), Heal (2)
        # self.state = None

    def do_attack(self, target: Cog, gag: Gag) -> None:
        # TODO : Return 1 if hit, 0 if miss?

        super().do_attack(target=target, amount=gag.damage)

    def has_gag(self, gag_track: int, gag: int) -> bool:
        return self.count_gag(gag_track, gag) != 0

    def has_gags(self) -> bool:
        # [[0]*7]*7 == 2-D list, 7x7, initialized with 0's
        # Return True if the 2-D list is NOT empty, aka Toon has Gags
        # return self.gags != [[0]*7]*7
        # ! Raises AssertionError if Gag count exceeds `gag_limit`
        return self.count_all_gags(gags=self.gags) != 0

    # ? Do we want `count_all_gags` in Toon class method or GagGlobals.py func?
    def count_all_gags(self, gags: list = DEFAULT_GAGS) -> int:
        count = 0
        for gag_track in gags:
            for gag_quantity in gag_track:
                count += gag_quantity

        assert count <= gag_limit, (
            f"Gag quantity ({count}) exceeds Toon's ({self.name}) gag limit "
            f"({gag_limit})."
            )
        return count

    def count_gag(self, gag_track: int, gag: int) -> int:
        return self.gags[gag_track][gag]


name = "Astro"
health = "65"
levels = [5, 0, 6, 5, 5, 5, 2]
exps = [7421, 0, 10101, 9443, 8690, 6862, 191]

# TODO Create proper test for Toon object creation
gag_labels = ["Toon-Up", "Trap", "Lure", "Sound", "Throw", "Squirt", "Drop"]
# gags = [[1]*7] + [[0]*7]*6  # 7 total Gags
gags = [[10]*7] + [[0]*7]*6   # 70 total Gags
gag_limit = 70    # Expect pass
# gag_limit = 71  # Expect pass
# gag_limit = 69  # Expect failure
my_toon = Toon(name=name, health=health, gags=gags, gag_limit=gag_limit,
               gag_levels=levels, gag_exps=exps)


num_all_gags = my_toon.count_all_gags(my_toon.gags)
print(f"Toon {name} has Gags? {my_toon.has_gags()} {num_all_gags}")

has_gag = my_toon.has_gag(gag_track=0, gag=0)
num_gags = my_toon.count_gag(gag_track=0, gag=0)
print(f"Toon {name} has Toon-Up Gag? {has_gag} {num_gags}")
