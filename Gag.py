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

from dataclasses import dataclass, field
from math import floor as math_floor
from typing import Optional

from .AttackGlobals import Group
from .GagGlobals import (GAG_CARRY_LIMITS, GAG_DAMAGE, GAG_LABELS,
                         GAG_TRACK_LABELS, LEVELS, MULTI_TARGET_GAGS)


@dataclass
class Gag:

    # def __init__(self, track: int, exp: int, level: int, count: int = 0):
    # TODO #25, Create observer to monitor battles & determine viable Gags
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
    count: Optional[int] = field(default=0)

    # TODO Create function to get max count
    # Maximum number of carryable gags of this level
    # self.capacity_maximum = 5 + (5*(highest_level-level))

    def __post_init__(self):
        self.name = get_gag_name(track=self.track, level=self.level)
        self.track_name = get_gag_track_name(track=self.track)
        # ! Damage, quantity, capacity need to be dynamically updated after atk
        self.damage = get_gag_damage(track=self.gag.track, level=self.gag.level, exp=self.gag.exp)
        self.accuracy = get_gag_accuracy(track=self.gag.track, level=self.gag.level)
        self.target = get_gag_target(name=self.name)

    def __str__(self):
        # print(gag_throw) == 'Lvl 3 Throw, "Whole Fruit Pie" (2million dmg)'
        return f'lvl {self.level} {self.track_name} '\
               f'"{self.name}" ({self.track, self.level}, {self.damage}dmg)'

    def __repr__(self):
        # repr(gag_throw) == (track_idx, level, exp, damage_min, damage_max,
        #                     damage, accuracy, count_current, count_max)
        return f'Gag(track_name="{self.track_name}", track={self.track}, '\
               f'level={self.level}, name="{self.name}", count={self.count}, '\
               f'damage={self.damage}, exp={self.exp}, setup={self.is_setup},'\
               f' attack={self.is_attack})'


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
    return Group.Multi if name in MULTI_TARGET_GAGS else Group.Single


def get_gag_track_name(track: int) -> str:
    """Return name of the Gag Track, given a track#

    Args:
        track (int): Index number of the Gag Track <0-6>

    Returns:
        str: Name of the Gag Track, typically used for logging messages
    """
    return GAG_TRACK_LABELS[track]
