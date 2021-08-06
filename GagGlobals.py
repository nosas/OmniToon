# Original: https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/toonbase/ToontownBattleGlobals.py  # noqa
from __future__ import annotations

from enum import Enum, IntEnum
from typing import Tuple, Union


# Gag track indices
class TRACK(IntEnum):
    HEAL = 0
    TRAP = 1
    LURE = 2
    SOUND = 3
    THROW = 4
    SQUIRT = 5
    DROP = 6


# Gag indices
class GAG(bytes, Enum):

    @staticmethod
    def _get_gag_idx(track: int, gag_level: int) -> int:
        return track * 7 + gag_level

    def __new__(cls, track: TRACK, level: int):
        gag_index = cls._get_gag_idx(track=track, gag_level=level)
        obj = bytes.__new__(cls, [gag_index])
        obj._value_ = gag_index
        obj._value = (track, level)
        obj._track = track
        obj._level = level
        return obj

    @classmethod
    def from_tuple(cls, track_gag_tuple: Tuple[Union[TRACK | int], int]) -> GAG:
        """Return GAG enum object from a tuple containing TRACK, gag_level

        Example: (TRACK.HEAL, 0) return GAG.FEATHER
                 (TRACK.HEAL.value, 0) also returns GAG.FEATHER
                 (0, 0) also returns GAG.FEATHER
        Args:
            track_gag_tuple (Tuple[Union[TRACK): Tuple containing TRACK, gag_level

        Returns:
            GAG: GAG enum object
        """
        track = TRACK(track_gag_tuple[0])
        gag_level = track_gag_tuple[1]
        return cls(cls._get_gag_idx(track=track, gag_level=gag_level))

    @property
    def track(self) -> TRACK:
        # return self.value[0].value
        return self._track

    @property
    def level(self) -> int:
        # return self.value[1]
        return self._level

    @property
    def value(self) -> Tuple[TRACK, int]:
        return (self._track, self._level)

    FEATHER = (TRACK.HEAL, 0)
    MEGAPHONE = (TRACK.HEAL, 1)
    LIPSTICK = (TRACK.HEAL, 2)
    BAMBOO_CANE = (TRACK.HEAL, 3)
    PIXIE_DUST = (TRACK.HEAL, 4)
    JUGGLING_BALLS = (TRACK.HEAL, 5)
    HIGH_DIVE = (TRACK.HEAL, 6)

    BANANA_PEEL = (TRACK.TRAP, 0)
    RAKE = (TRACK.TRAP, 1)
    MARBLES = (TRACK.TRAP, 2)
    QUICKSAND = (TRACK.TRAP, 3)
    TRAPDOOR = (TRACK.TRAP, 4)
    TNT = (TRACK.TRAP, 5)
    RAILROAD = (TRACK.TRAP, 6)

    ONE_BILL = (TRACK.LURE, 0)
    SMALL_MAGNET = (TRACK.LURE, 1)
    FIVE_BILL = (TRACK.LURE, 2)
    BIG_MAGNET = (TRACK.LURE, 3)
    TEN_BILL = (TRACK.LURE, 4)
    HYPNO_GOGGLES = (TRACK.LURE, 5)
    PRESENTATION = (TRACK.LURE, 6)

    BIKE_HORN = (TRACK.SOUND, 0)
    WHISTLE = (TRACK.SOUND, 1)
    BUGLE = (TRACK.SOUND, 2)
    AOOGAH = (TRACK.SOUND, 3)
    ELEPHANT_TRUNK = (TRACK.SOUND, 4)
    FOGHORN = (TRACK.SOUND, 5)
    OPERA_SINGER = (TRACK.SOUND, 6)

    CUPCAKE = (TRACK.THROW, 0)
    FRUIT_PIE_SLICE = (TRACK.THROW, 1)
    CREAM_PIE_SLICE = (TRACK.THROW, 2)
    WHOLE_FRUIT_PIE = (TRACK.THROW, 3)
    WHOLE_CREAM_PIE = (TRACK.THROW, 4)
    BIRTHDAY_CAKE = (TRACK.THROW, 5)
    WEDDING_CAKE = (TRACK.THROW, 6)

    SQUIRTING_FLOWER = (TRACK.SQUIRT, 0)
    GLASS_OF_WATER = (TRACK.SQUIRT, 1)
    SQUIRT_GUN = (TRACK.SQUIRT, 2)
    SELTZER_BOTTLE = (TRACK.SQUIRT, 3)
    FIRE_HOSE = (TRACK.SQUIRT, 4)
    STORM_CLOUD = (TRACK.SQUIRT, 5)
    GEYSER = (TRACK.SQUIRT, 6)

    FLOWER_POT = (TRACK.DROP, 0)
    SANDBAG = (TRACK.DROP, 1)
    ANVIL = (TRACK.DROP, 2)
    BIG_WEIGHT = (TRACK.DROP, 3)
    SAFE = (TRACK.DROP, 4)
    GRAND_PIANO = (TRACK.DROP, 5)
    TOONTANIC = (TRACK.DROP, 6)


