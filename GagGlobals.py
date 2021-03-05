# %% Import functions, define globals
# Original: https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/toonbase/ToontownBattleGlobals.py  # noqa

from math import floor as math_floor

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
    (((8, 10), (LEVELS[0][0], LEVELS[0][1])),      # Toon-Up
        ((15, 18), (LEVELS[0][1], LEVELS[0][2])),
        ((25, 30), (LEVELS[0][2], LEVELS[0][3])),
        ((40, 45), (LEVELS[0][3], LEVELS[0][4])),
        ((60, 70), (LEVELS[0][4], LEVELS[0][5])),
        ((90, 120), (LEVELS[0][5], LEVELS[0][6])),
        ((210, 210), (LEVELS[0][6], MAX_SKILL))),
    (((10, 12), (LEVELS[1][0], LEVELS[1][1])),     # Trap
        ((18, 20), (LEVELS[1][1], LEVELS[1][2])),
        ((30, 35), (LEVELS[1][2], LEVELS[1][3])),
        ((45, 50), (LEVELS[1][3], LEVELS[1][4])),
        ((60, 70), (LEVELS[1][4], LEVELS[1][5])),
        ((90, 180), (LEVELS[1][5], LEVELS[1][6])),
        ((195, 195), (LEVELS[1][6], MAX_SKILL))),
    (((0, 0), (0, 0)),                             # Lure
        ((0, 0), (0, 0)),
        ((0, 0), (0, 0)),
        ((0, 0), (0, 0)),
        ((0, 0), (0, 0)),
        ((0, 0), (0, 0)),
        ((0, 0), (0, 0))),
    (((3, 4), (LEVELS[3][0], LEVELS[3][1])),       # Sound
        ((5, 7), (LEVELS[3][1], LEVELS[3][2])),
        ((9, 11), (LEVELS[3][2], LEVELS[3][3])),
        ((14, 16), (LEVELS[3][3], LEVELS[3][4])),
        ((19, 21), (LEVELS[3][4], LEVELS[3][5])),
        ((25, 50), (LEVELS[3][5], LEVELS[3][6])),
        ((90, 90), (LEVELS[3][6], MAX_SKILL))),
    (((4, 6), (LEVELS[4][0], LEVELS[4][1])),       # Throw
        ((8, 10), (LEVELS[4][1], LEVELS[4][2])),
        ((14, 17), (LEVELS[4][2], LEVELS[4][3])),
        ((24, 27), (LEVELS[4][3], LEVELS[4][4])),
        ((36, 40), (LEVELS[4][4], LEVELS[4][5])),
        ((48, 100), (LEVELS[4][5], LEVELS[4][6])),
        ((120, 120), (LEVELS[4][6], MAX_SKILL))),
    (((3, 4), (LEVELS[5][0], LEVELS[5][1])),       # Squirt
        ((6, 8), (LEVELS[5][1], LEVELS[5][2])),
        ((10, 12), (LEVELS[5][2], LEVELS[5][3])),
        ((18, 21), (LEVELS[5][3], LEVELS[5][4])),
        ((27, 30), (LEVELS[5][4], LEVELS[5][5])),
        ((36, 80), (LEVELS[5][5], LEVELS[5][6])),
        ((105, 105), (LEVELS[5][6], MAX_SKILL))),
    (((10, 10), (LEVELS[6][0], LEVELS[6][1])),     # Drop
        ((18, 18), (LEVELS[6][1], LEVELS[6][2])),
        ((30, 30), (LEVELS[6][2], LEVELS[6][3])),
        ((45, 45), (LEVELS[6][3], LEVELS[6][4])),
        ((60, 60), (LEVELS[6][4], LEVELS[6][5])),
        ((85, 170), (LEVELS[6][5], LEVELS[6][6])),
        ((180, 180), (LEVELS[6][6], MAX_SKILL)))
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


