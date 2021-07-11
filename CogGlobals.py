# Originals:
# * https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/toonbase/TTLocalizerEnglish.py  # noqa
# * https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/toonbase/ToontownBattleGlobals.py  # noqa
# * https://github.com/forest2001/Toontown-Rewritten/blob/master/toontown/battle/SuitBattleGlobals.py  # noqa

from random import randint

from .AttackGlobals import ATK_TGT_SINGLE, ATK_TGT_MULTI
from .Exceptions import (InvalidAttackIndex, InvalidAttackName, InvalidCogKey,
                         InvalidRelativeLevel)

ATK_IDX_NAME, ATK_IDX_TGT, ATK_IDX_DMG, \
    ATK_IDX_ACC, ATK_IDX_FREQ = (0, 1, 2,
                                 3, 4)
COG_HP = (6, 12, 20, 30, 42, 56, 72, 90, 110, 132, 156, 200)
# ! Correct the strange formatting from SuitBattleGlobals with following regex
# \((\d{1,3},)\n\s+(\d{1,3},)\n\s+(\d{1,3},)\n\s+(\d{1,3},)\n\s+(\d{1,3})\)
# ($1 $2 $3 $4 $5)
# ! TODO #8,  Add 1 to all Cog's minimum levels (Done for BossBots)
# ! TODO #8, Add ATK_TGT_ to every Cog's attack
# ! NOTE : Minimum Cog Level is 1, not 0
# ! Create get_cog_atk_tgt(atk_name=cog_attack['name']), return 0,1,2
COG_ATTRIBUTES = {
    'f': {
        'name': 'Flunky',
        'singularname': 'a Flunky',
        'pluralname': 'Flunkies',
        # 'name': TTLocalizer.SuitFlunky
        # 'singularname': TTLocalizer.SuitFlunkyS,
        # 'pluralname': TTLocalizer.SuitFlunkyP,

        'level': 1,  # minimum Cog level, max level = min_level+4
        'hp': COG_HP[0:5],  # Cog HP range from 'min_rel_level' to '..level'+5
        'def': (2, 5, 10, 12, 15),
        'freq': (50, 30, 10, 5, 5),
        'acc': (35, 40, 45, 50, 55),
        'attacks': (
            ('PoundKey', ATK_TGT_SINGLE,  # Name, Target
                (2, 2, 3, 4, 6),          # Dmg
                (75, 75, 80, 80, 90),     # Acc
                (30, 35, 40, 45, 50)),    # Freq
            ('Shred', ATK_TGT_SINGLE,
                (3, 4, 5, 6, 7),
                (50, 55, 60, 65, 70),
                (10, 15, 20, 25, 30)),
            ('ClipOnTie', ATK_TGT_SINGLE,
                (1, 1, 2, 2, 3),
                (75, 80, 85, 90, 95),
                (60, 50, 40, 30, 20))
        )
    },
    'p': {
        'name': 'PencilPusher',
        'level': 2,
        'hp': COG_HP[1:6],
        'def': (5, 10, 15, 20, 25),
        'freq': (50, 30, 10, 5, 5),
        'acc': (45, 50, 55, 60, 65),
        'attacks': (
            ('FountainPen', ATK_TGT_SINGLE,
                (2, 3, 4, 6, 9),
                (75, 75, 75, 75, 75),
                (20, 20, 20, 20, 20)),
            ('RubOut', ATK_TGT_SINGLE,
                (4, 5, 6, 8, 12),
                (75, 75, 75, 75, 75),
                (20, 20, 20, 20, 20)),
            ('FingerWag', ATK_TGT_SINGLE,
                (1, 2, 2, 3, 4),
                (75, 75, 75, 75, 75),
                (35, 30, 25, 20, 15)),
            ('WriteOff', ATK_TGT_SINGLE,
                (4, 6, 8, 10, 12),
                (75, 75, 75, 75, 75),
                (5, 10, 15, 20, 25)),
            ('FillWithLead', ATK_TGT_SINGLE,
                (3, 4, 5, 6, 7),
                (75, 75, 75, 75, 75),
                (20, 20, 20, 20, 20))
        )
    },
    'ym': {
        'name': 'Yesman',
        'level': 3,
        'hp': COG_HP[2:7],
        'def': (10, 15, 20, 25, 30),
        'freq': (50, 30, 10, 5, 5),
        'acc': (65, 70, 75, 80, 85),
        'attacks': (
            ('RubberStamp', ATK_TGT_SINGLE,
                (2, 2, 3, 3, 4),
                (75, 75, 75, 75, 75),
                (35, 35, 35, 35, 35)),
            ('RazzleDazzle', ATK_TGT_SINGLE,
                (1, 1, 1, 1, 1),
                (50, 50, 50, 50, 50),
                (25, 20, 15, 10, 5)),
            ('Synergy', ATK_TGT_MULTI,
                (4, 5, 6, 7, 8),
                (50, 60, 70, 80, 90),
                (5, 10, 15, 20, 25)),
            ('TeeOff', ATK_TGT_SINGLE,
                (3, 3, 4, 4, 5),
                (50, 60, 70, 80, 90),
                (35, 35, 35, 35, 35))
        )
    },
    'mm': {
        'name': 'Micromanager',
        'level': 4,
        'hp': COG_HP[3:8],
        'def': (15, 20, 25, 30, 35),
        'freq': (50, 30, 10, 5, 5),
        'acc': (70, 75, 80, 82, 85),
        'attacks': (
            ('Demotion', ATK_TGT_SINGLE,
                (6, 8, 12, 15, 18),
                (50, 60, 70, 80, 90),
                (30, 30, 30, 30, 30)),
            ('FingerWag', ATK_TGT_SINGLE,
                (4, 6, 9, 12, 15),
                (50, 60, 70, 80, 90),
                (10, 10, 10, 10, 10)),
            ('FountainPen', ATK_TGT_SINGLE,
                (3, 4, 6, 8, 10),
                (50, 60, 70, 80, 90),
                (15, 15, 15, 15, 15)),
            ('BrainStorm', ATK_TGT_SINGLE,
                (4, 6, 9, 12, 15),
                (5, 5, 5, 5, 5),
                (25, 25, 25, 25, 25)),
            ('BuzzWord', ATK_TGT_SINGLE,
                (4, 6, 9, 12, 15),
                (50, 60, 70, 80, 90),
                (20, 20, 20, 20, 20))
        )
    },
    'ds': {
        'name': 'Downsizer',
        'level': 5,
        'hp': COG_HP[4:9],
        'def': (20, 25, 30, 35, 40),
        'freq': (50, 30, 10, 5, 5),
        'acc': (35, 40, 45, 50, 55),
        'attacks': (
            ('Canned', ATK_TGT_SINGLE,
                (5, 6, 8, 10, 12),
                (60, 75, 80, 85, 90),
                (25, 25, 25, 25, 25)),
            ('Downsize', ATK_TGT_SINGLE,
                (8, 9, 11, 13, 15),
                (50, 65, 70, 75, 80),
                (35, 35, 35, 35, 35)),
            ('PinkSlip', ATK_TGT_SINGLE,
                (4, 5, 6, 7, 8),
                (60, 65, 75, 80, 85),
                (25, 25, 25, 25, 25)),
            ('Sacked', ATK_TGT_SINGLE,
                (5, 6, 7, 8, 9),
                (50, 50, 50, 50, 50),
                (15, 15, 15, 15, 15))
        )
    },
    'hh': {
        'name': 'HeadHunter',
        'level': 6,
        'hp': COG_HP[5:10],
        'def': (25, 30, 35, 40, 45),
        'freq': (50, 30, 10, 5, 5),
        'acc': (35, 40, 45, 50, 55),
        'attacks': (
            ('FountainPen', ATK_TGT_SINGLE,
                (5, 6, 8, 10, 12),
                (60, 75, 80, 85, 90),
                (15, 15, 15, 15, 15)),
            ('GlowerPower', ATK_TGT_SINGLE,
                (7, 8, 10, 12, 13),
                (50, 60, 70, 80, 90),
                (20, 20, 20, 20, 20)),
            ('HalfWindsor', ATK_TGT_SINGLE,
                (8, 10, 12, 14, 16),
                (60, 65, 70, 75, 80),
                (20, 20, 20, 20, 20)),
            ('HeadShrink', ATK_TGT_SINGLE,
                (10, 12, 15, 18, 21),
                (65, 75, 80, 85, 95),
                (35, 35, 35, 35, 35)),
            ('Rolodex', ATK_TGT_SINGLE,
                (6, 7, 8, 9, 10),
                (60, 65, 70, 75, 80),
                (10, 10, 10, 10, 10))
        )
    },
    'cr': {
        'name': 'CorporateRaider',
        'level': 7,
        'hp': COG_HP[6:11],
        'def': (30, 35, 40, 45, 50),
        'freq': (50, 30, 10, 5, 5),
        'acc': (35, 40, 45, 50, 55),
        'attacks': (
            ('Canned', ATK_TGT_SINGLE,
                (6, 7, 8, 9, 10),
                (60, 75, 80, 85, 90),
                (20, 20, 20, 20, 20)),
            ('EvilEye', ATK_TGT_SINGLE,
                (12, 15, 18, 21, 24),
                (60, 70, 75, 80, 90),
                (35, 35, 35, 35, 35)),
            ('PlayHardball', ATK_TGT_SINGLE,
                (7, 8, 12, 15, 16),
                (60, 65, 70, 75, 80),
                (30, 30, 30, 30, 30)),
            ('PowerTie', ATK_TGT_SINGLE,
                (10, 12, 14, 16, 18),
                (65, 75, 80, 85, 95),
                (15, 15, 15, 15, 15))
        )
    },
    'tbc': {
        'name': 'TheBigCheese',
        'level': 8,
        'hp': COG_HP[7:12],
        'def': (35, 40, 45, 50, 55),
        'freq': (50, 30, 10, 5, 5),
        'acc': (35, 40, 45, 50, 55),
        'attacks': (
            ('CigarSmoke', ATK_TGT_SINGLE,
                (10, 12, 15, 18, 20),
                (55, 65, 75, 85, 95),
                (20, 20, 20, 20, 20)),
            ('FloodTheMarket', ATK_TGT_SINGLE,
                (14, 16, 18, 20, 22),
                (70, 75, 85, 90, 95),
                (10, 10, 10, 10, 10)),
            ('SongAndDance', ATK_TGT_SINGLE,
                (14, 15, 17, 19, 20),
                (60, 65, 70, 75, 80),
                (20, 20, 20, 20, 20)),
            ('TeeOff', ATK_TGT_SINGLE,
                (8, 11, 14, 17, 20),
                (55, 65, 70, 75, 80),
                (50, 50, 50, 50, 50))
        )
    }
}