REG_MAX_SKILL = 10000  # Max gag EXP
UBER_SKILL = 500       # EXP required to unlock final gag
MAX_SKILL = UBER_SKILL + REG_MAX_SKILL
GAG_TRACK_LABELS = ["Toon-Up", "Trap", "Lure", "Sound",
                    "Throw", "Squirt", "Drop"]
GAG_LABELS = (
    ('Feather', 'Megaphone', 'Lipstick', 'Bamboo Cane',
        'Pixie Dust', 'Juggling Balls', 'High Dive'),  # Toon-up
    ('Banana Peel', 'Rake', 'Marbles', 'Quicksand',
        'Trapdoor', 'TNT', 'Railroad'),  # Trap
    ('$1 bill', 'Small Magnet', '$5 bill', 'Big Magnet',
        '$10 bill', 'Hypno-goggles', 'Presentation'),  # Lure
    ('Bike Horn', 'Whistle', 'Bugle', 'Aoogah',
        'Elephant Trunk', 'Foghorn', 'Opera Singer'),  # Sound
    ('Cupcake', 'Fruit Pie Slice', 'Cream Pie Slice', 'Whole Fruit Pie',
        'Whole Cream Pie', 'Birthday Cake', 'Wedding Cake'),  # Throw
    ('Squirting Flower', 'Glass of Water', 'Squirt Gun', 'Seltzer Bottle',
        'Fire Hose', 'Storm Cloud', 'Geyser'),  # Squirt
    ('Flower Pot', 'Sandbag', 'Anvil', 'Big Weight',
        'Safe', 'Grand Piano', 'Toontanic')  # Drop
)
# Experience points needed to unlock the gag at the indexed position
LEVELS = [[0, 20, 200, 800, 2000, 6000, 10000],    # Toon-Up
          [0, 20, 100, 800, 2000, 6000, 10000],    # Trap
          [0, 20, 100, 800, 2000, 6000, 10000],    # Lure
          [0, 40, 200, 1000, 2500, 7500, 10000],   # Sound
          [0, 10, 50, 400, 2000, 6000, 10000],     # Throw
          [0, 10, 50, 400, 2000, 6000, 10000],     # Squirt
          [0, 20, 100, 500, 2000, 6000, 10000]]    # Drop

# -1 means the gag_track is locked, 0 means lvl 1 Gag is unlocked
DEFAULT_TRACK_LEVELS = [-1, -1, -1, -1, 0, 0, -1]
DEFAULT_TRACK_EXPS_CURRENT = DEFAULT_TRACK_LEVELS
# Populate DEFAULT_TRACK_EXPS_NEXT from Gag track levels in DEFAULT_LEVELS
# NOTE: The EXP value is the required to level up the Gag
# DEFAULT_TRACK_EXPS_NEXT = [0, 0, 0, 0, 10, 10, 0]
DEFAULT_TRACK_EXPS_NEXT = [
    LEVELS[track_idx][level + 1] for
    track_idx, level in enumerate(DEFAULT_TRACK_LEVELS)
]
# DEFAULT_EXPS = [0, 0, 0, 0, 10, 10, 0]
DEFAULT_GAG_COUNT = [[-1, -1, -1, -1, -1, -1, -1],  # Toon-Up
                     [-1, -1, -1, -1, -1, -1, -1],  # Trap
                     [-1, -1, -1, -1, -1, -1, -1],  # Lure
                     [-1, -1, -1, -1, -1, -1, -1],  # Sound
                     [0,  -1, -1, -1, -1, -1, -1],  # Throw
                     [0,  -1, -1, -1, -1, -1, -1],  # Squirt
                     [-1, -1, -1, -1, -1, -1, -1]]  # Drop
DEFAULT_GAG_LIMIT = 20

