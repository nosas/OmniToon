# %% Import functions and classes
from .Cog import Cog
from .Entity import Entity
from .Exceptions import (GagCountError, InvalidToonAttackTarget,
                         LockedGagError, LockedGagTrackError,
                         NotEnoughGagsError, TooManyGagsError)
from .Gag import Gag
from .GagGlobals import (LEVELS, LURE_TRACK, count_all_gags, get_gag_accuracy,
                         get_gag_exp, get_gag_exp_needed)

DEFAULT_HP = 15
# -1 means the gag_track is locked,0 means lvl 1 Gag is unlocked
DEFAULT_LEVELS = [-1, -1, -1, -1, 0, 0, -1]
# DEFAULT_EXPS = [0, 0, 0, 0, 10, 10, 0]
# Populate DEFAULT_EXP from Gag track levels in DEFAULT_LEVELS
DEFAULT_EXPS = [LEVELS[idx][level] for idx, level in enumerate(DEFAULT_LEVELS)]
DEFAULT_GAGS = [[-1, -1, -1, -1, -1, -1, -1],  # Toon-Up
                [-1, -1, -1, -1, -1, -1, -1],  # Trap
                [-1, -1, -1, -1, -1, -1, -1],  # Lure
                [-1, -1, -1, -1, -1, -1, -1],  # Sound
                [0,  -1, -1, -1, -1, -1, -1],  # Throw
                [0,  -1, -1, -1, -1, -1, -1],  # Squirt
                [-1, -1, -1, -1, -1, -1, -1]]  # Drop
DEFAULT_GAG_LIMIT = 20


