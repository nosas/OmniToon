# %% Import functions and classes
from .Entity import Entity
from .Cog import Cog
from .Gag import Gag
from .GagGlobals import (
    LEVELS, LURE_TRACK, count_all_gags, get_gag_accuracy,
    get_gag_exp, get_gag_exp_needed
)

DEFAULT_HP = 15
# -1 means the gag_track is locked,0 means lvl 1 Gag is unlocked
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

        self.gags = gags
        # Verify total Gag count in `gags` doesn't exceed `gag_limit`
        if self._count_all_gags() > gag_limit:
            self.gags = DEFAULT_GAGS

        self.gag_levels = gag_levels
        self.gag_exps = gag_exps

    def _count_all_gags(self) -> int:
        """Return the Toon's total number of usable Gags

        Returns:
            int: Total number of Gags
        """
        count = count_all_gags(gags=self.gags)

        # TODO : Raise TooManyGagsError if Gag count exceeds `gag_limit`
        assert count <= self.gag_limit, (
            f"Gag quantity ({count}) exceeds Toon's ({self.name}) gag limit "
            f"({self.gag_limit})."
            )
        return count

    def _has_gag(self, gag_track: int, gag_level: int) -> bool:
        """True if Toon has the Gag, False if Toon doesn't have, or hasn't yet
            unlocked, the Gag.

        Args:
            gag_track (int): Index number of the Gag Track <0-6>
            gag_level (int): Level of the Gag <0-6>

        Returns:
            bool: True if Toon has the Gag
        """
        return self.count_gag(gag_track, gag_level) != 0

    def choose_gag(self, gag_track: int, gag_level: int) -> Gag:
        """Return Gag object containing Gag's vital info, iff Toon has the Gag

        Args:
            gag_track (int): Index number of the Gag Track <0-6>
            gag_level (int): Level of the Gag <0-6>

        Returns:
            Gag: Vital information about the Toon's Gag
        """
        gag_exp = self.get_gag_exp(gag_track=gag_track)
        gag = Gag(track=gag_track, exp=gag_exp, level=gag_level)
        if self._has_gag(gag_track=gag_track, gag_level=gag_level):
            return gag

        # TODO : Raise NotEnoughGagsError
        assert self._has_gag(gag_track=gag.track, gag_level=gag.level), (
            f"Toon \"{self.name}\" does not have any lvl {gag.level} "
            f"{gag.track_name} gags \"{gag.name}\"."
            )

    def count_gag(self, gag_track: int, gag_level: int) -> int:
        """Return Toon's current quantity of a Gag(gag_track, gag_level)

        Args:
            gag_track (int): Index number of the Gag Track <0-6>
            gag_level (int): Level of the Gag <0-6>

        Returns:
            int: Current quantity of a Gag
        """
        # TODO : Raise LockedGagTrackError if self.gags[gag_track] == [-1]*7
        # TODO : Raise LockedGagError if self.gags[gag_track][gag_level] == -1
        return self.gags[gag_track][gag_level]

    def do_attack(self, target: Cog, gag_track: int, gag_level: int) -> int:
        """Perform an attack on a Cog, given gag_track# and gag_level#

        Args:
            target (Cog): Cog object that is going to be attacked
            gag_track (int): Index number of the Gag Track <0-6>
            gag_level (int): Level of the Gag <0-6>

        Returns:
            int: 0 if the attack misses, 1 if it hits
        """
        # TODO: Raise InvalidToonAttackTarget
        assert type(target) == Cog, (
            f"Toon \"{self.name}\" tried to attack a non-Cog object:"
            f"{type(target)}"
        )

        gag = self.choose_gag(gag_track=gag_track, gag_level=gag_level)
        # TODO: Pass in attack_accuracy
        attack_hit = super().do_attack(target=target, amount=gag.damage)
        if attack_hit:
            # ! Maybe return tuple containing all attack info when creating
            # ! the Observer: gag track, level, exp, damage, reward, target,
            # ! target_hp, current_hp
            self.gag_exps[gag_track] += gag_level

        # TODO Create function to add EXP so we can track rewards for model
        self.gags[gag_track][gag_level] -= 1
        return attack_hit

    def get_attack_accuracy(self, gag: Gag, target: Cog, bonus: int=0) -> int:
        """Calculate Gag Attack accuracy, given a gag and Cog target

        attack_accuracy = gag_accuracy + gag_exp + target_defense + bonus
            Source: https://toontownrewritten.fandom.com/wiki/Accuracy#propAcc

        Args:
            gag (Gag): Gag object obtained from `self.choose_gag()`
            target (Cog): Cog object that is going to be attacked
            bonus (int, optional): Bonus added when near a prop bonus during
                                   Battle. Defaults to 0.

        Returns:
            int: Attack accuracy value in range <0-95>
        """
        # ! When Trap gag is used, atkAcc is set to 100, and atkHit is set to 1
        if gag.track == LURE_TRACK:
            return 100
        # ! For all other gags, if atkAcc exceeds 95, it will be reduced to 95
        gag_acc = get_gag_accuracy(gag.track, gag.level)
        gag_exp = self.get_gag_exp(gag.track)
        target_def = target.defense

        # ? Won't this always be 95 bc track_exp is easily > 95
        atk_acc = gag_acc + gag_exp + target_def + bonus
        return min(atk_acc, 95)

    def get_gag_exp(self, gag_track: int) -> int:
        """Get EXP for a Toon's Gag Track, given gag_track# and list of gag_exps

        Args:
            gag_track (int): Index number of the Gag Track <0-6>

            Example of valid input ::
                0     # HEAL_TRACK
                1     # TRAP_TRACK
                2     # LURE_TRACK
                3     # SOUND_TRACK
                4     # THROW_TRACK
                5     # SQUIRT_TRACK
                6     # DROP_TRACK

        Returns:
            int: Toon's current Gag Track EXP
        """
        # return self.gag_exps[gag_track]
        return get_gag_exp(gag_track=gag_track,
                           current_exps=self.gag_exps)

    def get_gag_exp_needed(self, gag_track: int) -> int:
        """Return the Gag Track EXP required to advance to next Gag Track level

        Args:
            gag_track (int): Index number of the Gag Track <0-6>

            Example of valid input ::
                0     # HEAL_TRACK
                1     # TRAP_TRACK
                2     # LURE_TRACK
                3     # SOUND_TRACK
                4     # THROW_TRACK
                5     # SQUIRT_TRACK
                6     # DROP_TRACK

        Returns:
            int: EXP required to level up the Toon's Gag Track
        """
        return get_gag_exp_needed(gag_track=gag_track,
                                  current_exps=self.gag_exps)

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

    def has_gags(self) -> bool:
        """True if Toon has any available Gags, checks quantity of all Gags

        Returns:
            bool: True if Toon has any available Gags
        """
        # [[0]*7]*7 == 2-D list, 7x7, initialized with 0's
        # Return True if the 2-D list is NOT empty, aka Toon has Gags
        # return self.gags != [[0]*7]*7
        return self._count_all_gags() != 0
