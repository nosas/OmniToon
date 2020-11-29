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

# Experience points needed to unlock the gag at the indexed position
LEVELS = [[0, 20, 200, 800, 2000, 6000, 10000],    # Toon-Up
          [0, 20, 100, 800, 2000, 6000, 10000],    # Trap
          [0, 20, 100, 800, 2000, 6000, 10000],    # Lure
          [0, 40, 200, 1000, 2500, 7500, 10000],   # Sound
          [0, 10, 50, 400, 2000, 6000, 10000],     # Throw
          [0, 10, 50, 400, 2000, 6000, 10000],     # Squirt
          [0, 20, 100, 500, 2000, 6000, 10000]]    # Drop

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
                    ((5, 0, 0, 0, 0, 0, 0),       # Trap
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
    count = 0
    for gag_track in gags:
        count += sum(gag_track)

    return count


def get_gag_damage(gag_track: int, gag_level: int, exp: int):
    """Return Gag damage based on Gag level and exp

    Args:
        gag_track (int): Index of Gag track
        gag_level (int): Level of the Gag track
        exp (int): Current EXP o
    Returns:
        int: Damage of Gag
    """
    # MIN_MAX_TUPLE = GAG_DAMAGE[GAG_TRACK_INDEX][GAG_INDEX] = ((min_dmg, max_dmg), (min_exp, max_exp))  # noqa
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


def get_gag_carry_limits(gag_track, gag_level):
    """Return list of Gag carry limits based on Gag level

    Args:
        gag_track (int): Index of Gag track
        gag_level (int): Level of the Gag track

    Returns:
        tuple: 7-member tuple of Gag carry limits
    """

    return GAG_CARRY_LIMITS[gag_track][gag_level]


# %% Test `get_gag_damage`
# TODO: Create tests to verify functions are always working as expected
gag_track = THROW_TRACK
gag_level = 5
exp = 8690
min_exp = GAG_DAMAGE[gag_track][gag_level][1][0]
max_exp = GAG_DAMAGE[gag_track][gag_level][1][1]
gag_damage = get_gag_damage(gag_track=gag_track, gag_level=gag_level, exp=exp)

print(min_exp, max_exp, gag_damage)

# %% Test `get_gag_carry_limits`
gag_track = THROW_TRACK
gag_level = 5
carry_limits = get_gag_carry_limits(gag_track=gag_track, gag_level=gag_level)
print(carry_limits)

# %% Print carry limits, damage, and EXP of Astro's backpack
astro_levels = [5, 0, 6, 5, 5, 5, 2]
astro_exp = [7421, 0, 10101, 9443, 8690, 6862, 191]

for gag_track_index, label in enumerate(GAG_TRACK_LABELS):
    gag_track = gag_track_index
    gag_level = astro_levels[gag_track_index]

    if gag_level == 0:  # Skip if Gag track is not unlocked
        continue

    # Get current Gag track EXP and max Gag track EXP
    exp = astro_exp[gag_track_index]
    if gag_level != 6:
        # LEVELS indexing is offset by -1. LEVELS[0] is 0, but LEVELS[6] is 10k
        # Increment the `gag_level` by 1 to correct the offset, unless the
        # Gag track is already maxed out at gag_level=6
        max_exp = LEVELS[gag_track_index][gag_level+1]
    else:
        max_exp = LEVELS[gag_track_index][gag_level]

    # Get 7-member tuple of Gag carry limits
    carry_limits = get_gag_carry_limits(
        gag_track=gag_track, gag_level=gag_level
    )

    print(label)
    print(f"    EXP: {exp}/{max_exp}")
    print(f"    LIM: {carry_limits}")

    # Get Gag damage/limit if the Gag is unlocked
    for gag_index, gag_limit in enumerate(carry_limits):
        if gag_limit == 0:  # Skip Gag damage/limit if Gag is not unlocked
            continue
        damage = get_gag_damage(
            gag_track=gag_track_index, gag_level=gag_index, exp=exp
        )
        print(f"        DMG: {damage}, LIM: {gag_limit}")
