# %% Import functions and classes
from .Entity import Entity
from .Cog import Cog
from .Gag import Gag
from .GagGlobals import LEVELS, count_all_gags, get_gag_track_name

DEFAULT_HP = 15
DEFAULT_LEVELS = [-1, -1, -1, -1, 0, 0, -1]
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
    def __init__(self, name, hp=DEFAULT_HP, gags=DEFAULT_GAGS,
                 gag_exps=DEFAULT_EXPS, gag_levels=DEFAULT_LEVELS,
                 gag_limit=DEFAULT_GAG_LIMIT):
        """Toon object class

        Args:
            name (str): Name of the Toon
            hp (int, optional): Laff-o-Meter of a toon
            # ? Gags = 2-D list : [type?][type?].. 2D array of type Gag or int?
            # ! Create Gags object, remove 2-D list and replace with Gags obj
            # ! Toon.gags = Gags(toons_gags=2-D list)
            # ! Toon.gags.get_gag(gtype="throw", level=<1-7|0-6>)
            gags (list, optional): 2-D array, ex: `[GAG_TRACK][GAG]`. Defaults
                to DEFAULT_GAGS.
            gag_exps ([type], optional): [description]. Defaults to DEFAULT_EXPS.
            gag_levels ([type], optional): [description]. Defaults to DEFAULT_LEVELS.
            gag_limit ([type], optional): [description]. Defaults to DEFAULT_GAG_LIMIT.
        """  # noqa
        self.name = name
        self.hp = hp
        self.gag_limit = gag_limit

        # Verify total Gag count in `gags` doesn't exceed `gag_limit`
        # ! Raises AssertionError if Gag count exceeds `gag_limit`
        self.gags = gags
        if self.__count_all_gags() > gag_limit:
            self.gags = DEFAULT_GAGS

        self.gag_levels = gag_levels
        self.gag_exps = gag_exps

    def __count_all_gags(self) -> int:
        count = count_all_gags(gags=self.gags)

        assert count <= self.gag_limit, (
            f"Gag quantity ({count}) exceeds Toon's ({self.name}) gag limit "
            f"({self.gag_limit})."
            )
        return count

    def choose_gag(self, gag_track: int, gag_level: int) -> Gag:
        gag_exp = self.get_gag_exp(gag_track)
        gag = Gag(track=gag_track, exp=gag_exp, level=gag_level)

        assert self.has_gag(gag_track=gag.track, gag=gag.level), (
            f"Toon \"{self.name}\" does not have any lvl {gag.level} "
            f"{gag.track_name} gags \"{gag.name}\"."
            )

        return(gag)

    def count_gag(self, gag_track: int, gag_level: int) -> int:
        return self.gags[gag_track][gag_level]

    def do_attack(self, target: Cog, gag_track: int, gag_level: int) -> None:
        # Need to calculate Attack accuracy, wrong to assume attacks always hit
        #                   atkAcc = propAcc + trackExp + tgtDef + bonus
        # https://toontownrewritten.fandom.com/wiki/Accuracy#propAcc
        # When Trap gag is used, atkAcc is  set to 100, and atkHit is set to 1.
        # For all other gags, if atkAcc exceeds 95, it will be reduced to 95.
        # TODO: Create InvalidGagTargetError
        assert type(target) == Cog, (
            f"Toon \"{self.name}\" tried to attack a non-Cog object:"
            f"{type(target)}"
        )

        try:
            gag = self.choose_gag(gag_track=gag_track, gag_level=gag_level)
        # TODO: Create NotEnoughGagsError, LockedGagError, TooManyGagsError
        # These errors should be caught and tested in func `choose_gag`
        except AssertionError as e:
            gag_track_name = get_gag_track_name(gag_track=gag_track)
            # assert self.has_gag(gag_track=gag_track, gag=gag_level), (
            print(f"Toon \"{self.name}\" tried to attack with lvl {gag_level} "
                  f"{gag_track_name} ({gag_track}) gag_track, but lacks"
                  " number of available gags "
                  f"{self.count_gag(gag_track=gag_track, gag=gag_level)}")
            raise e

        self.gags[gag_track][gag_level] -= 1

        if super().do_attack(target=target, amount=gag.damage):
            # TODO : Return 1 if hit, 0 if miss? Must be done in Entity class
            # TODO : If attack hits, add EXP to gag track
            # TODO : Add EXP multiplier (cog building, invasions)
            self.gag_exps[gag_track] += gag_level

    def get_gag_exp(self, gag_track: int) -> int:
        # ? Should I change this to use `get_gag_exp` from GagGlobals?
        return self.gag_exps[gag_track]

    def get_viable_attacks(self, target: Cog) -> list:
        """Return 2-D list of Gags that can be used and gain Gag
            A Gag is viable if its level is at or below the Cog's level.

        Args:
            target (Cog): Cog object that is going to be attacked

        Returns:
            list: 2-D list of Gags. 0 means the Gag is not available or
                  does not gain Gag EXP when used. If all Gags are unviable,
                  it will return the a list of the Toon's Gags.
        """
        # However, if the Cog being attacked is at a lower level than the gag,
        # then the toon will receive no skill points.
        # https://toontown.fandom.com/wiki/Skill_points#Earning_skill_points
        # TODO : Make sure to check against the highest level Cog in the battle
        # TODO : Add attributes to Gags to determine if valid/invalid/locked
        if target.level >= 7:
            return self.gags
        elif target.level >= 0:
            viable_gags = [
                gag_track for gag_track in self.gags[0:target.level]
            ]
            return viable_gags
        else:
            print(f"[!] What the heck is the Cog's level? {target.attrs}")

    def has_gag(self, gag_track: int, gag: int) -> bool:
        # ! Should also check if gag is unlocked yet, not just quantity.
        return self.count_gag(gag_track, gag) != 0

    def has_gags(self) -> bool:
        # [[0]*7]*7 == 2-D list, 7x7, initialized with 0's
        # Return True if the 2-D list is NOT empty, aka Toon has Gags
        # return self.gags != [[0]*7]*7
        return self.__count_all_gags() != 0


# name = "Astro"
# hp = "65"
# levels = [5, 0, 6, 5, 5, 5, 2]
# exps = [7421, 0, 10101, 9443, 8690, 6862, 191]

# # TODO Create proper test for Toon object creation
# gag_labels = ["Toon-Up", "Trap", "Lure", "Sound", "Throw", "Squirt", "Drop"]
# # gags = [[1]*7] + [[0]*7]*6  # 7 total Gags
# gags = [[10]*7] + [[0]*7]*6   # 70 total Gags
# gag_limit = 70    # Expect pass
# # gag_limit = 71  # Expect pass
# # gag_limit = 69  # Expect failure
# my_toon = Toon(name=name, hp=hp, gags=gags, gag_limit=gag_limit,
#                gag_levels=levels, gag_exps=exps)


# num_all_gags = count_all_gags(my_toon.gags)
# print(f"Toon {name} has Gags? {my_toon.has_gags()} {num_all_gags}")

# has_gag = my_toon.has_gag(gag_track=0, gag=0)
# num_gags = my_toon.count_gag(gag_track=0, gag=0)
# print(f"Toon {name} has Toon-Up Gag? {has_gag} {num_gags}")
