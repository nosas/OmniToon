# Original: https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/toonbase/ToontownBattleGlobals.py  # noqa

from math import floor as math_floor

# Gag indexes
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

# Experience points needed to unlock the gag at the indexed position
LEVELS = [[0, 20, 200, 800, 2000, 6000, 10000],    # Toon-Up
          [0, 20, 100, 800, 2000, 6000, 10000],    # Trap
          [0, 20, 100, 800, 2000, 6000, 10000],    # Lure
          [0, 40, 200, 1000, 2500, 7500, 10000],   # Sound
          [0, 10, 50, 400, 2000, 6000, 10000],     # Throw
          [0, 10, 50, 400, 2000, 6000, 10000],     # Squirt
          [0, 20, 100, 500, 2000, 6000, 10000]]    # Drop

# MIN_MAX_TUPLE = GAG_DAMAGE[GAG_INDEX][GAG_LEVEL] = ((min_dmg, max_dmg), (min_exp, max_exp))  # noqa
# MIN_DMG, MAX_DMG = MIN_MAX_TUPLE[0] = (min_dmg, max_dmg)
# MIN_EXP, MAX_EXP = MIN_MAX_TUPLE[1] = (min_exp, max_exp)
#    Example of Level 3 throw min/max = GAG_DAMAGE[4][3]
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


def get_gag_damage(gag_track, gag_level, exp):
    # def get_gag_damage(gag_track, gag_level, exp, organicBonus=False,
    #                    propBonus=False, propAndOrganicBonusStack=False):
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


# %% Test `get_gag_damage`
# TODO: Create tests to verify functions are always working as expected
gag_track = THROW_TRACK
gag_level = 5
exp = 8690
min_exp = GAG_DAMAGE[gag_track][gag_level][1][0]
max_exp = GAG_DAMAGE[gag_track][gag_level][1][1]
gag_damage = get_gag_damage(gag_track=gag_track, gag_level=gag_level, exp=exp)

print(min_exp, max_exp, gag_damage)