def get_actual_from_relative_level(cog_key: str, relative_level: int) -> int:
    """Get a Cog's actual level from its cog key and relative level

    Args:
        cog_key (str): Key value for COG_ATTRIBUTES of the Cog's name.
            Example input :: 'f' for Flunky, 'p' for PencilPusher
        relative_level (int): Relative level of the Cog, <0-4>

    Returns:
        int: Cog's actual level (cog_min_level + relative_level)
    """
    if cog_key not in COG_ATTRIBUTES:
        raise InvalidCogKey
    if relative_level not in range(5):
        raise InvalidRelativeLevel(rel_lvl=relative_level)
    cog_data = COG_ATTRIBUTES[cog_key]
    actual_level = cog_data['level'] + relative_level
    return actual_level


def get_cog_attack(cog_key: str, relative_level: int, attack_index: int = -1) -> dict:   # noqa
    """Return dictionary of Cog's attack given COG_ATTR key and relative_level,
        returns a pseudo-random Cog attack if attack_index argument

    Args:
        cog_key (str): Key value for COG_ATTRIBUTES of the Cog's name.
            Example input :: 'f' for Flunky, 'p' for PencilPusher
        relative_level (int): Relative level of the Cog, <0-4>
        attack_index (int, optional): Should be within the range of
            (0, len(Cog.attacks)).
            Defaults to -1, selects random attack.

    Returns:
        dict: Dictionary containing cog key, atk name/id/hp(dmg)/acc/freq etc.

        Example attack dictionary for lvl 2 Flunky (key='f', lvl='1', atk=0) ::
            {
                'cog_key': 'f',
                'name': 'PoundKey',
                'id': 0,
                'damage': 3,
                'acc': 80,
                'freq': 40,
                'target': 2  # ATK_TGT_SINGLE=1, ATK_TGT_MULTI=2
            }
    """
    if cog_key not in COG_ATTRIBUTES:
        raise InvalidCogKey
    if relative_level not in range(5):
        raise InvalidRelativeLevel(rel_lvl=relative_level)

    # * attack_choices == COG_ATTRIBUTES[cog_key]['attacks']
    attack_choices = get_cog_attacks_all_levels(cog_key=cog_key)
    if attack_index == -1:  # Select random attack_index
        # notify.debug('get_cog_attack: picking attacking for %s' % cog_key)
        attack_index = pick_cog_attack(attack_choices=attack_choices,
                                       relative_level=relative_level)

    if attack_index not in range(-1, len(attack_choices)):
        raise InvalidAttackIndex

    attack_tuple = attack_choices[attack_index]
    """ Example attack tuple ::
            (
                'PoundKey', ATK_TGT_SINGLE, # Name, Target
                (2, 2, 3, 4, 6),            # Dmg
                (75, 75, 80, 80, 90),       # Acc
                (30, 35, 40, 45, 50)        # Freq
            )
    """
    attack_dict = {}
    attack_dict['cog_key'] = cog_key
    attack_name = attack_tuple[ATK_IDX_NAME]
    attack_dict['name'] = attack_name
    attack_dict['id'] = attack_index
    # attack_dict['id'] = list(COG_ATTACKS.keys()).index(attack_name)
    # attack_dict['animName'] = COG_ATTACKS[attack_name][0]
    attack_dict['damage'] = attack_tuple[ATK_IDX_DMG][relative_level]
    attack_dict['acc'] = attack_tuple[ATK_IDX_ACC][relative_level]
    attack_dict['freq'] = attack_tuple[ATK_IDX_FREQ][relative_level]
    attack_dict['target'] = attack_tuple[ATK_IDX_TGT]  # previously group
    # attack_dict['group'] = COG_ATTACKS[attack_name][1]
    return attack_dict


