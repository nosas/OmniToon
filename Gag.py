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
from typing import List, Optional

from .AttackGlobals import GROUP
from .Exceptions import (GagCountError, LockedGagError, LockedGagTrackError,
                         NotEnoughGagsError)

from .GagGlobals import (DEFAULT_GAG_COUNT, DEFAULT_TRACK_EXPS_CURRENT, GAG,
                         GAG_CARRY_LIMITS, GAG_DAMAGE, GAG_LABELS,
                         GAG_TRACK_LABELS, LEVELS, MULTI_TARGET_GAGS, TRACK)


def get_default_gag_count() -> List[List[int]]:
    return DEFAULT_GAG_COUNT.copy()


def get_default_exps_current() -> List[int]:
    return DEFAULT_TRACK_EXPS_CURRENT.copy()


def get_default_gags() -> List[List[Gag]]:
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
        exp (int): EXP of the Gag Track <-1-10499>
        level (int): Level of the Gag <0-6>
        track (int): Index of the Gag Track <0-6>
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
    """Collection of Gags and Gag-related function

    Args:
        gag_count (list, optional): 2-D list, ex: `gags[GAG_TRACK][GAG_LEVEL]`.
            Defaults to DEFAULT_GAG_COUNTS.
            Example `gag_count` ::
                gag_count = [[0,   0,  0,  5,  5,  3, -1],  # 0 Toon-up
                             [-1, -1, -1, -1, -1, -1, -1],  # 1 Trap (locked)
                             [0,   0,  0,  0,  5,  3,  1],  # 2 Lure
                             [0,   0,  0,  0,  5,  3, -1],  # 3 Sound
                             [0,   2,  1,  4,  4,  2, -1],  # 4 Throw
                             [0,   0,  0,  5,  5,  3, -1],  # 5 Squirt
                             [0,   9,  5, -1, -1, -1, -1]]  # 6 Drop
        track_exps (list, optional): List containing Gag Track EXP.
            Defaults to DEFAULT_TRACK_EXPS_CURRENT.
            Example `track_exps` ::
                track_exps = [7421,   # 0 Toon-up
                              -1,     # 1 Trap (locked)
                              10101,  # 2 Lure
                              9443,   # 3 Sound
                              8690,   # 4 Throw
                              6862,   # 5 Squirt
                              191]    # 6 Drop

    Raises:
        GagCountError: Raised when counting Gags and Gag count is less than 0
        NotEnoughGagsError: Raised when choosing a Gag whose count is 0
        LockedGagTrackError: Raised when choosing a Gag whose Gag Track is locked
        LockedGagError: Raised when choosing a locked Gag

    """

    gag_count: List[List[int]] = field(default_factory=get_default_gag_count)
    track_exps: Optional[List[int]] = field(default_factory=get_default_exps_current)

    @property
    def track_levels(self) -> List[int]:
        """Return ordered (by Gag Track index) list of Gag Track exps"""
        return self._calculate_gag_levels_from_gag_count()

    @property
    def gags(self):
        """Create a 2D list of Gag objects"""
        all_gags = [self._get_gag(level=gag_enum.level, track=gag_enum.track) for gag_enum in GAG]
        return [all_gags[track*7:(track+1)*7] for track in TRACK]

    @property
    def unlocked_gags(self) -> List[Gag]:
        """Return a flattened list of unlocked Gags"""
        return [gag for gag in self._flatten_gags() if gag.count != -1]

    @property
    def available_gags(self) -> List[Gag]:
        """Return a flattened list of available (unlocked, count > 0) Gags"""
        return [gag for gag in self.unlocked_gags if gag.count > 0]

    def __iter__(self):
        return iter(self._flatten_gags())

    def _flatten_gags(self) -> List[Gag]:
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
        return [(6 - track.count(-1)) for track in self.gag_count]

    def _count_all_gags(self) -> int:
        """Return the Toon's total number of usable Gags

        Returns:
            int: Total number of Gags
        """
        count = count_all_gags(gag_count=self.gag_count)

        # if count > self.gag_limit:
        #     raise TooManyGagsError(count, self.gag_limit)
        if count < 0:
            raise GagCountError
        return count

    def _count_gag(self, track: int, level: int) -> int:
        """Return Toon's current quantity of a Gag(track, level)

        Args:
            track (int): Index number of the Gag Track <0-6>
            level (int): Level of the Gag <0-6>

        Returns:
            int: Current quantity of a Gag
        """
        return self.gag_count[track][level]

    def _count_gag_track(self, track: int) -> int:
        """Return Toon's current number of Gags in a Gag track

        Args:
            track (int): Index number of the Gag Track <0-6>

        Returns:
            int: Current quantity of a Gag track
        """
        return sum(self.gag_count[track], start=self.gag_count[track].count(-1))

    def _get_gag(self, track: int, level: int) -> Gag:
        # count_max =  # ! TODO #42
        return Gag(track=track, level=level,
                   exp=self.get_gag_exp(track=track),
                   count=self._count_gag(track=track, level=level))

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

    def get_gag(self, track: int, level: int) -> Gag:
        """Return Gag object containing Gag's vital info, iff Toon has the Gag

        Args:
            track (int): Index number of the Gag Track <0-6>
            level (int): Level of the Gag <0-6>


        Returns:
            Gag: Vital information about the Toon's Gag
        """
        gag = self._get_gag(track=track, level=level)
        if gag.count == 0:
            raise NotEnoughGagsError(gag)
        if self.gag_count[track] == [-1] * 7:
            raise LockedGagTrackError(track=track)
        if gag.count == -1:
            raise LockedGagError(level=level)

        print(f"        [+] Toon `choose_gag()` {self} : {gag}")
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
        return self.track_exps[track]

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