# MIN_MAX_TUPLE = GAG_DAMAGE[GAG_TRACK_INDEX][GAG_LEVEL] = ((min_dmg, max_dmg), (min_exp, max_exp))  # noqa
# MIN_DMG, MAX_DMG = MIN_MAX_TUPLE[0] = (min_dmg, max_dmg)
# MIN_EXP, MAX_EXP = MIN_MAX_TUPLE[1] = (min_exp, max_exp)
#    Example of Level 3 Throw min/max = GAG_DAMAGE[4][3]
GAG_DAMAGE = (
    (((8, 10), (LEVELS[TRACK.HEAL][0], LEVELS[TRACK.HEAL][1])),      # Toon-Up
        ((15, 18), (LEVELS[TRACK.HEAL][1], LEVELS[TRACK.HEAL][2])),
        ((25, 30), (LEVELS[TRACK.HEAL][2], LEVELS[TRACK.HEAL][3])),
        ((40, 45), (LEVELS[TRACK.HEAL][3], LEVELS[TRACK.HEAL][4])),
        ((60, 70), (LEVELS[TRACK.HEAL][4], LEVELS[TRACK.HEAL][5])),
        ((90, 120), (LEVELS[TRACK.HEAL][5], LEVELS[TRACK.HEAL][6])),
        ((210, 210), (LEVELS[TRACK.HEAL][6], MAX_SKILL))),
    (((10, 12), (LEVELS[TRACK.TRAP][0], LEVELS[TRACK.TRAP][1])),     # Trap
        ((18, 20), (LEVELS[TRACK.TRAP][1], LEVELS[TRACK.TRAP][2])),
        ((30, 35), (LEVELS[TRACK.TRAP][2], LEVELS[TRACK.TRAP][3])),
        ((45, 50), (LEVELS[TRACK.TRAP][3], LEVELS[TRACK.TRAP][4])),
        ((60, 70), (LEVELS[TRACK.TRAP][4], LEVELS[TRACK.TRAP][5])),
        ((90, 180), (LEVELS[TRACK.TRAP][5], LEVELS[TRACK.TRAP][6])),
        ((195, 195), (LEVELS[TRACK.TRAP][6], MAX_SKILL))),
    (((0, 0), (LEVELS[TRACK.LURE][0], LEVELS[TRACK.LURE][1])),       # Lure
        ((0, 0), (LEVELS[TRACK.LURE][1], LEVELS[TRACK.LURE][2])),
        ((0, 0), (LEVELS[TRACK.LURE][2], LEVELS[TRACK.LURE][3])),
        ((0, 0), (LEVELS[TRACK.LURE][3], LEVELS[TRACK.LURE][4])),
        ((0, 0), (LEVELS[TRACK.LURE][4], LEVELS[TRACK.LURE][5])),
        ((0, 0), (LEVELS[TRACK.LURE][5], LEVELS[TRACK.LURE][6])),
        ((0, 0), (LEVELS[TRACK.LURE][6], MAX_SKILL))),
    (((3, 4), (LEVELS[TRACK.SOUND][0], LEVELS[TRACK.SOUND][1])),       # Sound
        ((5, 7), (LEVELS[TRACK.SOUND][1], LEVELS[TRACK.SOUND][2])),
        ((9, 11), (LEVELS[TRACK.SOUND][2], LEVELS[TRACK.SOUND][3])),
        ((14, 16), (LEVELS[TRACK.SOUND][3], LEVELS[TRACK.SOUND][4])),
        ((19, 21), (LEVELS[TRACK.SOUND][4], LEVELS[TRACK.SOUND][5])),
        ((25, 50), (LEVELS[TRACK.SOUND][5], LEVELS[TRACK.SOUND][6])),
        ((90, 90), (LEVELS[TRACK.SOUND][6], MAX_SKILL))),
    (((4, 6), (LEVELS[TRACK.THROW][0], LEVELS[TRACK.THROW][1])),       # Throw
        ((8, 10), (LEVELS[TRACK.THROW][1], LEVELS[TRACK.THROW][2])),
        ((14, 17), (LEVELS[TRACK.THROW][2], LEVELS[TRACK.THROW][3])),
        ((24, 27), (LEVELS[TRACK.THROW][3], LEVELS[TRACK.THROW][4])),
        ((36, 40), (LEVELS[TRACK.THROW][4], LEVELS[TRACK.THROW][5])),
        ((48, 100), (LEVELS[TRACK.THROW][5], LEVELS[TRACK.THROW][6])),
        ((120, 120), (LEVELS[TRACK.THROW][6], MAX_SKILL))),
    (((3, 4), (LEVELS[TRACK.SQUIRT][0], LEVELS[TRACK.SQUIRT][1])),     # Squirt
        ((6, 8), (LEVELS[TRACK.SQUIRT][1], LEVELS[TRACK.SQUIRT][2])),
        ((10, 12), (LEVELS[TRACK.SQUIRT][2], LEVELS[TRACK.SQUIRT][3])),
        ((18, 21), (LEVELS[TRACK.SQUIRT][3], LEVELS[TRACK.SQUIRT][4])),
        ((27, 30), (LEVELS[TRACK.SQUIRT][4], LEVELS[TRACK.SQUIRT][5])),
        ((36, 80), (LEVELS[TRACK.SQUIRT][5], LEVELS[TRACK.SQUIRT][6])),
        ((105, 105), (LEVELS[TRACK.SQUIRT][6], MAX_SKILL))),
    (((10, 10), (LEVELS[TRACK.DROP][0], LEVELS[TRACK.DROP][1])),     # Drop
        ((18, 18), (LEVELS[TRACK.DROP][1], LEVELS[TRACK.DROP][2])),
        ((30, 30), (LEVELS[TRACK.DROP][2], LEVELS[TRACK.DROP][3])),
        ((45, 45), (LEVELS[TRACK.DROP][3], LEVELS[TRACK.DROP][4])),
        ((60, 60), (LEVELS[TRACK.DROP][4], LEVELS[TRACK.DROP][5])),
        ((85, 170), (LEVELS[TRACK.DROP][5], LEVELS[TRACK.DROP][6])),
        ((180, 180), (LEVELS[TRACK.DROP][6], MAX_SKILL)))
)