def get_cog_attacks_all_levels(cog_key: str) -> tuple:
    """Return tuple containing all possible Cog attack choices for a single Cog

    Args:
        cog_key (str): Cog key, short-hand of the Cog's name

    Returns:
        attack_choices (tuple): All possible Cog attack choices

        Example output for cog_key='f' ::
            'attacks': (
                ('PoundKey', ATK_TGT_SINGLE  [0] Name, [1] Target
                    (2, 2, 3, 4, 6),         [2] Damage
                    (75, 75, 80, 80, 90),    [3] Accuracy
                    (30, 35, 40, 45, 50)),   [4] Frequency
                ('Shred', ATK_TGT_SINGLE
                    (3, 4, 5, 6, 7),
                    (50, 55, 60, 65, 70),
                    (10, 15, 20, 25, 30)),
                ('ClipOnTie', ATK_TGT_SINGLE
                    (1, 1, 2, 2, 3),
                    (75, 80, 85, 90, 95),
                    (60, 50, 40, 30, 20))
            )
    """
    if cog_key not in COG_ATTRIBUTES:
        raise InvalidCogKey
    return COG_ATTRIBUTES[cog_key]['attacks']


def get_cog_vitals(cog_key: str, relative_level: int = -1) -> dict:
    """Return dictionary of Cog's vital info, given cog_key and relative_level

    Args:
        cog_key (str): Key used to obtain desired Cog from `COG_ATTRIBUTES`
        relative_level (int, optional): Relative level from 0-4. Defaults to -1

    Returns:
        vitals_dict: Structured dictionary containing vital Cog information

        Example output for (cog_key='f', relative_lvl=4) ::
            {
                'name': 'Flunky',
                'level': 5,
                'hp': 42,
                'def': 15,
                'attacks': [
                    {
                        'acc': 80,
                        'freq': 40,
                        'damage': 3,
                        'id': 0,
                        'name': 'PoundKey',
                        'target': 1  # <0-2> ATK_TGT_SINGLE=1, ATK_TGT_MULTI=2
                    }
                    {
                        'acc': 70,
                        'freq': 30,
                        'damage': 7,
                        'id': 1,
                        'name': 'Shred',
                        'target': 1
                    },
                    {
                        'acc': 95,
                        'freq': 20,
                        'damage': 3,
                        'id': 2,
                        'name': 'ClipOnTie',
                        'target': 1
                    }
                ]
            }
    """
    if cog_key not in COG_ATTRIBUTES:
        raise InvalidCogKey

    if relative_level not in range(-1, 5):
        raise InvalidRelativeLevel(rel_lvl=relative_level)

    cog_data = COG_ATTRIBUTES[cog_key]
    # Pick pseudo-random Cog level if no relative_level is provided
    if relative_level == -1:
        relative_level = pick_from_freq_list(cog_data['freq'])
    vitals_dict = {}
    vitals_dict['level'] = get_actual_from_relative_level(
        cog_key=cog_key, relative_level=relative_level)
    if vitals_dict['level'] == 12:  # for level 12 cogs, ex: Skelecogs
        relative_level = 0
    vitals_dict['name'] = cog_data['name']
    vitals_dict['hp'] = cog_data['hp'][relative_level]
    vitals_dict['def'] = cog_data['def'][relative_level]

    attacks = cog_data['attacks']
    all_attacks_list = []
    for attack_index, attack_tuple in enumerate(attacks):
        attack_dict = {}
        attack_dict['cog_key'] = cog_key
        attack_name = attack_tuple[ATK_IDX_NAME]
        attack_dict['name'] = attack_name
        attack_dict['id'] = attack_index
        # attack_dict['id'] = list(COG_ATTACKS.keys()).index(attack_name)
        # attack_dict['animName'] = COG_ATTACKS[attack_name][0]
        attack_dict['damage'] = attack_tuple[ATK_IDX_DMG][relative_level]
        attack_dict['acc'] = attack_tuple[ATK_IDX_ACC][relative_level]
        attack_dict['freq'] = attack_tuple[ATK_IDX_FREQ][relative_level]
        attack_dict['target'] = attack_tuple[ATK_IDX_TGT]  # previously group
        # attack_dict['group'] = COG_ATTACKS[attack_name][1]
        all_attacks_list.append(attack_dict)

    vitals_dict['attacks'] = all_attacks_list
    return vitals_dict