# ? AssertionErrors when? During initialization of attributes or separate func?
# ? Should I use @property decorators again?
class Toon(Entity):
    def __init__(self, name, hp=DEFAULT_HP, gags=DEFAULT_GAGS,
                 gag_exps=DEFAULT_EXPS, gag_levels=DEFAULT_LEVELS,
                 gag_limit=DEFAULT_GAG_LIMIT):
        """Toon object class

        Args:
            name (str): Name of the Toon
            hp (int, optional): Laff-o-Meter (health points) of a Toon
            # ? Gags = 2-D list : [type?][type?].. 2D array of type Gag or int?
            # ! Create Gags object, remove 2-D list and replace with Gags obj
            # ! Toon.gags = Gags(toons_gags=2-D list)
            # ! Toon.gags.get_gag(gtype="throw", level=<1-7|0-6>)
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
        super().__init__(name=name, hp=hp)
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

        if count > self.gag_limit:
            raise TooManyGagsError(count, self.gag_limit)

        return count

    def _count_gag(self, gag_track: int, gag_level: int) -> int:
        """Return Toon's current quantity of a Gag(gag_track, gag_level)

        Args:
            gag_track (int): Index number of the Gag Track <0-6>
            gag_level (int): Level of the Gag <0-6>

        Returns:
            int: Current quantity of a Gag
        """
        assert gag_track in range(7)
        assert gag_level in range(7)

        gag_count = self.gags[gag_track][gag_level]

        return gag_count

    def _has_gag(self, gag_track: int, gag_level: int) -> bool:
        """True if Toon has the Gag, False if Toon doesn't have, or hasn't yet
            unlocked, the Gag.

        Args:
            gag_track (int): Index number of the Gag Track <0-6>
            gag_level (int): Level of the Gag <0-6>

        Returns:
            bool: True if Toon has the Gag
        """
        # Not in [0, -1]
        return self._count_gag(gag_track, gag_level) > 0

    def choose_gag(self, gag_track: int, gag_level: int) -> Gag:
        """Return Gag object containing Gag's vital info, iff Toon has the Gag

        Args:
            gag_track (int): Index number of the Gag Track <0-6>
            gag_level (int): Level of the Gag <0-6>

        Returns:
            Gag: Vital information about the Toon's Gag
        """
        gag_count = self._count_gag(gag_track, gag_level)

        if gag_count == 0:
            raise NotEnoughGagsError
        if self.gags[gag_track] == [-1]*7:
            raise LockedGagTrackError(gag_track)
        if gag_count == -1:
            raise LockedGagError(gag_level)

        gag_exp = self.get_gag_exp(gag_track=gag_track)
        return Gag(track=gag_track, exp=gag_exp, level=gag_level)

    # TODO Replace all gag_track,gag_level args to Gag objects
    def do_attack(self, target: Cog, gag_track: int, gag_level: int) -> int:
        """Perform an attack on a Cog, given gag_track# and gag_level#

        Args:
            target (Cog): Cog object that is going to be attacked
            gag_track (int): Index number of the Gag Track <0-6>
            gag_level (int): Level of the Gag <0-6>

        Returns:
            int: 0 if the attack misses, 1 if it hits
        """
        if type(target) != Cog:
            raise InvalidToonAttackTarget

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
        # ! Nope! We're calculating accuracy wrong. It shouldn't be track EXP
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
        return get_gag_exp(gag_track=gag_track, current_exps=self.gag_exps)

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

    # TODO : We should probably move this to Strategy, when we make Strategies.
    # TODO : Make sure to check against the highest level Cog in the battle
    # However, if the Cog being attacked is at a lower level than the gag,
    # then the toon will receive no skill points.
    # https://toontown.fandom.com/wiki/Skill_points#Earning_skill_points
    def get_viable_attacks(self, target: Cog) -> list:
        """Return 2-D list of Gags that can be used and gain Gag
            A Gag is viable if its level is at or below the Cog's level.

        Args:
            target (Cog): Cog object that is going to be attacked

        Returns:
            list: 2-D list of Gags. 0 means the Gag is not available or
                  does not gain Gag EXP when used. If all Gags are unviable,
                  it will return the a list of the Toon's Gags.

        Example of Toon Astro's vibale Gags against level 4 Cog ::
            toon_astro.gags = [
                [0,   0,  0,  5,  5,  3, -1],
                [-1, -1, -1, -1, -1, -1, -1],
                [0,   0,  0,  0,  5,  3,  1],
                [0,   0,  0,  0,  5,  3, -1],
                [0,   2,  1,  4,  4,  2, -1],
                [0,   0,  0,  5,  5,  3, -1],
                [0,   9,  5, -1, -1, -1, -1]
            ]

            all_viable_gags = [
                [-1, -1, -1,  5, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1],
                [-1,  2,  1,  4, -1, -1, -1],
                [-1, -1, -1,  5, -1, -1, -1],
                [-1,  9,  5, -1, -1, -1, -1]
            ]
        """
        # TODO : Add attributes to Gags to determine if valid/invalid/locked
        # All Gags are viable against lvl 7+ Cogs
        if target.level >= 7:
            return self.gags

        # Return Gags with index ranging from (0, target.level) aka (0,6)
        assert 7 > target.level >= 0, (
            f"[!] What the heck is the Cog's level? level={target.level}")

        all_viable_gags = []
        num_invalid_gags = 7 - target.level

        for gag_track in self.gags:
            viable_gags = gag_track.copy()
            track_index = self.gags.index(gag_track)

            # Can't use Lure against a lured Cog
            if target.is_lured and track_index == LURE_TRACK:
                all_viable_gags.append([-1]*7)
                continue

            # Pad the viable_gags list with -1s to make len(viable_gags) == 7
            # viable_gags = gag_track[:target.level] + [-1]*num_invalid_gags
            viable_gags[target.level:] = [-1]*num_invalid_gags
            for idx, gag in enumerate(viable_gags[:target.level]):
                # Can't use Gag if locked or quantity is 0
                viable_gags[idx] = -1 if gag in [0, -1] else gag

            all_viable_gags.append(viable_gags)

        return all_viable_gags

    def has_gags(self) -> bool:
        """True if Toon has any available Gags, checks quantity of all Gags

        Returns:
            bool: True if Toon has any available Gags
        """
        # [[0]*7]*7 == 2-D list, 7x7, initialized with 0's
        # Return True if the 2-D list is NOT empty, aka Toon has Gags
        # return self.gags != [[0]*7]*7
        return self._count_all_gags() != 0
