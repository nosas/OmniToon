# %% Import functions and classes
from random import choice as rand_choice
from random import randrange

from .Cog import Cog
from .Entity import Entity
from .Exceptions import (GagCountError, InvalidToonAttackTarget,
                         LockedGagError, LockedGagTrackError,
                         NotEnoughGagsError, TooManyGagsError)
from .Gag import Gag
from .GagGlobals import (HEAL_TRACK, LEVELS, LURE_TRACK, count_all_gags,
                         get_gag_accuracy, get_gag_exp, get_gag_exp_needed)

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
        if count < 0:
            raise GagCountError

        return count

    def _count_gag(self, track: int, level: int) -> int:
        """Return Toon's current quantity of a Gag(gag_track, gag_level)

        Args:
            gag_track (int): Index number of the Gag Track <0-6>
            gag_level (int): Level of the Gag <0-6>

        Returns:
            int: Current quantity of a Gag
        """
        assert track in range(7)
        assert level in range(7)

        count = self.gags[track][level]

        return count

    def _count_gag_track(self, track: int) -> int:
        """Return Toon's current number of Gags in a Gag track

        Args:
            gag_track (int): Index number of the Gag Track <0-6>

        Returns:
            int: Current quantity of a Gag track
        """
        count = sum(self.gags[track], start=self.gags[track].count(-1))
        return count

    def _get_gag(self, track: int, level: int) -> Gag:
        count = self._count_gag(track=track, level=level)
        exp = self.get_gag_exp(track=track)
        return Gag(track=track, exp=exp, level=level)

    def _has_gag(self, track: int, level: int) -> bool:
        """True if Toon has the Gag, False if Toon doesn't have, or hasn't yet
            unlocked, the Gag.

        Args:
            track (int): Index number of the Gag Track <0-6>
            level (int): Level of the Gag <0-6>

        Returns:
            bool: True if Toon has the Gag
        """
        # Not in [0, -1]
        return self._count_gag(track=track, level=level) > 0

    # ! This should, and all attack-related stuff, should go into Strategy
    def _pick_random_gag(self, target=None, attack=False) -> Gag:
        if self._count_all_gags() == 0:
            # TODO Need another error, this one is for individual Gags
            raise NotEnoughGagsError

        gags = self.gags if target is None else self.get_viable_attacks(target)

        if target:
            # If no Gags are viable (e.g. gag.unlocked & gag.count>0), expand
            # the random Gag selection to all of the Toon's Gags
            if count_all_gags(gags=gags) == 0:
                print(f"Toon \"{self.name}\" does not have any viable attacks "
                      f"against lvl {target.level} {target.name}.")
                print("    [!] Expanding random Gag selection to all Gags")
                gags = self.gags
            else:
                raise GagCountError

        # Example `viable_gags` = [(track, level), (track, level), ... ]
        viable_gags = []
        for track_index, gag_track in enumerate(gags):
            for gag_level, gag_count in enumerate(gag_track):
                # TODO Add rules to debug output
                rules = [gag_count not in [0, -1],
                         # Toons cannot use Heal as an attack
                         track_index != HEAL_TRACK if attack is True else 1
                         ]

                # If all rules pass (== True), this Gag is viable
                if all(rules):
                    viable_gags.append((track_index, gag_level))

        if viable_gags == []:
            raise NotEnoughGagsError

        gag_track, gag_level = rand_choice(viable_gags)
        random_gag = self.choose_gag(track=gag_track, level=gag_level)
        return random_gag

    def _pick_random_attack(self, target=None) -> Gag:
        return self._pick_random_gag(target=target, attack=True)

    def choose_gag(self, track: int, level: int) -> Gag:
        """Return Gag object containing Gag's vital info, iff Toon has the Gag

        Args:
            track (int): Index number of the Gag Track <0-6>
            level (int): Level of the Gag <0-6>

        Returns:
            Gag: Vital information about the Toon's Gag
        """

        count = self._count_gag(track, level)
        if count == 0:
            raise NotEnoughGagsError
        if self.gags[track] == [-1]*7:
            raise LockedGagTrackError(track=track)
        if count == -1:
            raise LockedGagError(level=level)

        return self._get_gag(track=track, level=level)

    def choose_attack(self, target: Cog, track: int, level: int) -> Gag:  # noqa
        # If no arguments were provided, pick a random attack
        # ! A random
        if track == -1 or level == -1:
            try:
                gag = self._pick_random_attack(target=target)
            except GagCountError:
                print(f"[!] WARNING : Unable to find viable attack, expanding "
                      "search to all Gags")
                gag = self._pick_random_attack(target=None)
            print(f"Random Gag == {gag.track}, {gag.level}, {gag.name}")
        else:
            gag = self.choose_gag(track=track, level=level)
        return gag

    # TODO Replace all gag_track,gag_level args to Gag objects
    def do_attack(self, target: Cog, track: int=-1, level: int=-1) -> int:  # noqa
        """Perform an attack on a Cog, given track# and level#

        Args:
            target (Cog): Cog object that is going to be attacked
            track (int, optional): Index number of the Gag Track <0-6>.
                Defaults to -1.
            level (int, optional): Level of the Gag <0-6>.
                Defaults to -1.

        Returns:
            int: 0 if the attack misses, 1 if it hits
        """
        if type(target) != Cog:
            raise InvalidToonAttackTarget

        gag = self.choose_attack(target=target, track=track, level=level)

        # TODO: Pass in attack_accuracy
        attack_hit = super().do_attack(target=target, amount=gag.damage)
        if attack_hit:
            # ! Maybe return tuple containing all attack info when creating
            # ! the Observer: gag track, level, exp, damage, reward, target,
            # ! target_hp, current_hp
            self.gag_exps[gag.track] += gag.level

        # TODO Create func: Add Gag EXP (reward), so we can track model rewards
        self.gags[gag.track][gag.level] -= 1
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
        gag_acc = get_gag_accuracy(track=gag.track, level=gag.level)
        gag_exp = self.get_gag_exp(track=gag.track)
        target_def = target.defense

        # ? Won't this always be 95 bc track_exp is easily > 95
        # ! Nope! We're calculating accuracy wrong. It shouldn't be track EXP
        atk_acc = gag_acc + gag_exp + target_def + bonus
        return min(atk_acc, 95)

    def get_gag_exp(self, track: int) -> int:
        """Get EXP for a Toon's Gag Track, given track# and list of exps

        Args:
            track (int): Index number of the Gag Track <0-6>

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
        # return self.gag_exps[track]
        return get_gag_exp(track=track, current_exps=self.gag_exps)

    def get_gag_exp_needed(self, track: int) -> int:
        """Return the Gag Track EXP required to advance to next Gag Track level

        Args:
            track (int): Index number of the Gag Track <0-6>

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
        return get_gag_exp_needed(track=track,
                                  current_exps=self.get_gag_exp(track)
                                  )

    # TODO : We should probably move this to Strategy, when we make Strategies.
    # TODO : Make sure to check against the highest level Cog in the battle
    # However, if the Cog being attacked is at a lower level than the gag,
    # then the toon will receive no skill points.
    # https://toontown.fandom.com/wiki/Skill_points#Earning_skill_points
    def get_viable_attacks(self, target: Cog) -> list:
        """Return 2-D list of Gags that can be used and gain Gag EXP (reward)
            A Gag is viable if its level below the Cog's level.

        Args:
            target (Cog): Cog object that is going to be attacked

        Returns:
            list: 2-D list of Gags. 0 means the Gag is not available or
                  does not gain Gag EXP when used. If all Gags are unviable,
                  it will return the a list of the Toon's Gags.

        Example of Toon Astro's viable Gags against level 4 Cog ::
            input = toon_astro.gags = [
                [0,   0,  0,  5,  5,  3, -1],
                [-1, -1, -1, -1, -1, -1, -1],
                [0,   0,  0,  0,  5,  3,  1],
                [0,   0,  0,  0,  5,  3, -1],
                [0,   2,  1,  4,  4,  2, -1],
                [0,   0,  0,  5,  5,  3, -1],
                [0,   9,  5, -1, -1, -1, -1]
            ]

            output = all_viable_gags = [
                [-1, -1, -1,  5, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1],
                [-1,  2,  1,  4, -1, -1, -1],
                [-1, -1, -1,  5, -1, -1, -1],
                [-1,  9,  5, -1, -1, -1, -1]
            ]
        """
        all_viable_gags = self.get_viable_gags(target=target)
        all_viable_gags[HEAL_TRACK] = [-1]*7
        return all_viable_gags

    def get_viable_gags(self, target: Cog) -> list:
        """Return 2-D list of Gags that can be used and gain Gag EXP (reward)
            A Gag is viable if its level below the Cog's level.

        Args:
            target (Cog): Cog object that is going to be attacked

        Returns:
            list: 2-D list of Gags. 0 means the Gag is not available or
                  does not gain Gag EXP when used. If all Gags are unviable,
                  it will return the a list of the Toon's Gags.

        Example of Toon Astro's viable Gags against level 4 Cog ::
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

        # Return Gags with index ranging from (0, target.level) aka (0,6)
        assert 7 > target.level >= 0, (
            f"[!] What the heck is the Cog's level? level={target.level}")

        all_viable_gags = []

        for track_index, gag_track in enumerate(self.gags):
            viable_gags = gag_track.copy()

            # Can't use Lure against a lured Cog
            if target.is_lured and track_index == LURE_TRACK:
                all_viable_gags.append([-1]*7)
                continue

            # Compare each Gag. Unviable if count == 0 or Cog.level < gag.level
            for gag_level, gag_count in enumerate(viable_gags):
                # No reward if Gag lvl is greater than, or equal to, Cog lvl
                if gag_level >= target.level:
                    viable_gags[gag_level] = -1
                    continue
                # Can't use Gag if locked or quantity is 0
                if gag_count in [0, -1]:
                    viable_gags[gag_level] = -1

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