def count_all_gags(gags: list) -> int:
    """Return the total number of Gags, given a 2-D list of Gags

    Args:
        gags (2-D list): List of Gags, can be obtained from Toon.gags
            `gags` structure ::
                DEFAULT_GAGS = [
                    [0, 0, 0, 0, 0, 0, 0],  # Toon-Up
                    [0, 0, 0, 0, 0, 0, 0],  # Trap
                    [0, 0, 0, 0, 0, 0, 0],  # Lure
                    [0, 0, 0, 0, 0, 0, 0],  # Sound
                    [0, 0, 0, 0, 0, 0, 0],  # Throw
                    [0, 0, 0, 0, 0, 0, 0],  # Squirt
                    [0, 0, 0, 0, 0, 0, 0]   # Drop
                ]

    Returns:
        int: Total number of Gags
    """
    count = 0
    for gag_track in gags:
        count += sum(gag_track)

    return count


def get_gag_accuracy(gag_track: int, gag_level: int) -> int:
    """atkAcc = propAcc + trackExp + tgtDef + bonus

    Args:
        gag_track (int): Index number of the Gag Track <0-6>
        gag_level (int): Level of the Gag <0-6>

    Returns:
        int: [description]
    """
    return -1  # ! TODOOOO


def get_gag_name(gag_track: int, gag_level: int) -> str:
    """Return name of the Gag, given a gag_track# and gag_level#

    Args:
        gag_track (int): Index number of the Gag Track <0-6>
        gag_level (int): Level of the Gag <0-6>

    Returns:
        str: Name of the Gag, typically used for logging messages
    """
    return GAG_LABELS[gag_track][gag_level]


def get_gag_track_name(gag_track: int) -> str:
    """Return name of the Gag Track, given a gag_track#

    Args:
        gag_track (int): Index number of the Gag Track <0-6>

    Returns:
        str: Name of the Gag Track, typically used for logging messages
    """
    return GAG_TRACK_LABELS[gag_track]


def get_gag_damage(gag_track: int, gag_level: int, exp: int) -> int:
    """Calculate and return Gag damage, given gag_track#, gag_level# and exp

    Args:
        gag_track (int): Index number of the Gag Track <0-6>
        gag_level (int): Level of the Gag <0-6>
        exp (int): Current EXP of the Gag Track <0-10000?>

    Returns:
        int: Damage of Gag
    """
    # MIN_MAX_TUPLE = GAG_DAMAGE[GAG_TRACK_INDEX][GAG_INDEX] =>
    #                 ((min_dmg, max_dmg), (min_exp, max_exp))
    # MIN_DMG, MAX_DMG = MIN_MAX_TUPLE[0] = (min_dmg, max_dmg)
    # MIN_EXP, MAX_EXP = MIN_MAX_TUPLE[1] = (min_exp, max_exp)
    #    Example of Level 3 Throw min/max = GAG_DAMAGE[4][3]

    min_dmg = GAG_DAMAGE[gag_track][gag_level][0][0]
    max_dmg = GAG_DAMAGE[gag_track][gag_level][0][1]
    min_exp = GAG_DAMAGE[gag_track][gag_level][1][0]
    max_exp = GAG_DAMAGE[gag_track][gag_level][1][1]
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


def get_gag_exp(gag_track: int, current_exps: list) -> int:
    """Get EXP for a Toon's Gag Track, given gag_track# and list of gag_exps

    Args:
        gag_track (int): Index number of the Gag Track <0-6>
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
    return current_exps[gag_track]


def get_gag_exp_needed(gag_track: int, gag_level: int, current_exps: list) -> int:  # noqa
    """Return the Gag Track EXP required to advance to next Gag Track level

    Args:
        gag_track (int): Index number of the Gag Track <0-6>
        gag_level (int): Level of the Gag <0-6>
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
    current_gag_exp = get_gag_exp(gag_track, current_exps)
    next_gag_exp = LEVELS[gag_track][gag_level+1]
    return next_gag_exp - current_gag_exp


def get_gag_carry_limits(gag_track: int, gag_level: int) -> tuple:
    """Return list of Gag carry limits based on Gag level

    Args:
        gag_track (int): Index number of the Gag Track <0-6>
        gag_level (int): Level of the Gag <0-6>

    Returns:
        tuple: 7-member tuple of Gag carry limits

        Example output for level 2 Drop track carry limits (track=6, lvl=1) ::
            GAG_CARRY_LIMITS[6][1] = (10, 5, 0, 0, 0, 0, 0)
    """

    return GAG_CARRY_LIMITS[gag_track][gag_level]
