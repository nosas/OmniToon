"""
    BattleGlobalTracks = ['toon-up', 'trap', 'lure', 'sound', 'throw', 'squirt', 'drop']
    BattleGlobalNPCTracks = ['restock', 'toons hit', 'cogs miss']
    BattleGlobalAvPropStrings = (
    ('Feather', 'Megaphone', 'Lipstick', 'Bamboo Cane', 'Pixie Dust', 'Juggling Balls', 'High Dive'),
    ('Banana Peel', 'Rake', 'Marbles', 'Quicksand', 'Trapdoor', 'TNT', 'Railroad'),
    ('$1 bill', 'Small Magnet', '$5 bill', 'Big Magnet', '$10 bill', 'Hypno-goggles', 'Presentation'),
    ('Bike Horn', 'Whistle', 'Bugle', 'Aoogah', 'Elephant Trunk', 'Foghorn', 'Opera Singer'),
    ('Cupcake', 'Fruit Pie Slice', 'Cream Pie Slice', 'Whole Fruit Pie', 'Whole Cream Pie', 'Birthday Cake', 'Wedding Cake'),
    ('Squirting Flower', 'Glass of Water', 'Squirt Gun', 'Seltzer Bottle', 'Fire Hose', 'Storm Cloud', 'Geyser'),
    ('Flower Pot', 'Sandbag', 'Anvil', 'Big Weight', 'Safe', 'Grand Piano', 'Toontanic')
    )
"""  # noqa
from __future__ import annotations

from dataclasses import dataclass, field
from math import floor as math_floor
from random import choice as rand_choice
from typing import List, Optional

from .AttackGlobals import GROUP
from .Exceptions import (GagCountError, LockedGagError, LockedGagTrackError,
                         NotEnoughGagsError, TooManyGagsError)
from .GagGlobals import (DEFAULT_GAG_COUNT, DEFAULT_TRACK_EXPS_CURRENT,
                         DEFAULT_TRACK_EXPS_NEXT, GAG, GAG_CARRY_LIMITS,
                         GAG_DAMAGE, GAG_LABELS, GAG_TRACK_LABELS, LEVELS,
                         MULTI_TARGET_GAGS, TRACK)


def get_default_gag_counts():
    return DEFAULT_GAG_COUNT.copy()


def get_default_exps_current():
    return DEFAULT_TRACK_EXPS_CURRENT.copy()


def get_default_exps_next():
    return DEFAULT_TRACK_EXPS_NEXT.copy()


def get_default_gags():
    """Create a 2D list of Gag objects with default Gag values"""
    default_gags = []

    gag_track_list = []
    for gag_enum in GAG:
        gag_track_list.append(
            Gag(exp=DEFAULT_TRACK_EXPS_CURRENT[gag_enum.track],
                level=gag_enum.level,
                track=gag_enum.track,
                count=DEFAULT_GAG_COUNT[gag_enum.track][gag_enum.level])
        )

        if gag_enum.level == 6:  # or gag_enum.index
            default_gags.append(gag_track_list)
            gag_track_list = []

    return default_gags


@dataclass
class Gag:

    """Attack/Heal used by a Toon during Battle

    Args:
        track (int): Index of the Gag Track <0-6>
        exp (int): EXP of the Gag Track
        level (int): Level of the Gag <0-6>
        count (int, optional): Current quantity of the Gag. Defaults to 0.
    """
    exp: int
    level: int
    track: int
    _track: int = field(init=False, repr=False)
    count: Optional[int] = field(default=0)

    # Initialize with default values so they're included in __repr__
    # Is there a better way to include them in repr without initializing with default values?
    accuracy: int = field(init=False, default=-1)
    name: str = field(init=False, default='')
    target: int = field(init=False, default=-1)

    def __post_init__(self):
        # TODO Create function to get max count
        # Maximum number of carryable gags of this level
        # self.capacity_maximum = 5 + (5*(highest_level-level))
        self.accuracy = get_gag_accuracy(track=self.track, level=self.level)
        self.name = get_gag_name(track=self.track, level=self.level)
        self.target = get_gag_target(name=self.name)

    def __str__(self):
        # print(gag_throw) == 'Lvl 3 Throw, "Whole Fruit Pie" (2million dmg)'
        return f'lvl {self.level} {self.track.name} '\
               f'"{self.name}" ({self.track, self.level}, {self.damage}dmg)'

    @property
    def damage(self) -> int:
        return get_gag_damage(track=self.track, level=self.level, exp=self.exp)

    @property
    def track(self) -> TRACK:
        return self._track

    @track.setter
    def track(self, new_track: int) -> None:
        """Ensure the integer being passed in is converted to a TRACK enum

        This will allow us to easily access the Gag Track's name and value

        Args:
            new_track (int): Integer in range <0-6>, corresponding to TRACK enum class
        """
        assert new_track in range(7)
        self._track = TRACK(new_track)


