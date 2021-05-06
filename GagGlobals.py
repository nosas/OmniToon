# %% Import functions, define globals
# Original: https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/toonbase/ToontownBattleGlobals.py  # noqa

from math import floor as math_floor

from .Attack import ATK_TGT_MULTI, ATK_TGT_SINGLE

# Gag track indexes
HEAL_TRACK = 0
TRAP_TRACK = 1
LURE_TRACK = 2
SOUND_TRACK = 3
THROW_TRACK = 4
SQUIRT_TRACK = 5
DROP_TRACK = 6
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

# MIN_MAX_TUPLE = GAG_DAMAGE[GAG_TRACK_INDEX][GAG_LEVEL] = ((min_dmg, max_dmg), (min_exp, max_exp))  # noqa
# MIN_DMG, MAX_DMG = MIN_MAX_TUPLE[0] = (min_dmg, max_dmg)
# MIN_EXP, MAX_EXP = MIN_MAX_TUPLE[1] = (min_exp, max_exp)
#    Example of Level 3 Throw min/max = GAG_DAMAGE[4][3]
GAG_DAMAGE = (
    (((8, 10), (LEVELS[HEAL_TRACK][0], LEVELS[HEAL_TRACK][1])),      # Toon-Up
        ((15, 18), (LEVELS[HEAL_TRACK][1], LEVELS[HEAL_TRACK][2])),
        ((25, 30), (LEVELS[HEAL_TRACK][2], LEVELS[HEAL_TRACK][3])),
        ((40, 45), (LEVELS[HEAL_TRACK][3], LEVELS[HEAL_TRACK][4])),
        ((60, 70), (LEVELS[HEAL_TRACK][4], LEVELS[HEAL_TRACK][5])),
        ((90, 120), (LEVELS[HEAL_TRACK][5], LEVELS[HEAL_TRACK][6])),
        ((210, 210), (LEVELS[HEAL_TRACK][6], MAX_SKILL))),
    (((10, 12), (LEVELS[TRAP_TRACK][0], LEVELS[TRAP_TRACK][1])),     # Trap
        ((18, 20), (LEVELS[TRAP_TRACK][1], LEVELS[TRAP_TRACK][2])),
        ((30, 35), (LEVELS[TRAP_TRACK][2], LEVELS[TRAP_TRACK][3])),
        ((45, 50), (LEVELS[TRAP_TRACK][3], LEVELS[TRAP_TRACK][4])),
        ((60, 70), (LEVELS[TRAP_TRACK][4], LEVELS[TRAP_TRACK][5])),
        ((90, 180), (LEVELS[TRAP_TRACK][5], LEVELS[TRAP_TRACK][6])),
        ((195, 195), (LEVELS[TRAP_TRACK][6], MAX_SKILL))),
    (((0, 0), (LEVELS[LURE_TRACK][0], LEVELS[LURE_TRACK][1])),       # Lure
        ((0, 0), (LEVELS[LURE_TRACK][1], LEVELS[LURE_TRACK][2])),
        ((0, 0), (LEVELS[LURE_TRACK][2], LEVELS[LURE_TRACK][3])),
        ((0, 0), (LEVELS[LURE_TRACK][3], LEVELS[LURE_TRACK][4])),
        ((0, 0), (LEVELS[LURE_TRACK][4], LEVELS[LURE_TRACK][5])),
        ((0, 0), (LEVELS[LURE_TRACK][5], LEVELS[LURE_TRACK][6])),
        ((0, 0), (LEVELS[LURE_TRACK][6], MAX_SKILL))),
    (((3, 4), (LEVELS[SOUND_TRACK][0], LEVELS[SOUND_TRACK][1])),       # Sound
        ((5, 7), (LEVELS[SOUND_TRACK][1], LEVELS[SOUND_TRACK][2])),
        ((9, 11), (LEVELS[SOUND_TRACK][2], LEVELS[SOUND_TRACK][3])),
        ((14, 16), (LEVELS[SOUND_TRACK][3], LEVELS[SOUND_TRACK][4])),
        ((19, 21), (LEVELS[SOUND_TRACK][4], LEVELS[SOUND_TRACK][5])),
        ((25, 50), (LEVELS[SOUND_TRACK][5], LEVELS[SOUND_TRACK][6])),
        ((90, 90), (LEVELS[SOUND_TRACK][6], MAX_SKILL))),
    (((4, 6), (LEVELS[THROW_TRACK][0], LEVELS[THROW_TRACK][1])),       # Throw
        ((8, 10), (LEVELS[THROW_TRACK][1], LEVELS[THROW_TRACK][2])),
        ((14, 17), (LEVELS[THROW_TRACK][2], LEVELS[THROW_TRACK][3])),
        ((24, 27), (LEVELS[THROW_TRACK][3], LEVELS[THROW_TRACK][4])),
        ((36, 40), (LEVELS[THROW_TRACK][4], LEVELS[THROW_TRACK][5])),
        ((48, 100), (LEVELS[THROW_TRACK][5], LEVELS[THROW_TRACK][6])),
        ((120, 120), (LEVELS[THROW_TRACK][6], MAX_SKILL))),
    (((3, 4), (LEVELS[SQUIRT_TRACK][0], LEVELS[SQUIRT_TRACK][1])),     # Squirt
        ((6, 8), (LEVELS[SQUIRT_TRACK][1], LEVELS[SQUIRT_TRACK][2])),
        ((10, 12), (LEVELS[SQUIRT_TRACK][2], LEVELS[SQUIRT_TRACK][3])),
        ((18, 21), (LEVELS[SQUIRT_TRACK][3], LEVELS[SQUIRT_TRACK][4])),
        ((27, 30), (LEVELS[SQUIRT_TRACK][4], LEVELS[SQUIRT_TRACK][5])),
        ((36, 80), (LEVELS[SQUIRT_TRACK][5], LEVELS[SQUIRT_TRACK][6])),
        ((105, 105), (LEVELS[SQUIRT_TRACK][6], MAX_SKILL))),
    (((10, 10), (LEVELS[DROP_TRACK][0], LEVELS[DROP_TRACK][1])),     # Drop
        ((18, 18), (LEVELS[DROP_TRACK][1], LEVELS[DROP_TRACK][2])),
        ((30, 30), (LEVELS[DROP_TRACK][2], LEVELS[DROP_TRACK][3])),
        ((45, 45), (LEVELS[DROP_TRACK][3], LEVELS[DROP_TRACK][4])),
        ((60, 60), (LEVELS[DROP_TRACK][4], LEVELS[DROP_TRACK][5])),
        ((85, 170), (LEVELS[DROP_TRACK][5], LEVELS[DROP_TRACK][6])),
        ((180, 180), (LEVELS[DROP_TRACK][6], MAX_SKILL)))
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
    'Megaphone', 'Bamboo Cane', 'Juggling Balls', 'High Dive', 'Railroad',
    'Small Magnet', 'Big Magnet', 'Hypno-goggles', 'Presentation',
    'Bike Horn', 'Whistle', 'Bugle', 'Aoogah', 'Elephant Trunk', 'Foghorn',
    'Opera Singer', 'Wedding Cake', 'Geyser', 'Toontanic'
    ]


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
                             be obtained from Toon.gag_exps
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
                             be obtained from Toon.gag_exps
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


def get_gag_name(track: int, level: int) -> str:
    """Return name of the Gag, given a track# and level#

    Args:
        track (int): Index number of the Gag Track <0-6>
        level (int): Level of the Gag <0-6>

    Returns:
        str: Name of the Gag, typically used for logging messages
    """
    return GAG_LABELS[track][level]


def get_gag_target(name: str):
    """Return whether a Gag attacks is single-target or multi-target

    Args:
        name (str): Name of the Gag

    Returns:
        int: Single-target (1) or multi-target (2)
    """
    return ATK_TGT_MULTI if name in MULTI_TARGET_GAGS else ATK_TGT_SINGLE


def get_gag_track_name(track: int) -> str:
    """Return name of the Gag Track, given a track#

    Args:
        track (int): Index number of the Gag Track <0-6>

    Returns:
        str: Name of the Gag Track, typically used for logging messages
    """
    return GAG_TRACK_LABELS[track]