def pick_cog_attack(attack_choices: tuple, relative_level, attack_name='') -> int:  # noqa
    # ! This does not support `cog.attacks` dict as input, use cog.get_attack()
    """Return a pseudo-random attack index obtained from
    `get_cog_attacks_all_levels`, unless `attack_name` argument is provided.

    Args:
        attack_choices (tuple): List of Cog's attack choices, retrieved from
            `get_cog_attacks_all_levels` function
            Example of `attack_choices` ::
                attack_choices = (
                    ('PoundKey', ATK_TGT_SINGLE  [0] Name, [1] Target
                        (2, 2, 3, 4, 6),         [2] Damage
                        (75, 75, 80, 80, 90),    [3] Accuracy
                        (30, 35, 40, 45, 50)),   [4] Frequency
                    ('Shred', ATK_TGT_SINGLE
                        (3, 4, 5, 6, 7),
                        (50, 55, 60, 65, 70),
                        (10, 15, 20, 25, 30)),
                    ('ClipOnTie', ATK_TGT_SINGLE
                        (1, 1, 2, 2, 3),
                        (75, 80, 85, 90, 95),
                        (60, 50, 40, 30, 20))
                )
        relative_level (int): Level relative to the Cog's minimum lvl <0-5>
        attack_name (str, optional): Attack name as seen in
            COG_ATTRS[cog_key]['attacks'][0] or `get_cog_attacks_all_levels`
            function
            Example of valid input ::
                <'PoundKey'|'Shred'|'ClipOnTie'>

    Returns:
        int: Index of the Cog attack
    """
    # TODO #77, Verify attack_choices input is valid

    if relative_level not in range(5):
        raise InvalidRelativeLevel(rel_lvl=relative_level)

    # If attack_name is specified
    if attack_name:
        all_attack_names = [attack[ATK_IDX_NAME] for attack in attack_choices]
        if attack_name not in all_attack_names:
            raise InvalidAttackName
        return all_attack_names.index(attack_name)

    # else, return pseudo-random attack based on the attack's frequency
    attack_index = None
    rand_num = randint(0, 99)
    count = 0

    for cur_index, attack in enumerate(attack_choices):
        atk_frequency = attack[ATK_IDX_FREQ][relative_level]
        count += atk_frequency
        if rand_num < count:
            attack_index = cur_index
            break
    return attack_index


def pick_from_freq_list(freq_list: tuple or list) -> int:
    """Return a pseudo-random relative level of a Cog, given a 5-member tuple
        or list, can be obtained from COG_ATTRIBUTES[cog_key]['freq'].

        The higher the frequency value <0-99>, the higher chance that relative
        level (index of the frequency value) is returned.

    Args:
        freq_list (<tuple|list>): List containing the 5 frequency values

        Example of freq_list bias towards relative_level=0 ::
            freq_list = (50, 30, 10, 5, 5)
            returns =   (0,   1,  2, 3, 4)

    Returns:
        int: Relative level of the Cog
    """
    rand_num = randint(0, 99)
    count = 0
    index = 0
    level = None

    for index, freq in enumerate(freq_list):
        count = count + freq
        if rand_num < count:
            level = index
            break
    return level
