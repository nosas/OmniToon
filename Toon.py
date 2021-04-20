# %% Import functions and classes
from random import choice as rand_choice

from .Cog import Cog
from .Entity import Entity
from .Exceptions import (CogLuredError, GagCountError, InvalidToonAttackTarget,
                         LockedGagError, LockedGagTrackError,
                         NotEnoughGagsError, TargetDefeatedError,
                         TooManyGagsError)
from .Gag import Gag
from .GagGlobals import (DROP_TRACK, HEAL_TRACK, LEVELS, LURE_TRACK,
                         TRAP_TRACK, count_all_gags, get_gag_accuracy,
                         get_gag_exp, get_gag_exp_needed)

DEFAULT_HP = 15
# -1 means the gag_track is locked,0 means lvl 1 Gag is unlocked
DEFAULT_LEVELS = [-1, -1, -1, -1, 0, 0, -1]
# Populate DEFAULT_EXP from Gag track levels in DEFAULT_LEVELS
DEFAULT_EXPS = [LEVELS[idx][level] for idx, level in enumerate(DEFAULT_LEVELS)]
# DEFAULT_EXPS = [0, 0, 0, 0, 10, 10, 0]
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
        self.hp_max = hp
        self.gag_limit = gag_limit
        self.gags = gags
        # Verify total Gag count in `gags` doesn't exceed `gag_limit`
        if self._count_all_gags() > gag_limit:
            self.gags = DEFAULT_GAGS

        self.gag_levels = gag_levels
        self.gag_exps = gag_exps

    def __str__(self):
        return f'"{self.name}" ({self.hp}/{self.hp_max}hp)'

    def __repr__(self):
        return self.__str__()

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
        # count_max =  # ! TODO #42
        exp = self.get_gag_exp(track=track)
        return Gag(track=track, exp=exp, level=level, count=count)

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

    # ! TODO #38, this & all attack-related stuff should go into Strategy
    def _pick_random_gag(self, target=None, attack=False) -> Gag:
        if self._count_all_gags() == 0:
            # TODO Need another error, this one is for individual Gags
            raise NotEnoughGagsError

        gags = self.gags if target is None else self.get_viable_attacks(target)

        # Verify there's at least 1 viable Gag, given the Cog's level
        if target:
            # If no Gags are viable (e.g. gag.unlocked & gag.count>0), expand
            # the random Gag selection to all of the Toon's Gags
            if count_all_gags(gags=gags) == 0:
                print(f"        [!] WARNING `_pick_random_gag` : Toon {self} "
                      f"does not have any viable attacks against Cog {target}")
                print("            [-] Expanding random Gag selection to all "
                      "Gags")
                gags = self.gags

        # If there are no viable Gags at all, raise GagCountError and restock
        if count_all_gags(gags=gags) == 0:
            raise GagCountError

        # Example `viable_gags` = [(track, level), (track, level), ... ]
        viable_gags = []
        for track_index, gag_track in enumerate(gags):
            for gag_level, gag_count in enumerate(gag_track):
                # TODO #38, add different rules for different Strategies
                # TODO #38, Create Rules for valid Gags using numpy masks,
                # validate against those Rules. We can make more custom
                # exceptions for this when we make strategies.

                rules = [gag_count not in [0, -1],
                         # Toons cannot use Heal as an attack
                         track_index != HEAL_TRACK if attack is True else 1
                         ]
                if target:
                    rules.append(
                        track_index != LURE_TRACK if target.is_lured else 1)

                # If all rules pass, this Gag is viable
                if all(rules):
                    viable_gags.append((track_index, gag_level))

        if viable_gags == []:
            raise NotEnoughGagsError

        gag_track, gag_level = rand_choice(viable_gags)
        random_gag = self.choose_gag(track=gag_track, level=gag_level,
                                     attack=attack)
        return random_gag

    def _pick_random_attack(self, target) -> Gag:
        return self._pick_random_gag(target=target, attack=True)

    def choose_gag(self, track: int, level: int, attack=False) -> Gag:
        """Return Gag object containing Gag's vital info, iff Toon has the Gag

        Args:
            track (int): Index number of the Gag Track <0-6>
            level (int): Level of the Gag <0-6>
            attack (bool, optional) : True if

        Returns:
            Gag: Vital information about the Toon's Gag
        """

        gag = self._get_gag(track=track, level=level)
        if gag.count == 0:
            raise NotEnoughGagsError(gag)
        if self.gags[track] == [-1]*7:
            raise LockedGagTrackError(track=track)
        if gag.count == -1:
            raise LockedGagError(level=level)

        gag_or_atk = 'gag' if not attack else 'attack'
        print(f"            [-] `choose_{gag_or_atk}()` : {gag}")
        return gag

    def choose_attack(self, target: Cog = None, track: int = -1, level: int = -1) -> Gag:  # noqa
        # If no arguments were provided, pick a random attack
        if track == -1 or level == -1:
            gag = self._pick_random_attack(target=target)
            # print(f"            [>] Toon `choose_attack` random Gag : {gag}")
        else:
            gag = self.choose_gag(track=track, level=level, attack=True)
        return gag

    # TODO #11, Replace all gag_track,gag_level args to Gag objects
    def do_attack(self, target: Cog, gag_atk: Gag, overdefeat=False) -> int:
        """Perform an attack on a Cog, given track# and level#

        Args:
            target (Cog): Cog object that is going to be attacked
            # ! TODO : Update docstrings

        Returns:
            int: 0 if the attack misses, 1 if it hits
        """
        if type(target) != Cog:
            raise InvalidToonAttackTarget

        gag_atk = self._get_gag(track=gag_atk.track, level=gag_atk.level)
        if gag_atk.track == TRAP_TRACK:
            if target.is_lured:
                raise CogLuredError("Can't use Trap on a lured Cog")
            if target.is_trapped:
                target.is_trapped = False
                target.clear_trap()

        try:
            # TODO #10, Pass in attack_accuracy
            attack_hit = Entity.do_attack(self, target=target,
                                          amount=gag_atk.damage)
            if attack_hit and gag_atk.track == LURE_TRACK:
                target.is_lured = True
            elif attack_hit and target.is_lured:
                # TODO #20, add bonus damage for attacking lured Cog
                target.is_lured = False

        except TargetDefeatedError:
            # Multiple Toons attack the same Cog with the same Gag track
            if overdefeat is True:
                pass
            # Target is already defeated. Return 0, do not decrease Gag count
            print(f"    [!] WARNING `do_attack` : {self} tried to attack a "
                  f"defeated Cog {target}")
            print(f"        [-] Skipping {gag_atk} attack, Cog {target} is "
                  "already defeated")
            return 0

        # TODO #37, Add Gag EXP (reward), so we can track rewards
        self.gags[gag_atk.track][gag_atk.level] -= 1
        return attack_hit

    def get_attack_accuracy(self, gag: Gag, target: Cog, bonus: int = 0) -> int:  # noqa
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

    # TODO #38, We should move this to Strategy, when we make Strategies.
    # TODO #38, Make sure to check against the highest level Cog in the battle
    # However, if the Cog being attacked is at a lower level than the gag,
    # then the toon will receive no skill points.
    # https://toontown.fandom.com/wiki/Skill_points#Earning_skill_points
    def get_viable_attacks(self, target: Cog) -> list:
        """Return 2-D list of Gags that can be used and gain Gag EXP (reward)
            A Gag is viable if its level is below the Cog's level.

            NOTE: We're using 0-indexing for Gag levels, but 1-indexing for Cog

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
        # TODO  #11, Add Gag attributes to determine if valid/invalid/locked
        all_viable_gags = []

        for track_index, gag_track in enumerate(self.gags):
            viable_gags = gag_track.copy()

            # Can't use Lure against a lured Cog
            # Drop could be viable if a Cog is lured, because another Toon can
            # attack the Cog when it's lured, and then we use Drop. But we'll
            # assume it's unviable until we develop Strategies
            # TODO #38
            if target.is_lured and track_index in [LURE_TRACK, DROP_TRACK]:
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