@dataclass
class Gags:
    """Collection of Gags and Gag-related functions"""

    gag_count: List[List[int]] = field(default_factory=get_default_gag_counts)
    track_exps: Optional[List[int]] = field(default_factory=get_default_exps_current)
    # TODO Turn this into a property
    # track_exps_next: Optional[List[int]] = field(init=False,
    #                                              default_factory=get_default_exps_next)

    @property
    def track_levels(self):
        return self._calculate_gag_levels_from_gag_count(self.gag_count)

    @property
    def gags(self):
        """Create a 2D list of Gag objects"""
        all_gags = []

        gag_track_list = []
        for gag_enum in GAG:
            gag_track_list.append(
                Gag(exp=self.track_exps[gag_enum.track],
                    level=gag_enum.level,
                    track=gag_enum.track,
                    count=self.gag_count[gag_enum.track][gag_enum.level])
            )

            if gag_enum.level == 6:  # or gag_enum.index
                all_gags.append(gag_track_list)
                gag_track_list = []

        return all_gags

    @property
    def unlocked_gags(self):
        """Return a flattened list unlocked of Gags"""

        return [gag for gag in self._flatten_gags() if gag.count != -1]

    @property
    def available_gags(self):
        """Return a flattened list available (unlocked, count > 0) of Gags"""

        return [gag for gag in self.unlocked_gags if gag.count > 0]

    def __iter__(self):
        return iter(self._flatten_gags())

    def _flatten_gags(self) -> list:
        """Return a flattened list of Gags"""
        return [gag for gag_list in self.gags for gag in gag_list]

    def _calculate_gag_levels_from_gag_count(self) -> List[int]:
        """Determine the Gag Level of each Gag Track, given a list of all Gags

        Returns:
            List[int]: Level of each Gag track, -1 == locked, 0 == lvl 1 Gag is unlocked

        Example Input:
                DEFAULT_GAGS = [
                    [-1, -1, -1, -1, -1, -1, -1],   # Toon-Up
                    [-1, -1, -1, -1, -1, -1, -1],   # Trap
                    [-1, -1, -1, -1, -1, -1, -1],   # Lure
                    [-1, -1, -1, -1, -1, -1, -1],   # Sound
                    [0,  -1, -1, -1, -1, -1, -1],   # Throw
                    [0,  -1, -1, -1, -1, -1, -1],   # Squirt
                    [-1, -1, -1, -1, -1, -1, -1]    # Drop
                ]

            Output: [-1, -1, -1, -1, 0, 0, -1, -1]
        """
        return [(6 - track.count(-1)) for track in self.gags]

    def _calculate_gag_levels_from_track_exps(self) -> List[int]:
        """Determine the Gag Level of each Gag Track, given a list of Track EXPs

        Returns:
            List[int]: Level of each Gag track, -1 == locked, 0 == lvl 1 Gag is unlocked

        Example Input:
                DEFAULT_EXPS = [-1, -1, -1, -1, 0, 0, -1, -1]

            Output: [-1, -1, -1, -1, 0, 0, -1, -1]
        """
        gag_levels = [-1, -1, -1, -1, 0, 0, -1, -1]

        for track_idx, current_exp in enumerate(self.gags):
            if current_exp == -1:
                continue

            for level, exp in enumerate(LEVELS[track_idx]):
                if current_exp <= exp:
                    gag_levels[track_idx] = level
                    continue

        return gag_levels

    def _count_all_gags(self) -> int:
        """Return the Toon's total number of usable Gags

        Returns:
            int: Total number of Gags
        """
        count = count_all_gags(gags=self.gag_count)

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

        gags = self.gags if target is None else self.get_viable_attacks(target=target)

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
        # TODO : How can we utilize get_viable_gags here?
        # Can we just do [(track_index, gag_level) for track, level in gags if gag_count > 0]
        viable_gags = []
        for track_index, gag_track in enumerate(gags):
            for gag_level, gag_count in enumerate(gag_track):
                # TODO #38, add different rules for different Strategies
                # TODO #38, Create Rules for valid Gags using numpy masks,
                # validate against those Rules. We can make more custom
                # exceptions for this when we make strategies.

                rules = [gag_count not in [0, -1],
                         # Toons cannot use Heal as an attack
                         track_index != TRACK.HEAL if attack is True else 1
                         ]
                if target:
                    # Can't lure a lured Cog
                    rules.append(
                        track_index != TRACK.LURE if target.is_lured else 1)
                    # Can't trap a trapped Cog
                    rules.append(
                        track_index != TRACK.TRAP if target.is_trapped else 1)

                # If all rules pass, this Gag is viable
                if all(rules):
                    viable_gags.append((track_index, gag_level))

        if viable_gags == []:
            raise NotEnoughGagsError

        gag_track, gag_level = rand_choice(viable_gags)
        random_gag = self.choose_gag(track=gag_track, level=gag_level,
                                     attack=attack)
        return random_gag

    def choose_gag(self, track: int, level: int, attack=False) -> Gag:
        """Return Gag object containing Gag's vital info, iff Toon has the Gag

        Args:
            track (int): Index number of the Gag Track <0-6>
            level (int): Level of the Gag <0-6>
            attack (bool, optional) : True if called by `choose_attack()`.
                                      Defaults to False

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
        print(f"        [+] Toon `choose_{gag_or_atk}()` {self} : {gag}")
        return gag

    def get_gag_exp(self, track: int) -> int:
        """Get EXP for a Toon's Gag Track, given track# and list of exps

        Args:
            track (int): Index number of the Gag Track <0-6>

            Example of valid input ::
                0     # TRACK.HEAL
                1     # TRACK.TRAP
                2     # TRACK.LURE
                3     # TRACK.SOUND
                4     # TRACK.THROW
                5     # TRACK.SQUIRT
                6     # TRACK.DROP

        Returns:
            int: Toon's current Gag Track EXP
        """
        # return self.track_exps[track]
        return get_gag_exp(track=track, current_exps=self.track_exps)

    def get_gag_exp_needed(self, track: int) -> int:
        """Return the Gag Track EXP required to advance to next Gag Track level

        Args:
            track (int): Index number of the Gag Track <0-6>

            Example of valid input ::
                0     # TRACK.HEAL
                1     # TRACK.TRAP
                2     # TRACK.LURE
                3     # TRACK.SOUND
                4     # TRACK.THROW
                5     # TRACK.SQUIRT
                6     # TRACK.DROP

        Returns:
            int: EXP required to level up the Toon's Gag Track
        """
        return get_gag_exp_needed(track=track,
                                  current_exps=self.get_gag_exp(track)
                                  )


def count_all_gags(gags: list) -> int:
    """Return the total number of Gags, given a 2-D list of Gags

    Args:
        gags (2-D list): List of Gags, can be obtained from Toon.gags
            `gags` structure ::
                DEFAULT_GAGS = [
                    [-1, -1, -1, -1, -1, -1, -1],  # Toon-Up
                    [-1, -1, -1, -1, -1, -1, -1],  # Trap
                    [-1, -1, -1, -1, -1, -1, -1],  # Lure
                    [-1, -1, -1, -1, -1, -1, -1],  # Sound
                    [0,  -1, -1, -1, -1, -1, -1],  # Throw
                    [0,  -1, -1, -1, -1, -1, -1],  # Squirt
                    [-1, -1, -1, -1, -1, -1, -1]   # Drop
                ]

    Returns:
        int: Total number of Gags
    """
    count = 0
    for gag_track in gags:
        # Summing the -1 values will result in a negative Gag count
        # We can negate summing of -1 values by adding the count of -1 in the
        # current Gag track list to the starting index of sum(gag_track)
        count += sum(gag_track, start=gag_track.count(-1))

    return count


def get_gag_accuracy(track: int, level: int) -> int:
    """atkAcc = propAcc + trackExp + tgtDef + bonus

    Args:
        track (int): Index number of the Gag Track <0-6>
        level (int): Level of the Gag <0-6>

    Returns:
        int: [description]
    """
    return -1  # ! TODO #10 <<<<<<<<<<<<<<<<<<<<<<<<<<<<


def get_gag_carry_limits(track: int, level: int) -> tuple:
    """Return list of Gag carry limits based on Gag level

    Args:
        track (int): Index number of the Gag Track <0-6>
        level (int): Level of the Gag <0-6>

    Returns:
        tuple: 7-member tuple of Gag carry limits

        Example output for level 2 Drop track carry limits (track=6, lvl=1) ::
            GAG_CARRY_LIMITS[6][1] = (10, 5, 0, 0, 0, 0, 0)
    """

    return GAG_CARRY_LIMITS[track][level]


def get_gag_damage(track: int, level: int, exp: int) -> int:
    """Calculate and return Gag damage, given track#, level# and exp

    Args:
        track (int): Index number of the Gag Track <0-6>
        level (int): Level of the Gag <0-6>
        exp (int): Current EXP of the Gag Track <0-10000?>

    Returns:
        int: Damage of Gag
    """
    # MIN_MAX_TUPLE = GAG_DAMAGE[GAG_TRACK_INDEX][GAG_INDEX] =>
    #                 ((min_dmg, max_dmg), (min_exp, max_exp))
    # MIN_DMG, MAX_DMG = MIN_MAX_TUPLE[0] = (min_dmg, max_dmg)
    # MIN_EXP, MAX_EXP = MIN_MAX_TUPLE[1] = (min_exp, max_exp)
    #    Example of Level 3 Throw min/max = GAG_DAMAGE[4][3]

    min_dmg, max_dmg = get_gag_min_max_damage(track=track, level=level)
    min_exp, max_exp = get_gag_min_max_exp(track=track, level=level)
    exp_val = min(exp, max_exp)
    exp_per_hp = float(max_exp - min_exp + 1) / float(max_dmg - min_dmg + 1)
    damage = math_floor((exp_val - min_exp) / exp_per_hp) + min_dmg
    if damage <= 0:
        damage = min_dmg
    # if propAndOrganicBonusStack:
    #     originalDamage = damage
    #     if organicBonus:
    #         damage += getDamageBonus(originalDamage)
    #     if propBonus:
    #         damage += getDamageBonus(originalDamage)
    # elif organicBonus or propBonus:
    #     damage += getDamageBonus(damage)
    return damage


def get_gag_exp(track: int, current_exps: list) -> int:
    """Get EXP for a Toon's Gag Track, given track# and list of Gag exps

    Args:
        track (int): Index number of the Gag Track <0-6>
        current_exps (list): Ordered 7-member list of all Gag Track EXPs, can
                             be obtained from Toon.track_exps
            `current_exps` ordered structure ::
                [
                    HEAL_TRACK_XP,    # 0
                    TRAP_TRACK_XP,    # 1
                    LURE_TRACK_XP,    # 2
                    SOUND_TRACK_XP,   # 3
                    THROW_TRACK_XP,   # 4
                    SQUIRT_TRACK_XP,  # 5
                    DROP_TRACK_XP     # 6
                ]

    Returns:
        int: Current Gag Track EXP
    """
    return current_exps[track]


def get_gag_exp_needed(track: int, level: int, current_exps: list = None,
                       current_exp: int = None) -> int:  # noqa
    """Return the Gag Track EXP required to advance to next Gag Track level

    Args:
        track (int): Index number of the Gag Track <0-6>
        level (int): Level of the Gag <0-6>
        current_exps (list): Ordered 7-member list of all Gag Track EXPs, can
                             be obtained from Toon.track_exps
            `current_exps` ordered structure ::
                [
                    HEAL_TRACK_XP,    # 0
                    TRAP_TRACK_XP,    # 1
                    LURE_TRACK_XP,    # 2
                    SOUND_TRACK_XP,   # 3
                    THROW_TRACK_XP,   # 4
                    SQUIRT_TRACK_XP,  # 5
                    DROP_TRACK_XP     # 6
                ]

    Returns:
        int: EXP required to advance to next Gag Track level
    """
    assert current_exp or current_exps
    if current_exps:  # If passing in Toon's EXPs
        current_exp = get_gag_exp(track, current_exps)

    next_gag_exp = LEVELS[track][level]
    return next_gag_exp - current_exp


def get_gag_min_max_damage(track: int, level: int) -> tuple[int, int]:
    return GAG_DAMAGE[track][level][0]


def get_gag_min_max_exp(track: int, level: int) -> tuple[int, int]:
    return GAG_DAMAGE[track][level][1]


def get_gag_label(track: int, level: int) -> str:
    """Return name of the Gag, given a track# and level#

    Args:
        track (int): Index number of the Gag Track <0-6>
        level (int): Level of the Gag <0-6>

    Returns:
        str: Name of the Gag, typically used for logging messages
    """
    return GAG_LABELS[track][level]


def get_gag_name(track: int, level: int) -> str:
    """Return name of the Gag, given a track# and level#

    Args:
        track (int): Index number of the Gag Track <0-6>
        level (int): Level of the Gag <0-6>

    Returns:
        str: Name of the Gag, typically used for logging messages
    """
    return GAG.from_tuple((track, level)).name


def get_gag_target(name: str):
    """Return whether a Gag attacks is single-target or multi-target

    Args:
        name (str): Name of the Gag

    Returns:
        int: Single-target (1) or multi-target (2)
    """
    return GROUP.MULTI if name in MULTI_TARGET_GAGS else GROUP.SINGLE


def get_gag_track_label(track: int) -> str:
    """Return name of the Gag Track, given a track#

    Args:
        track (int): Index number of the Gag Track <0-6>

    Returns:
        str: Name of the Gag Track, typically used for logging messages
    """
    return GAG_TRACK_LABELS[track]


def get_gag_track_name(track: int) -> str:
    """Return name of the Gag Track, given a track#

    Args:
        track (int): Index number of the Gag Track <0-6>

    Returns:
        str: Name of the Gag Track, typically used for logging messages
    """
    return TRACK(track).name