GAG_CARRY_LIMITS = (((10, 0, 0, 0, 0, 0, 0),      # Toon-up
                     (10, 5, 0, 0, 0, 0, 0),      # Gag level 1
                     (15, 10, 5, 0, 0, 0, 0),     # Gag level 2
                     (20, 15, 10, 5, 0, 0, 0),    # Gag level 3
                     (25, 20, 15, 10, 3, 0, 0),   # Gag level 4
                     (30, 25, 20, 15, 7, 3, 0),   # Gag level 5
                     (30, 25, 20, 15, 7, 3, 1)),  # Gag level 6
                    ((5, 0, 0, 0, 0, 0, 0),       # ! Trap, unique carry limit
                     (7, 3, 0, 0, 0, 0, 0),
                     (10, 7, 3, 0, 0, 0, 0),
                     (15, 10, 7, 3, 0, 0, 0),
                     (15, 15, 10, 5, 3, 0, 0),
                     (20, 15, 15, 10, 5, 2, 0),
                     (20, 15, 15, 10, 5, 2, 1)),
                    ((10, 0, 0, 0, 0, 0, 0),      # Lure
                     (10, 5, 0, 0, 0, 0, 0),
                     (15, 10, 5, 0, 0, 0, 0),
                     (20, 15, 10, 5, 0, 0, 0),
                     (25, 20, 15, 10, 3, 0, 0),
                     (30, 25, 20, 15, 7, 3, 0),
                     (30, 25, 20, 15, 7, 3, 1)),
                    ((10, 0, 0, 0, 0, 0, 0),      # Sound
                     (10, 5, 0, 0, 0, 0, 0),
                     (15, 10, 5, 0, 0, 0, 0),
                     (20, 15, 10, 5, 0, 0, 0),
                     (25, 20, 15, 10, 3, 0, 0),
                     (30, 25, 20, 15, 7, 3, 0),
                     (30, 25, 20, 15, 7, 3, 1)),
                    ((10, 0, 0, 0, 0, 0, 0),      # Throw
                     (10, 5, 0, 0, 0, 0, 0),
                     (15, 10, 5, 0, 0, 0, 0),
                     (20, 15, 10, 5, 0, 0, 0),
                     (25, 20, 15, 10, 3, 0, 0),
                     (30, 25, 20, 15, 7, 3, 0),
                     (30, 25, 20, 15, 7, 3, 1)),
                    ((10, 0, 0, 0, 0, 0, 0),      # Squirt
                     (10, 5, 0, 0, 0, 0, 0),
                     (15, 10, 5, 0, 0, 0, 0),
                     (20, 15, 10, 5, 0, 0, 0),
                     (25, 20, 15, 10, 3, 0, 0),
                     (30, 25, 20, 15, 7, 3, 0),
                     (30, 25, 20, 15, 7, 3, 1)),
                    ((10, 0, 0, 0, 0, 0, 0),      # Drop
                     (10, 5, 0, 0, 0, 0, 0),
                     (15, 10, 5, 0, 0, 0, 0),
                     (20, 15, 10, 5, 0, 0, 0),
                     (25, 20, 15, 10, 3, 0, 0),
                     (30, 25, 20, 15, 7, 3, 0),
                     (30, 25, 20, 15, 7, 3, 1)))

MULTI_TARGET_GAGS = [
    'MEGAPHONE', 'BAMBOO_CANE', 'JUGGLING_BALLS', 'HIGH_DIVE', 'RAILROAD',
    'SMALL_MAGNET', 'BIG_MAGNET', 'HYPNO_GOGGLES', 'PRESENTATION', 'BIKE_HORN',
    'WHISTLE', 'BUGLE', 'AOOGAH', 'ELEPHANT_TRUNK', 'FOGHORN', 'OPERA_SINGER',
    'WEDDING_CAKE', 'GEYSER', 'TOONTANIC'
]