def count_all_gags(gag_count: list) -> int:
    """Return the total number of Gags, given a 2-D list of Gags

    Args:
        gags (2-D list): List of Gags, can be obtained from Toon.gag_counts
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
    return sum(sum(gag_track) for gag_track in gag_count)


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
        current_exp (int): Gag track's current EXP value

    Returns:
        int: EXP required to advance to next Gag Track level
    """
    assert current_exp or current_exps
    if current_exps:  # If passing in Toon's EXPs
        current_exp = get_gag_exp(track, current_exps)

    next_gag_exp = LEVELS[track][level]
    return next_gag_exp - current_exp


def get_gag_min_max_damage(track: int, level: int) -> tuple[int, int]:
    """Return a tuple of the Gag's min/max damage

    Args:
        track (int): Index number of the Gag Track <0-6>
        level (int): Level of the Gag <0-6>

    Returns:
        tuple[int, int]: (Minimum damage, maximum damage)
    """
    return GAG_DAMAGE[track][level][0]


def get_gag_min_max_exp(track: int, level: int) -> tuple[int, int]:
    """Return a tuple of the Gag's min/max EXP

    Minimum EXP required to unlock this Gag, maximum EXP to unlock following Gag.
    This EXP is also used to calculate the Gag's current damage value.

    Args:
        track (int): Index number of the Gag Track <0-6>
        level (int): Level of the Gag <0-6>

    Returns:
        tuple[int, int]: (Minimum EXP, maximum EXP)
    """
    return GAG_DAMAGE[track][level][1]


def get_gag_label(track: int, level: int) -> str:
    """Return label of the Gag, given a track# and level#

    Args:
        track (int): Index number of the Gag Track <0-6>
        level (int): Level of the Gag <0-6>

    Returns:
        str: Label of the Gag, typically used for logging messages
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
    """Return label of the Gag Track, given a track#

    Args:
        track (int): Index number of the Gag Track <0-6>

    Returns:
        str: Label of the Gag Track, typically used for logging messages
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
